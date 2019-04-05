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
                
    directions = list(bc.Direction)
    #d = random.choice(directions)
    
    for d in directions:
        if gc.can_harvest(unit.id, d):
            gc.harvest(unit.id, d)
            return
    
    for d in directions:
        if gc.can_replicate(unit.id, d) and MyInfo.getNumUnits(bc.UnitType.Worker, gc) < 10:
            gc.replicate(unit.id, d)
            # a child is born. we should initialize it as a Worker class. but...for now...whatever man
    
    #check if we can blueprint...then...do it..
    #this method doesnt exist yet. but it should handle like do we need one, do we have the funds, etc
    '''
    if info.isRocketBlueprintTime():
        blueprint(worker,directions,location,bc.UnitType.Rocket)
        return
        
    if info.isFactoryBlueprintTime():
        blueprint(worker,directions,location,utype)
        return
    '''    
    
    
def blueprint(worker,directions,location,utype):
    for d in directions:
            if gc.can_blueprint(worker.id, utype,d):
                gc.blueprint(worker.id, utype,d)
                for u in gc.sense_nearby_units(location.map_location()):
                    if u.unit_type == utype:
                        worker.newBuildTarget(u)
                return
