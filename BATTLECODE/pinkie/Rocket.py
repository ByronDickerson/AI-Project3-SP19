import battlecode as bc
import random
import Info

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
        for d in Info.directions:
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

