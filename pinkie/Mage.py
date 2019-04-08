#https://github.com/AnPelec/Battlecode-2018/blob/master/Project%20Achilles/run.py
import battlecode as bc
import random

import Info

def blink_attack_mars(gc, unit):
    if not gc.is_blink_ready(unit.id):
        return
    if bc.ResearchInfo().get_level(bc.UnitType.Mage) < 4:
        return
        
    location = unit.location
    enemy_team = Info.get_enemy_team()
        
    possible_targets = gc.sense_nearby_units_by_team(location.map_location(), 2, enemy_team)
    if len(possible_targets) > 2:
        return
        
    for guess in range(NUMBER_OF_GUESSES):
        i = random.randint(0, marsHeight-1)
        j = random.randint(0, marsWidth-1)
        
        try:
            temp_location = bc.MapLocation(bc.Planet.Mars, i, j)
            if gc.can_blink(unit.id, temp_location):
                gc.blink(unit.id, temp_location)
                return
                
        except Exception as e:
            print('Error:', e)
            # use this to show where the error was
            #traceback.print_exc()

def blink_attack_earth(gc, unit):
    if not gc.is_blink_ready(unit.id):
        return
    if bc.ResearchInfo().get_level(bc.UnitType.Mage) < 4:
        return
        
    location = unit.location
    enemy_team = Info.get_enemy_team()
    
    possible_targets = gc.sense_nearby_units_by_team(location.map_location(), 2, enemy_team)
    if len(possible_targets) > 2:
        return
    '''        
    for guess in range(NUMBER_OF_GUESSES):
        i = random.randint(0, earthHeight-1)
        j = random.randint(0, earthWidth-1)
        
        try:
            temp_location = bc.MapLocation(bc.Planet.Earth, i, j)
            if gc.can_blink(unit.id, temp_location):
                gc.blink(unit.id, temp_location)
                return
                
        except Exception as e:
            print('Error:', e)
            # use this to show where the error was
            #traceback.print_exc()
    '''

def run_toward_rocket(unit, r):
    if r.unit_type == bc.UnitType.Rocket and len(r.structure_garrison()) < 8:
        Info.pathfind(unit,r)

def worst_enemy(unit, enemies):
    top = enemies[0]
    for e in enemies:
        if e.health > top.health:
            top = e
    return e

def battle(gc,unit, enemy):
    if Info.enemy(enemy) and gc.is_attack_ready(unit.id) and gc.can_attack(unit.id, enemy.id):
        gc.attack(unit.id, enemy.id)
        #print('Mage is attack!')

def guard(gc, unit, nearfriends):
    if len(nearfriends) == 0:
        return
    gtarget = nearfriends[0]
    for f in nearfriends:
        if f.unit_type == bc.UnitType.Ranger:
            gtarget = f
            break
    followDir = Info.pathfind(unit,gtarget)
    if Info.roll(25):  #25 percent chance to move randomly instead of directly follow...this way it won't pin someone to a wall
        followDir = random.choice(Info.directions)
    if gc.is_move_ready(unit.id) and gc.can_move(unit.id, followDir):
        gc.move_robot(unit.id,followDir)




def mageAction(gc, u):
    if u.location.is_on_map():
        nearby_enemies = gc.sense_nearby_units_by_team(u.location.map_location(), u.vision_range, Info.get_enemy_team())
        nearby_attackable = gc.sense_nearby_units_by_team(u.location.map_location(), u.attack_range(), Info.get_enemy_team())
        nearby_friends = gc.sense_nearby_units_by_team(u.location.map_location(), u.vision_range, gc.team())
        nearby_rocket = gc.sense_nearby_units_by_type(u.location.map_location(), 2, bc.UnitType.Rocket)

        if gc.planet() == bc.Planet.Earth:
            if gc.round() > 600:
                if not len(nearby_rocket[0].structure_garrison()) == 8: #if not board_rocket(u, nearby_rocket):
                    run_toward_rocket(u, nearby_rocket)

            if len(nearby_attackable) > 0:
                bad_guy = worst_enemy(u, nearby_attackable)
                battle(gc,u, bad_guy)
            #elif len(nearby_enemies) > 0:
            #    bad_guy = closest_enemy(u, nearby_en)
            #    chase(u, bad_guy)
            #elif not board_rocket(u, nearby_rocket): #Dunno what this is supposed to do
            #    if len(fight_loc) > 0:
            #        pursue(u)
            else:
                guard(gc, u, nearby_friends)
        else:
            if len(nearby_attackable) > 0:
                bad_guy = worst_enemy(u, nearby_attackable)
                battle(gc, u, bad_guy)
            #elif len(nearby_enemies) > 0:
            #    bad_guy = closest_enemy(u, nearby_en)
            #    chase(u, bad_guy)
            #elif len(fight_loc) > 0:
            #    pursue(u)
            else:
                guard(gc, u, nearby_friends)

#def mageAction(gc, unit):
