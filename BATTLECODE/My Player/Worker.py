#The info file was inspired from Slink3's extra info.py
import battlecode as bc
import MyInfo

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
def workerLogic(gc, unit):

    #The worker will prioritize building
    #Then attacking
    #THen gathering resources
    #Then replicating
    #Then wandering around

    directions = list(bc.Direction)
    #curD = random.choice(directions)
    
    location = unit.location
    if location.is_on_map():
        nearby = gc.sense_nearby_units(location.map_location(), 2)
        for other in nearby:
            if unit.unit_type == bc.UnitType.Worker and gc.can_build(unit.id, other.id):
                gc.build(unit.id, other.id)
                print('built a factory!')
                # move onto the next unit
                continue
            if other.team != gc.team() and gc.is_attack_ready(unit.id) and gc.can_attack(unit.id, other.id):
                print('attacked a thing!')
                gc.attack(unit.id, other.id)
                continue

                
    for d in directions:
        if gc.can_harvest(unit.id, d):
            gc.harvest(unit.id, d)
            return
    
    for d in directions:
        if gc.can_replicate(unit.id, d) and MyInfo.getNumUnits(bc.UnitType.Worker, gc) < 10:
            gc.replicate(unit.id, d)
            # a child is born. we should initialize it as a Worker class. but...for now...whatever man


    if MyInfo.getNumUnits(bc.UnitType.Rocket, gc) < 2 and gc.karbonite() > bc.UnitType.Rocket.blueprint_cost() and gc.can_blueprint(unit.id, bc.UnitType.Rocket, d):
        try:
            gc.build(unit.id, rocket_id)
            print("building Rocket!")
        except Exception as e:
            print('Error:', e)
            # use this to show where the error was
            traceback.print_exc()

        gc.blueprint(unit.id, bc.UnitType.Rocket, d)
        print('built a rocket!')
        # move onto the next unit

    for d in directions:
        if gc.is_move_ready(unit.id) and gc.can_move(unit.id, d):
            gc.move_robot(unit.id, d)
            continue

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

