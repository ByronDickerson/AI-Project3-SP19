import battlecode as bc
import random

directions = list(bc.Direction)
unit = 0
gc = 0

def mageLogic(unitParam, gcParam):
    global unit
    global gc
    unit = unitParam
    gc = gcParam

    if not unit.location.is_in_garrison():
        if tryToAttack() == False:
            d = random.choice(directions)

            if gc.is_move_ready(unit.id) and gc.can_move(unit.id, d):
                gc.move_robot(unit.id, d)	



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
            return True

    return False