import battlecode as bc 
import random

directions = list(bc.Direction)
unit = 0
gc = 0

def rangerLogic(unitParam, gcParam):
    global unit
    global gc
    unit = unitParam
    gc = gcParam

    # If ranger is in garrison or space, then do nothing
    if unit.location.is_in_garrison():
        return

    if unit.ranger_is_sniping():
        return

    #if nothing is ready do nothing
    if not gc.is_attack_ready(unit.id):
        if not gc.is_move_ready(unit.id):
            return

    if not gc.is_move_ready(unit.id):
        return
    
    #Current unit location
    unitLocation = unit.location.map_location()

    #Nearby Enemy Location
    enemies = []

    #If we're red, look for blue units, else look for red units
    if unit.team == bc.Team.Red:
        enemies = gc.sense_nearby_units_by_team(unit.location.map_location(), 2, bc.Team.Blue)
    else:
        enemies = gc.sense_nearby_units_by_team(unit.location.map_location(), 2, bc.Team.Red)


   #try to snipe enemies
    if unit.is_ability_unlocked():
        if gc.is_begin_snipe_ready(unit.id):
            for enemy in enemies:
                if gc.can_begin_snipe(unit.id, enemy):
                    gc.begin_snipe(unit.id, enemy)
                    return

    #If there are enemies, attack
    if len(enemies)>0:
        for enemy in enemies:
            if gc.can_attack(unit.id, enemy.id) and unit.attack_heat() < 10 :
                gc.attack(unit.id, enemy.id)
                
    # Move randomly
    for direction in randomDirections:
        if gc.can_move(unit.id, direction):
            #gc.move_robot(unit.id, direction)
            move.goto(gc, unit.id, unitLocation.add(direction))
            return
