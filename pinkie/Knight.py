# Knight Unit Targeting
# Seeks and destroys enemies, attacking however possible.
# Retreats to nearby healers if health is low.
# Randomly explores world map.

import battlecode as bc
import Info  

def knightAction(gc, unit):

    location = unit.location  # knight's current location
    my_team = gc.team()       # our team

    # if the location is on a map (and not inside a structure eg rocket)
    if location.is_on_map():

        # list all units within attacking range
        shortrange = gc.sense_nearby_units(location.map_location(), 2)
        
        # for units within attack range
        for other in shortrange:            
            # if the other unit is an enemy and knight can attack
            if type(other) != int and Info.enemy(other,gc) and gc.is_attack_ready(unit.id):
                #attack
                gc.attack(unit.id, other.id)
        # else no enemies near, carry on
        
        # if javelin is available and ready to use
        if gc.is_javelin_ready(unit.id):
            # list all units within javelin range
            midrange = gc.sense_nearby_units(location.map_location(), 10)

            #for units within javelin range
            for other in midrange:
                # if enemy detected, attack
                if Info.enemy(other,gc):
                    gc.javelin(unit.id, other.id)
        # else no javelin, carry on

        # if unit can move
        if gc.is_move_ready(unit.id):
            # list all units within sight range
            longrange = gc.sense_nearby_units(location.map_location(), 50)

            for other in longrange:
                # does this unit have low health and has it located a friendly healer?
                seekhealer = Info.lowHealth(unit) and (not Info.enemy(other,gc)) and other.unit_type == bc.UnitType.Healer
                
                # if enemy or a needed healer or a rocket is spotted, go towards that unit
                if seekhealer or Info.enemy(other,gc) or other.unit_type == bc.UnitType.Rocket:
                    d = Info.pathfind(unit, other)

                # if no better options, move randomly
                else:
                    d = Info.pathrand()
                    
                # take actual movement
                if gc.is_move_ready(unit.id) and gc.can_move(unit.id, d):
                    gc.move_robot(unit.id, d)
        # else no motion, carry on
