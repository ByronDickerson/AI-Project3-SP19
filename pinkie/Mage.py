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


def mage(gc, u):
    if u.location.is_on_map():
        nearby_en = gc.sense_nearby_units_by_team(u.location.map_location(), u.vision_range, op_team)
        nearby_at = gc.sense_nearby_units_by_team(u.location.map_location(), u.attack_range(), op_team)
        nearby_fr = gc.sense_nearby_units_by_team(u.location.map_location(), u.vision_range, my_team)
        nearby_rocket = gc.sense_nearby_units_by_type(u.location.map_location(), 2, bc.UnitType.Rocket)

        if gc.planet() == bc.Planet.Earth:
            if gc.round() > 600:
                if not board_rocket(u, nearby_rocket):
                    run_toward_rocket(u)

            if len(nearby_at) > 0:
                bad_guy = worst_enemy(u, nearby_at)
                battle(u, bad_guy)
            elif len(nearby_en) > 0:
                bad_guy = closest_enemy(u, nearby_en)
                chase(u, bad_guy)
            elif not board_rocket(u, nearby_rocket):
                if len(fight_loc) > 0:
                    pursue(u)
                else:
                    guard(u, nearby_fr)
        else:
            if len(nearby_at) > 0:
                bad_guy = worst_enemy(u, nearby_at)
                battle(u, bad_guy)
            elif len(nearby_en) > 0:
                bad_guy = closest_enemy(u, nearby_en)
                chase(u, bad_guy)
            elif len(fight_loc) > 0:
                pursue(u)
            else:
                guard(u, nearby_fr)

def mageAction(gc, unit):

	return