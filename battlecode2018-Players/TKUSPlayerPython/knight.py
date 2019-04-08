import battlecode as bc
import random

directions = list(bc.Direction)
unit = 0
quads = []
mapWidth = 0
mapHeight = 0
gc = 0


#note: (0,0) is the bottom left square

def knightLogic(unitParam, quadsParam, mapWidthParam, mapHeightParam, gcParam):
    global unit
    global quads
    global mapWidth
    global mapHeight
    global gc
    unit = unitParam
    quads = quadsParam
    mapWidth = mapWidthParam
    mapHeight = mapHeightParam
    gc = gcParam



    #movement logic will be skipped if knight is in space or in garrison
    if not unit.location.is_in_garrison() and not unit.location.is_in_space():
        #trys to attack a nearby unit.  If there is nothing to attack or if it cant attack then it will try to move
        if tryToAttack() == False:
            d = getMoveDirection()

            #if the knight can move towards the center it will, otherwise it will choose a random direction
            if gc.is_move_ready(unit.id) and gc.can_move(unit.id, d):
                gc.move_robot(unit.id, d)
            else:
                # pick a random direction:
                d = random.choice(directions)
                if gc.is_move_ready(unit.id) and gc.can_move(unit.id, d):
                    gc.move_robot(unit.id, d)
    

#current idea for knight movement:
#figure out how many of our non-knight units are in each quadrant.  Have the knights move to the quadrant with the least friendly units.
#once in that quadrant they can move randomly
def getMoveDirection():
    
    #gets the population of the smallest populated quadrant.  Then sees if there are other quadrants with the same number and puts it into a list.
    #if so it chooses a random quadrant from the list
    leastPopQuadNum = min(quads)
    smallestQuads = []
    for i in range (0, len(quads)):
        if leastPopQuadNum == quads[i]:
            smallestQuads.append(i)
    
    moveToQuad = smallestQuads[random.randint(0, len(smallestQuads) - 1)]

    #creates a newmapLocation which will be the center of the quadrant we need to go to
    quadCenter = bc.MapLocation(unit.location.map_location().planet, 0, 0)

    #sets the center of the quadrants coords
    if moveToQuad == 0:
        quadCenter.x = int(mapWidth - mapWidth/4)
        quadCenter.y = int(mapHeight - mapHeight/4)
    elif moveToQuad == 1:
        quadCenter.x = int(mapWidth/4)
        quadCenter.y = int(mapHeight - mapHeight/4)
    elif moveToQuad == 2:
        quadCenter.x = int(mapWidth)
        quadCenter.y = int(mapHeight/4)
    else:
        quadCenter.x = int(mapWidth - mapWidth/4)
        quadCenter.y = int(mapHeight/4)

    returnDirection = unit.location.map_location().direction_to(quadCenter)
    
    return returnDirection


#this function will return true if there is a nearby enemy unit and the knight can attack it.  Otherwise it will return false.
#if it can attack it will
def tryToAttack():

    nearbyEnemies = []
    if unit.team == bc.Team.Red:
        nearbyEnemies = gc.sense_nearby_units_by_team(unit.location.map_location(), 2, bc.Team.Blue)
    else:
        nearbyEnemies = gc.sense_nearby_units_by_team(unit.location.map_location(), 2, bc.Team.Red)

    #if there are no enemies then return false
    if len(nearbyEnemies) == 0:
        return False

    for enemy in nearbyEnemies:
        if gc.can_attack(unit.id, enemy.id) and unit.attack_heat() < 10 :
            gc.attack(unit.id, enemy.id)
            print("attacked", enemy.id)
            return True

    return False