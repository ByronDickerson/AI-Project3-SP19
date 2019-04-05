import battlecode as bc
import random
import MyInfo

def rocketLogic(rocket, gc):

    # If building, do nothing
    # if full, or almost out of time, then launch
    # if on mars, unload
    # if on mars and empty? perish
    
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
        
        return
    
    rocketLoc = rocket.location.map_location()
    
    #otherwise, load some boys. 
    #rocket chooses who to load; it takes priority
    nearby = nearby = gc.sense_nearby_units(rocketLoc, 2)
    for other in nearby:
        if gc.can_load(rocket.id,other.id):
            gc.load(rocket.id, other.id)
            print(rocket.id,'Rocket slurped a fellow',other.unit_type)
            return
    #from TKUS
    
    if rocket.location.map_location().planet == bc.Planet.Mars:
        print('Am On Mars')
        for d in MyInfo.directions:
            if occupants > 0 and gc.can_unload(rocket.id, d):
                gc.unload(rocket.id, d)
                print('Rocket unloaded someone onto mars!')
                return                
        if occupants == 0: #empty and on mars is just useless, an obstacle for other rockets. so perish
            gc.disintegrate_unit(rocket.id)
            print('It was an honor being a rocket. occupants =', occupants)
            return
    if gc.round() % 50 == 0:
        print(rocket.id, ':',rocket.location.map_location().planet) #only print every 50 rds
        
    
#helper to rocket
#copied entirely from the skid3 guy or whatever the name is
def launch(gc, marsMap, unitId):
    if gc.unit(unitId).structure_is_built():
        this_rocket = gc.unit(unitId)
    else:
        return
    garrison = this_rocket.structure_garrison()


    #destination = computeOptimalLandingPlace(marsMap)
    destination = bc.MapLocation(bc.Planet.Mars, random.randint(5, marsMap.width-5), random.randint(5, marsMap.height-5))
    try:
        while not marsMap.is_passable_terrain_at(destination):
            destination = bc.MapLocation(bc.Planet.Mars, random.randint(5, marsMap.width-5), random.randint(5, marsMap.height-5))
        if gc.can_launch_rocket(this_rocket.id, destination):
            gc.launch_rocket(this_rocket.id, destination)
            print('Launching rocket with occupants:', len(garrison))
    except Exception as e:
        print('Uh Oh:', e)
        print('Invalid destination is ', destination)
        print('mars size is ',marsMap.width, 'x',marsMap.height)


#sense nearby unbuilt things and then work on that
def workerTryBuilding(gc, u ):
    if u.location.is_on_map():
        nearby = gc.sense_nearby_units(u.location.map_location(), 2)
        for other in nearby:
            if other.team == gc.team() and other.unit_type == bc.UnitType.Factory or other.unit_type == bc.UnitType.Rocket:
                #print(worker.ID, ' is near a structure ',other.id)
                if not other.structure_is_built() and gc.can_build(u.id,other.id):
                    gc.build(u.id, other.id)
                    #print(u.id, ' Am still building this', other.unit_type)
                    return True
                else:
                    return False
                    

def workerLogic(gc, worker):
    directions = MyInfo.directions
    location = worker.location #does this work?
    my_team = gc.team()

    #The worker will prioritize building
    #Then attacking
    #THen gathering resources
    #Then replicating
    #Then wandering around
    if workerTryBuilding(gc, worker):
        return 

    #up to 5 factories i guess
    #try to blueprint

    if MyInfo.getNumUnits(bc.UnitType.Rocket, gc) < 1:
        blueprint(worker, directions, location, bc.UnitType.Rocket, gc)

    if MyInfo.getNumUnits(bc.UnitType.Factory, gc) < 5:
        blueprint(worker,directions,location,bc.UnitType.Factory, gc)
    


    

    #attack nearby enemy
    #should probably have it flee but that is much harder to computer
    if location.is_on_map():
        nearby = gc.sense_nearby_units(location.map_location(), 2)
        for other in nearby:
            if other.team != my_team and gc.is_attack_ready(worker.id) and gc.can_attack(worker.id, other.id):
                #print(worker.id, ' is attacking ',other.id)
                gc.attack(worker.id, other.id)
                
                return
                
   
    
    for d in directions:
        if gc.can_harvest(worker.id, d):
            gc.harvest(worker.id, d)
            #print(worker.ID, ' Am harvesting stuff ')
            return
    
    #wwhere 10 is the max number of workers
    if MyInfo.getNumUnits(bc.UnitType.Worker,gc) < 10:
        for d in directions:
            if gc.can_replicate(worker.id, d):
                #print(worker.id, ' Am replicating ')
                #print('Number of workers is', MyInfo.getNumUnits(bc.UnitType.Worker, gc))
                gc.replicate(worker.id, d)
                return
            # a child is born. we should initialize it as a Worker class. but...for now...whatever man
    
    dr = random.choice(directions)
    #last but not least, random walk
    trymove(gc,worker.id, dr)
    return


#custom move function for clarity. completely unnecessary but whatver
def trymove(gc, id, dir):
    if gc.is_move_ready(id) and gc.can_move(id, dir):
        gc.move_robot(id,dir)

def blueprint(worker,directions,location,utype, gc):
    for d in directions:
            if gc.can_blueprint(worker.id, utype,d):
                gc.blueprint(worker.id, utype,d)
                return
