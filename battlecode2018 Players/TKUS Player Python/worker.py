import battlecode as bc
import random
import targetList
import helperFunctions

#Rocket Rules
#1. Rockets are the number one priority if you can build a rocket do it
#2. Do not build a rocket while there is a rocket that is still being garrisoned //if we have a shit ton of units this might need to be changed
#3. Rockets can hold up to 8 units
#4. Once a rocket has been launched you can build another rocket. 

#Factory Rules
#1. Factories are always the first thing to build
#2. Each team gets 10 Karbonite per round and a factory takes 5 rounds to build a robot. Unless we're mining deposits we should never have more than 3 factories
maxRockets = 1
maxFactories = 4
maxWorkers = 5

harvestTotal = 0

workerTargetList = targetList.targetList()


directions = list(bc.Direction)

karboniteLeft = True

def workerLogic(unit, gc, unitCounter, persistentMap):
    global currentRockets
    global currentFactories
    global distance
    global harvestTotal
    global karboniteLeft
    currentTarget = 0

    # print(workerTargetList)

    

    d = random.choice(directions)

    # ---------------------------------------------------#
    #             Build Decisions                        #
    # ---------------------------------------------------#
    if not unit.location.is_in_garrison():
        # creates a rocket
        if len(unitCounter.currentRockets) < maxRockets:
            #checks if you have enough karbonite and can built in the given location
            if gc.karbonite() > bc.UnitType.Rocket.blueprint_cost() and gc.can_blueprint(unit.id, bc.UnitType.Rocket, d):
                gc.blueprint(unit.id, bc.UnitType.Rocket, d)
        

        #create a factory
        if len(unitCounter.currentFactories) < maxFactories:
            #checks if you have enough karbonite and can built in the given location
            if gc.karbonite() > bc.UnitType.Factory.blueprint_cost() and gc.can_blueprint(unit.id, bc.UnitType.Factory, d):
                gc.blueprint(unit.id, bc.UnitType.Factory, d)

        # replicate a worker only if there are more factories than workers
        if len(unitCounter.currentWorkers) < len(unitCounter.currentFactories):
        #if True:
            if gc.can_replicate(unit.id, d):
                gc.replicate(unit.id, d)

                print(unit.id, "replicated")


        # ---------------------------------------------------#
        #             Work  Decisions                        #
        # ---------------------------------------------------#

        #build nearby factories and Rockets
        workerLoc = unit.location
        workerMapLoc = workerLoc.map_location()
        if workerLoc.is_on_map():
            #gets all nearby factories at the given location
            nearbyUnits = gc.sense_nearby_units(workerLoc.map_location(), 2)
            for i in nearbyUnits:
                if i.unit_type == bc.UnitType.Factory:
                    if gc.can_build(unit.id, i.id):
                        gc.build(unit.id, i.id)
                elif i.unit_type == bc.UnitType.Rocket:
                    if gc.can_build(unit.id, i.id):
                        gc.build(unit.id, i.id)
                    elif gc.can_load(i.id, unit.id):
                        gc.load(i.id, unit.id)
                        continue

        # check if there is any karbonite around to harvest
        if karboniteLeft:
            for i in directions:
                direction = directions[i]
                if gc.can_harvest(unit.id, direction):
                    gc.harvest(unit.id, direction)
                    harvestMapLoc = workerMapLoc.add(direction)
                    persistentMap.updateKarbonite(harvestMapLoc, unit.worker_harvest_amount())
                    harvestTotal += unit.worker_harvest_amount()
                    # print(harvestTotal, " harvested!")
                    break




        # ---------------------------------------------------#
        #             Move Decisions                         #
        # ---------------------------------------------------#

        # if you don't have anything better to do. Move.
        if gc.is_move_ready(unit.id):
            factoryTargeted = False
            rocketTargeted = False
            karboniteTargeted = False


            if workerTargetList.hasTarget(unit.id):
                currentTarget = isTargetValid(workerTargetList.getCurrentTarget(unit.id), unit.id, persistentMap)

            if not currentTarget:
                # if a factory needs to be built move towards it
                for i in range(len(unitCounter.currentFactories)):
                    thisFactory = unitCounter.currentFactories[i]
                    factoryLoc = thisFactory.location.map_location()
                    if thisFactory.health<thisFactory.max_health and not workerTargetList.targetAlreadyTaken(factoryLoc):
                        print("targeting Factory")
                        workerTargetList.addToList(unit.id,factoryLoc)
                        factoryTargeted = True

                # else if a rocket needs to build move towards it
                if not factoryTargeted:
                    for i in range(len(unitCounter.currentRockets)):
                        thisRocket = unitCounter.currentRockets[i]
                        rocketLoc = thisRocket.location.map_location()
                        if rocketLoc.planet == bc.Planet.Earth:
                            if thisRocket.structure_is_built and unit.location.planet == bc.Planet.Earth:
                                workerTargetList.addToList(unit.id, rocketLoc)
                            elif thisRocket.health<thisRocket.max_health and not workerTargetList.targetAlreadyTaken(rocketLoc):
                                print("targeting Rocket")
                                workerTargetList.addToList(unit.id, rocketLoc)
                        
            # locate closest karbonite deposit that still has karbonite in it
            
                
                if workerMapLoc.planet == bc.Planet.Earth and not rocketTargeted and karboniteLeft:
                    print("looking for karbonite")
                    distance = 100000
                    karboniteLeft = False
                    for x in range(len(persistentMap.earthMap)):
                        for y in range(len(persistentMap.earthMap[0])):
                            #check if there is karbonite at that location
                            if persistentMap.earthMap[x][y].karbonite > 0 and persistentMap.earthMap[x][y].passable:
                                #get distance to that location
                                karboniteLeft = True
                                currentLoc = bc.MapLocation(bc.Planet.Earth, x, y)
                                newDistance = workerMapLoc.distance_squared_to(currentLoc)
                                # print(newDistance, distance)
                                if newDistance < distance and not workerTargetList.targetAlreadyTaken(currentLoc):
                                    distance = newDistance
                                    workerTargetList.addToList(unit.id, currentLoc)
                                    karboniteTargeted = True
                                    print("targeting karbonite")
                                    if distance<2:
                                        print("karbonite is close ending loop") 
                                        break
                                        
                
                currentTarget = workerTargetList.getCurrentTarget(unit.id)

            if workerTargetList.hasTarget(unit.id):
                direction = workerMapLoc.direction_to(currentTarget)
            
                
                if gc.can_move(unit.id, direction):
                    print("moving towards", direction)
                    gc.move_robot(unit.id, direction) 

                elif gc.can_move(unit.id, d):
                    print("movement blocked - moving randomly")
                    gc.move_robot(unit.id, d)

            elif gc.can_move(unit.id, d):
                print("target not found - moving randomly")
                gc.move_robot(unit.id, d)

def isTargetValid(mapTarget, id, persistentMap):
    if mapTarget: 
        if not persistentMap.earthMap[mapTarget.x][mapTarget.y].karbonite > 0 or \
        not persistentMap.earthMap[mapTarget.x][mapTarget.y].passable:
            # invalid target
            workerTargetList.clearCurrentTarget(id)
            return 0
        
        else:
            return mapTarget
    else:
        return 0