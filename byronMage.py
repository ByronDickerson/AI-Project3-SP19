#https://github.com/AnPelec/Battlecode-2018/blob/master/Project%20Achilles/run.py
class MageClass(object):
	def blink_attack_mars(unit):
		if not gc.is_blink_ready(unit.id):
			return
		if bc.ResearchInfo().get_level(bc.UnitType.Mage) < 4:
			return
			
		location = unit.location
			
		possible_targets = sense_nearby_units_by_team(location.map_location(), 2, enemy_team)
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
				traceback.print_exc()

	def blink_attack_earth(unit):
		if not gc.is_blink_ready(unit.id):
			return
		if bc.ResearchInfo().get_level(bc.UnitType.Mage) < 4:
			return
			
		location = unit.location
		
		possible_targets = sense_nearby_units_by_team(location.map_location(), 2, enemy_team)
		if len(possible_targets) > 2:
			return
				
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
				traceback.print_exc()
