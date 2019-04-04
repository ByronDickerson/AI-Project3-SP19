# Knight Unit Targeting
# Need token force to stay with rangers
# otherwise SEARCH AND DESTROY
# retreat to healer if low

import random

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
            if other.team != my_team and gc.is_attack_ready(unit.id):
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
                if other.team != my_team:
                    gc.javelin(unit.id, other.id)
        # else no javelin, carry on

        # if unit can move
        if gc.is_move_ready(unit.id):
            # list all units within sight range
            longrange = gc.sense_nearby_units(location.map_location(), 50)

            for other in longrange:
                # does this unit have low health and has it located a friendly healer?
                seekhealer = unit.health < 50 and other.team == my_team and other.unit_type == bc.UnitType.Healer

                # direction to walk in, should get changed below
                d = bc.Direction.Center 
                
                # if enemy or a needed healer is spotted, go towards that unit
                if seekhealer or other.team != my_team:
                    # determine other's position, relative to ours
                    ourX = unit.location.map_location().x
                    ourY = unit.location.map_location().y
                    otherX = other.location.map_location().x
                    otherY = other.location.map_location().y
                    distanceX = ourX - otherX # if distanceX is negative, the enemy is to the west
                    distanceY = ourY - otherY # if distanceY is negative, the enemy is to the south

                    # determine which direction is best to move in
                    # 'abs()' returns the absolute value of a number
                    if abs(distanceX) > abs(distanceY):
                        if distanceX < 0: d = bc.Direction.West
                        else: d = bc.Direction.East
                    else:
                        if distanceY < 0: d = bc.Direction.South
                        else: d = bc.Direction.North                     

                # if no better options, move randomly
                else:
                    directions = list(bc.Direction)
                    d = random.choice(directions)
                    
                # take actual movement
                if gc.is_move_ready(unit.id) and gc.can_move(unit.id, d):
                    gc.move_robot(unit.id, d)
        # else no motion, carry on
