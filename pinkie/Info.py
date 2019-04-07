#The info file was inspired from Slink3's extra info.py
import battlecode as bc
import random

gc = 0
directions = list(bc.Direction)

maxKnights = 10
maxMages = 5
maxRangers = 5
maxHealers = 5
maxMages = 5
maxWorkers = 10 #not used?

def getNumUnits(unitType, gcParam):
    global gc
    gc = gcParam

    numR = 0
    numK = 0
    numH = 0
    numF = 0
    numW = 0
    numM = 0
    numRockets = 0

    for unit in gc.my_units():
        if unit.unit_type == bc.UnitType.Ranger:
            numR+= 1
        elif unit.unit_type == bc.UnitType.Knight:
            numK+= 1
        elif unit.unit_type == bc.UnitType.Healer:
            numH+= 1
        elif unit.unit_type == bc.UnitType.Factory:
            numF+= 1
        elif unit.unit_type == bc.UnitType.Rocket:
            numRockets+= 1
        elif unit.unit_type == bc.UnitType.Worker:
            numW+= 1
        elif unit.unit_type == bc.UnitType.Mage:
            numM+= 1
        


    if unitType == bc.UnitType.Ranger:
        return numR
    elif unitType == bc.UnitType.Knight:
        return numK
    elif unitType == bc.UnitType.Healer:
        return numH
    elif unitType == bc.UnitType.Factory:
        return numF
    elif unitType == bc.UnitType.Rocket:
        return numRockets
    elif unitType == bc.UnitType.Worker:
        return numW
    elif unitType == bc.UnitType.Mage:
        return numM

def nearbyEnemies(unit, gcParam):
    gc = gcParam
    nearbyEnemies = []
    
    if unit.team == bc.Team.Red:
        #nearbyEnemies = gc.sense_nearby_units(unit.location.map_location(), unit.attack_range())
        nearbyEnemies = gc.sense_nearby_units_by_team(unit.location.map_location(), unit.attack_range(), bc.Team.Blue)
    else:
        #nearbyEnemies = gc.sense_nearby_units(unit.location.map_location(), unit.attack_range())
        nearbyEnemies = gc.sense_nearby_units_by_team(unit.location.map_location(), unit.attack_range(), bc.Team.Red)
    return nearbyEnemies


# tells unit which way to walk to get closer to target
# returns a direction
def pathfind(unit, target):
    # direction to walk in, should get changed below
    #print('seeking enemy!')
    
    d = bc.Direction.Center 
                
    ourX = unit.location.map_location().x
    ourY = unit.location.map_location().y
    otherX = target.location.map_location().x
    otherY = target.location.map_location().y

    # if distanceX is negative, the enemy is to the east
    distanceX = ourX - otherX
    # if distanceY is negative, the enemy is to the north
    distanceY = ourY - otherY

    #print('Xdistance: ', distanceX)

    # determine which direction is best to move in
    # 'abs()' returns the absolute value of a number
    if abs(distanceX) > abs(distanceY):
        if distanceX < 0:
            d = bc.Direction.East
        else:
            d = bc.Direction.West
    elif distanceY < 0:
        d = bc.Direction.North
    else:
        d = bc.Direction.South

    return d

# return a random direction
def pathrand():
    return random.choice(list(bc.Direction))

# is other unit an enemy?
# returns true if other is an enemy
def enemy(other):
    return other.team != gc.team()

# does our unit have low health?
# returns true if health is below 20%
def lowHealth(unit):
   return unit.health < (unit.max_health / 5)

def get_enemy_team():
	if gc.team() == bc.Team.Blue:
		enemy_team = bc.Team.Red

	elif gc.team() == bc.Team.Red:
		enemy_team = bc.Team.Blue
	else:
		enemy_team = None
		print("oh fuck u did team wrong")
	return enemy_team