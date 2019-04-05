import battlecode as bc 
import MyInfo
import random

possibleDirections = list(bc.Direction)
unit = 0
gc = 0

#I used Slink3 and TKUS's ranger classes and tried to combine them into this
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
    enemies = MyInfo.nearbyEnemies(unit, gc)

    #If there are enemies, attack
    if len(enemies)>0:
        for enemy in enemies:
           #try to snipe enemies
            if unit.is_ability_unlocked():
                if gc.is_begin_snipe_ready(unit.id):
                    if gc.can_begin_snipe(unit.id, enemy.location.map_location()):
                        gc.begin_snipe(unit.id, enemy.location.map_location())
                        return

            elif gc.can_attack(unit.id, enemy.id) and gc.is_attack_ready(unit.id) :
                gc.attack(unit.id, enemy.id)
                print("A Ranger Attacked")
    else:
        # Move randomly
        for direction in possibleDirections:
            if gc.can_move(unit.id, direction):
                gc.move_robot(unit.id, direction)
                return
