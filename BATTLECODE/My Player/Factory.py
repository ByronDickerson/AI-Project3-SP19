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

#basically jsut to hold some paramebers to go by
class Worker:
    def __init__(self, id):
        self.ID = id
        self.isBuilding = False
        self.isImproved = False
        self.buildTargetID = None
        
    
    def newBuildTarget(self,tgt):
        self.buildTargetID = tgt.id
        self.isBuilding = True


#input 'worker' is of the type Worker as defined in this file.
def workerLogic(gc, worker, info):
    
    #The worker will prioritize building
    #Then attacking
    #THen gathering resources
    #Then replicating
    #Then wandering around
    if worker.isBuilding:
        if gc.can_build(worker.ID, worker.buildTargetID):
            gc.build(worker.ID, worker.buildTargetID)
            return
    
    location = worker.location
    my_team = gc.team()

    #attack nearby enemy
    #should probably have it flee but that is much harder to computer
    if location.is_on_map():
        nearby = gc.sense_nearby_units(location.map_location(), 2)
        for other in nearby:
            if other.team != my_team and gc.is_attack_ready(worker.ID) and gc.can_attack(worker.ID, other.id):
                print(worker.ID, 'attacking',other.id)
                gc.attack(worker.ID, other.id)
                return
                
    directions = list(bc.Direction)
    #d = random.choice(directions)
    
    for d in directions:
        if gc.can_harvest(worker.ID, d):
            gc.harvest(worker.ID, d)
            return
    
    for d in directions:
        if gc.can_replicate(worker.ID, d):
            gc.replicate(worker.ID, d)
            # a child is born. we should initialize it as a Worker class. but...for now...whatever man
    
    #check if we can blueprint...then...do it..
    #this method doesnt exist yet. but it should handle like do we need one, do we have the funds, etc
    
    if info.isRocketBlueprintTime():
        blueprint(worker,directions,location,bc.UnitType.Rocket)
        return
        
    if info.isFactoryBlueprintTime():
        blueprint(worker,directions,location,utype)
        return
        
    
    
    
    
def blueprint(worker,directions,location,utype):
    for d in directions:
            if gc.can_blueprint(worker.ID, utype,d):
                gc.blueprint(worker.ID, utype,d)
                for u in gc.sense_nearby_units(location.map_location()):
                    if u.unit_type == utype:
                        worker.newBuildTarget(u)
                return
    
    
    
    
    
    
    
    
    
    
    