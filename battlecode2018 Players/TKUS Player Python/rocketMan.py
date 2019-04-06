import battlecode as bc
import random
# This will handle everything that rockets need to do


directions = list(bc.Direction)
persistentMap = 0

directions = list(bc.Direction)

def handleRocket(unit, gc, persistentMapParam):
    global persistentMap
    persistentMap = persistentMapParam
    # print('trying to launch a rocket to marks', bc.MapLocation(bc.Planet.Mars, 0, 0))

    # if the rocket is on earth
    rocketLoc = unit.location.map_location()
    currentLocation = 'no location found'


    if rocketLoc.planet == bc.Planet.Earth:
        currentScore = 0

        for y in range(len(persistentMap.marsMap)):
            for x in range(len(persistentMap.marsMap[0])):
                if persistentMap.marsMap[x][y].passable:
                    testLoc = bc.MapLocation(bc.Planet.Mars, x, y)
                    testScore = countDeployDirections(testLoc)
                    #check nearby directions to see if this is the best place to land
                    if testScore > currentScore:
                        currentScore = testScore
                        currentLocation = testLoc
                    if currentScore >= 8:
                        break

        if gc.can_launch_rocket(unit.id, currentLocation) and len(unit.structure_garrison())>6:
            gc.launch_rocket(unit.id, currentLocation)
            persistentMap.updateUnit(currentLocation, 'Rocket', 'Friendly')
            print('Rocket Launched!')

    elif rocketLoc.planet == bc.Planet.Mars:
        garrison = unit.structure_garrison()
        d = random.choice(directions)
        if len(garrison) > 0:
            d = random.choice(directions)
            if gc.can_unload(unit.id, d):
                print('unloaded a thing')
                gc.unload(unit.id, d)
    
    return

def countDeployDirections(currentLoc):
    # the higher the score the better the location
    locationScore = 0
    for i in directions:
        testDirection = currentLoc.add(directions[i])
        if persistentMap.checkPassable(testDirection):
            locationScore+=1
    
    return locationScore
