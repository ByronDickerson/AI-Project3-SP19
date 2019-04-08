#https://github.com/AnPelec/Battlecode-2018/blob/master/Project%20Achilles/run.py
import battlecode as bc
import random

import Info



# run towards the given rocket... 
def run_toward_rocket(gc, unit, r):
    if r.unit_type == bc.UnitType.Rocket:
        dir = Info.pathfind(unit,r)
    trymove(gc, unit.id, dir)

# The enemy with the highest health is the biggest threat according to this guy
def worst_enemy(unit, enemies):
    top = enemies[0]
    for e in enemies:
        if e.health > top.health:
            top = e
    return e

# Fight the given enemy...by attacking...
def battle(gc,unit, enemy):
    if Info.enemy(enemy) and gc.is_attack_ready(unit.id) and gc.can_attack(unit.id, enemy.id):
        gc.attack(unit.id, enemy.id)
        #print('Mage is attack!')

#follow a friend and attack anything that gets close
# Prioritize ranger but guard anyone except structures 
def guard(gc, unit, nearfriends):
    if len(nearfriends) == 0:
        return
    gtarget = None
    targetoption2 = nearfriends[0]
    #check if anyone is a ranger
    for f in nearfriends:
        if f.unit_type == bc.UnitType.Ranger:
            gtarget = f
            break
        if f.unit_type == bc.UnitType.Knight: #second choice is knight
            gtarget = f
        if f.unit_type in [bc.UnitType.Worker, bc.UnitType.Mage, bc.UnitType.Healer]:
            targetoption2 = f
    if gtarget is not None: #aka we found a knight or ranger:
        followDir = Info.pathfind(unit,gtarget)
    else: #one of the other bots
        followDir = Info.pathfind(unit,targetoption2)

    #25 percent chance to move randomly instead of directly follow...this way it won't pin someone to a wall
    #this also happens if the only nearby friend is a structure, to avoid crowding
    if Info.roll(25) or targetoption2.unit_type in [bc.UnitType.Factory, bc.UnitType.Rocket]:  
        followDir = random.choice(Info.directions)
    trymove(gc, unit.id, followDir)

#custom move function for clarity. completely unnecessary but whatver
def trymove(gc, id, dir):
    if gc.is_move_ready(id) and gc.can_move(id, dir):
        gc.move_robot(id,dir)

# finds the closest robot out of the list you give it, which should be enemies.
def closest_enemy(u, enemies):
    if len(enemies) > 0:
        closest = enemies[0]
        for e in enemies:
            if Info.distancebetween(u,e) < Info.distancebetween(u,closest):
                closest = e
        return closest

#follow a foe
def chase(gc, u, enemy):
    d = Info.pathfind(u,enemy)
    trymove(gc, u.id, d)


# The main fucntion for mage
def mageAction(gc, u):
    if u.location.is_on_map():
        #sense friends and foes
        nearby_enemies = gc.sense_nearby_units_by_team(u.location.map_location(), u.vision_range, Info.get_enemy_team())
        nearby_attackable = gc.sense_nearby_units_by_team(u.location.map_location(), u.attack_range(), Info.get_enemy_team())
        nearby_friends = gc.sense_nearby_units_by_team(u.location.map_location(), u.vision_range, gc.team())
        nearby_rocket = gc.sense_nearby_units_by_type(u.location.map_location(), 2, bc.UnitType.Rocket)

        # if it's time to go...then go
        if gc.planet() == bc.Planet.Earth:
            if gc.round() > 600:
                for r in nearby_rocket: # if there are no nearby rockets then it just continues doin other stuff
                    #if len(r.structure_garrison()) < 8: # don't bother if it's already full
                    #actually run toward even if it is full, to defend it
                    run_toward_rocket(gc, u, r)
 
        # Otherwise battle the biggest threat
        if len(nearby_attackable) > 0:
            bad_guy = worst_enemy(u, nearby_attackable)
            battle(gc,u, bad_guy)

        # Chase down closest threat
        elif len(nearby_enemies) > 0:
            bad_guy = closest_enemy(u, nearby_enemies)
            chase(gc, u, bad_guy)
        
        else:
            # follow around a friend... if a foe approaches mage will attack because that takes priority
            guard(gc, u, nearby_friends)





'''

Extra stuff that isnt implemented!

'''
#dunno if we will use these but here they are

def blink_attack_mars(gc, unit):

    marsMap = gc.starting_map(bc.Planet.Mars)

    if not gc.is_blink_ready(unit.id):
        return
    if bc.ResearchInfo().get_level(bc.UnitType.Mage) < 4:
        return
        
    location = unit.location
    enemy_team = Info.get_enemy_team()
        
    possible_targets = gc.sense_nearby_units_by_team(location.map_location(), 2, enemy_team)
    if len(possible_targets) > 2:
        return
    
    i = random.randint(0, marsMap.height-1)
    j = random.randint(0, marsMap.width-1)

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

    earthMap = gc.starting_map(bc.Planet.Earth)

    if not gc.is_blink_ready(unit.id):
        return
    if bc.ResearchInfo().get_level(bc.UnitType.Mage) < 4:
        return
        
    location = unit.location
    enemy_team = Info.get_enemy_team()
    
    possible_targets = gc.sense_nearby_units_by_team(location.map_location(), 2, enemy_team)
    if len(possible_targets) > 2:
        return
    
    i = random.randint(0, earthMap.height-1)
    j = random.randint(0, earthMap.width-1)
    
    try:
        temp_location = bc.MapLocation(bc.Planet.Earth, i, j)
        if gc.can_blink(unit.id, temp_location):
            gc.blink(unit.id, temp_location)
            return
            
    except Exception as e:
        print('Error:', e)
        # use this to show where the error was
        #traceback.print_exc()