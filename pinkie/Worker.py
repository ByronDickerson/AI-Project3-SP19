import battlecode as bc
import random
import Info

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
                    
def workerMars(gc, worker):
    directions = Info.directions
    location = worker.location
    my_team = gc.team()

    
    #If somebody has sensed a rocket landing, run there.
    if Info.marsTarget is not None:
        d = Info.pathfind(worker, Info.marsTarget)
        trymove(gc, worker.id, d)
        return 

    # Search for threats (and attack if possible)
    if location.is_on_map():
        nearby = gc.sense_nearby_units(location.map_location(), 2)
        for other in nearby:
            if other.team != my_team and gc.is_attack_ready(worker.id) and gc.can_attack(worker.id, other.id):
                #print(worker.id, ' is attacking ',other.id)
                gc.attack(worker.id, other.id)
                Info.marsTarget = other
                return

    #just go absolutely nuts on replication
    for d in directions:
            if gc.can_replicate(worker.id, d):
                #print(worker.id, ' Am replicating ')
                #print('Number of workers is', Info.getNumUnits(bc.UnitType.Worker, gc))
                gc.replicate(worker.id, d)
                return

    # And finally, harvest.
    for d in directions:
        if gc.can_harvest(worker.id, d):
            gc.harvest(worker.id, d)
            #print(worker.ID, ' Am harvesting stuff ')
            return

def workerLogic(gc, worker):
    directions = Info.directions
    location = worker.location #does this work?
    my_team = gc.team()

    #The worker will prioritize building
    #Then replicating
    #Then attacking
    #THen gathering resources
    #Then wandering around
    if workerTryBuilding(gc, worker):
        return 

    #wwhere 10 is the max number of workers
    if Info.getNumUnits(bc.UnitType.Worker,gc) < 10:
        for d in directions:
            if gc.can_replicate(worker.id, d):
                #print(worker.id, ' Am replicating ')
                #print('Number of workers is', Info.getNumUnits(bc.UnitType.Worker, gc))
                gc.replicate(worker.id, d)
                return
            # a child is born. 
    #up to 5 factories i guess
    #try to blueprint

    if Info.getNumUnits(bc.UnitType.Rocket, gc) < 3:
        blueprint(worker, directions, location, bc.UnitType.Rocket, gc)

    if Info.getNumUnits(bc.UnitType.Factory, gc) < 5:
        blueprint(worker,directions,location,bc.UnitType.Factory, gc)
    
    #should probably have it flee but that is much harder to computer
    if location.is_on_map():
        nearby = gc.sense_nearby_units(location.map_location(), 2)
        for other in nearby:
            if other.team != my_team: #and gc.is_attack_ready(worker.id) and gc.can_attack(worker.id, other.id):
                #print(worker.id, ' is attacking ',other.id)
                runaway(gc, worker, other)
                return
    
    for d in directions:
        if gc.can_harvest(worker.id, d):
            gc.harvest(worker.id, d)
            #print(worker.ID, ' Am harvesting stuff ')
            return
    
    
    
    dr = random.choice(directions)
    #last but not least, random walk
    trymove(gc,worker.id, dr)
    return

def runaway(gc, worker, other):
    t = Info.pathfind(worker,other)
    go = t
    if t == bc.Direction.South:
        go = bc.Direction.North
    elif t == bc.Direction.North:
        go = bc.Direction.South
    elif t == bc.Direction.East:
        go = bc.Direction.West
    elif t == bc.Direction.West:
        go = bc.Direction.East
    trymove(gc, worker.id, go)

#custom move function for clarity. completely unnecessary but whatver
def trymove(gc, id, dir):
    if gc.is_move_ready(id) and gc.can_move(id, dir):
        gc.move_robot(id,dir)

def blueprint(worker,directions,location,utype, gc):
    for d in directions:
            if gc.can_blueprint(worker.id, utype,d):
                gc.blueprint(worker.id, utype,d)
                return
