import battlecode as bc
import random

possibleDirections = list(bc.Direction)


def factoryLogic(unit, gc):
   
    counter = [1, 2, 3]
    count = random.choice(counter)
    if not unit.structure_is_built():
        return

    # Try to unload existing units from structure's garrison
    for direction in possibleDirections:
        if gc.can_unload(unit.id, direction):
            gc.unload(unit.id, direction)
            return

    if gc.round()<675:
        if count==1:
            if gc.can_produce_robot(unit.id, bc.UnitType.Knight):
                gc.produce_robot(unit.id, bc.UnitType.Knight)
                return

        elif count==2:
            if gc.can_produce_robot(unit.id, bc.UnitType.Ranger): 
                gc.produce_robot(unit.id, bc.UnitType.Ranger)
                return

        elif count==3:
            if gc.can_produce_robot(unit.id, bc.UnitType.Ranger):
                gc.produce_robot(unit.id, bc.UnitType.Ranger)
                return
    return

def rocketLogic(rocket, gc, info):
    
    #if it isnt done being built then chill out
    if not rocket.structure_is_built():
        return
    
    #how many already in?
    occupants = len(rocket.structure_garrison())     
    
    #if its about to flood and we got some passengers...just go
    #also launch if you're full
    if (gc.round() >= 700 and occupants > 0) or (occupants == 8):
        #from slink3
        launch(gc, gc.starting_map(bc.Planet.Mars), rocket.id)
        
    else:
        #otherwise, load some boys. 
        #rocket chooses who to load; it takes priority
        nearby = nearby = gc.sense_nearby_units(location.map_location(), 2)
        for other in nearby:
            if gc.can_load(rocket.id,other.id):
                gc.load(rocket.id, other.id)
                return
    
#helper to rocket
#copied entirely from the skid3 guy or whatever the name is
def launch(gc, marsMap, unitId):
	if gc.unit(unitId).structure_is_built():
		this_rocket = gc.unit(unitId)
	else:
		return
	garrison = this_rocket.structure_garrison()

	#destination = computeOptimalLandingPlace(marsMap)
	destination = bc.MapLocation(bc.Planet.Mars, random.randint(0, marsMap.width), random.randint(0, marsMap.height))
	while(not marsMap.is_passable_terrain_at(destination)):
		destination = bc.MapLocation(bc.Planet.Mars, random.randint(0, marsMap.width), random.randint(0, marsMap.height))
	if gc.can_launch_rocket(this_rocket.id, destination):
		gc.launch_rocket(this_rocket.id, destination)

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    