# Knight Unit Targeting
# Need token force to stay with rangers
# otherwise SEARCH AND DESTROY
# retreat to healer if low

import random
import toolbox as tb

# maybe consider also coding worker resource location

def knightAction(bc, gc, unit):
    print('knightAction called!')

    location = unit.location  # knight's current location
    my_team = gc.team()       # our team

    # if the location is on a map (and not inside a structure eg rocket)
    if location.is_on_map():

        # list all units within attacking range
        shortrange = gc.sense_nearby_units(location.map_location(), 2)
        
        # for units within attack range
        for other in shortrange:            
            # if the other unit is an enemy and knight can attack
            if tb.enemy(gc, other) and gc.is_attack_ready(unit.id):
                #attack
                print('attacked a thing!')
                gc.attack(unit.id, other.id)
        # else no enemies near, carry on
        
        # if javelin is available and ready to use
        if gc.is_javelin_ready(unit.id):
            # list all units within javelin range
            midrange = gc.sense_nearby_units(location.map_location(), 10)

            #for units within javelin range
            for other in midrange:
                # if enemy detected, attack
                if tb.enemy(gc, other):
                    gc.javelin(unit.id, other.id)
        # else no javelin, carry on

        # if unit can move
        if gc.is_move_ready(unit.id):
            # list all units within sight range
            longrange = gc.sense_nearby_units(location.map_location(), 50)

            for other in longrange:
                # does this unit have low health and has it located a friendly healer?
                seekhealer = tb.lowHealth(unit) and (not tb.enemy(gc, other)) and other.unit_type == bc.UnitType.Healer
                
                # if enemy or a needed healer is spotted, go towards that unit
                if seekhealer or tb.enemy(gc, other):
                    d = tb.pathfind(bc, unit, other)                   

                # if no better options, move randomly
                else:
                    d = tb.pathrand(bc)
                    
                # take actual movement
                if gc.is_move_ready(unit.id) and gc.can_move(unit.id, d):
                    gc.move_robot(unit.id, d)
        # else no motion, carry on
