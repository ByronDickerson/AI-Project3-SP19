import battlecode as bc 
import random

directions = list(bc.Direction)
unit = 0
gc = 0

def rangerLogic(unitParam, gcParam):
    # If ranger is in garrison or space, then do nothing
    if not unit.location.is_on_map():
        return

    if unit.ranger_is_sniping():
        return

    unitLocation = unit.location.map_location()


def rangerAttack():
    #check map for enemies
    enemies = []
    if unit.team == bc.Team.Red:
        enemies = gc.sense_nearby_units_by_team(unit.location.map_location(), 2, bc.Team.Blue)
    else:
        enemies = gc.sense_nearby_units_by_team(unit.location.map_location(), 2, bc.Team.Red)

    if len(enemies) == 0:
        return False

    for enemy in enemies:
        if gc.can_attack(unit.id, enemy.id) and unit.attack_heat() < 10 :
            gc.attack(unit.id, enemy.id)
            return True

    return False
