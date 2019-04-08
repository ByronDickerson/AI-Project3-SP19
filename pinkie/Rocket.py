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
        launch(gc, rocket.id)
        
        return
    
    # If situation is dire, just launch
    if occupants > 0 and situation_is_dire(gc, rocket):
        launch(gc, rocket.id)

    rocketLoc = rocket.location.map_location()
    
    #otherwise, load some boys. 
    #rocket chooses who to load; it takes priority
    nearby = gc.sense_nearby_units(rocketLoc, 2)
    for other in nearby:
        if gc.can_load(rocket.id,other.id) and not allSlurped(gc):
            gc.load(rocket.id, other.id)
            print(rocket.id,'Rocket slurped a fellow',other.unit_type)
            return
    #from TKUS

    #check if we have accidentally slurped every single person
    #If so, then unload
    #(Also 1 percent chance of this happening..just in case? i guess?)
    if Info.roll(1) or allSlurped(gc):
        for d in Info.directions:
            if gc.can_unload(rocket.id,d):
                gc.unload(rocket.id,d)
    
    ##if gc.round() % 50 == 0:
    #    print(rocket.id, ':',rocket.location.map_location().planet) #only print every 50 rds
        
def rocketMars(rocket, gc):
    occupants = len(rocket.structure_garrison())  
    #print('Am On Mars')
    for d in Info.directions:
        if occupants > 0 and gc.can_unload(rocket.id, d):
            gc.unload(rocket.id, d)
            print('Rocket unloaded someone onto mars!')
            return                
    if occupants == 0: #empty and on mars is just useless, an obstacle for other rockets. so perish
        gc.disintegrate_unit(rocket.id)
        print('It was an honor being a rocket. occupants =', occupants)
        return
    
#Check if everyone is in a rocket
#return false if even one person is not in garrison
def allSlurped(gc):
    for unit in gc.my_units():
        if not unit.location.is_in_garrison():
            return False
    return True


#helper to rocket
#copied entirely from the skid3 guy or whatever the name is
def launch(gc, unitId):
    marsMap =  gc.starting_map(bc.Planet.Mars)
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

#returns true or false
# A situation is dire if the rocket is overwhelmed by opposite team with few allies
def situation_is_dire(gc, rocket):
    if rocket.location.is_on_map():
        foes = gc.sense_nearby_units_by_team(rocket.location.map_location(), 25, Info.get_enemy_team(gc)) #is this radius valid? idk
        friends = gc.sense_nearby_units_by_team(rocket.location.map_location(), 25, gc.team())
        
        #this means 85 percent of nearby bots are enemies so remaining 15 will probably perish soon
        if len(foes) != 0 and len(friends) / len(foes) < 0.15:
            return True 
        return False
    