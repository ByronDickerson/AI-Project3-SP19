import battlecode as bc
import random

directions = list(bc.Direction)

def healerLogic(unit, gc):
	d = random.choice(directions)

	if gc.is_move_ready(unit.id) and gc.can_move(unit.id, d):
        	gc.move_robot(unit.id, d)	