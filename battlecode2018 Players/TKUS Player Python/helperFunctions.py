import battlecode as bc


def addToQuad(quads, unit, mapWidth, mapHeight, gc):
    
    location = unit.location
    
    #if a unit is in space, in the garrison, or is a knight it will skip them
    if not unit.location.is_in_garrison() and not unit.location.is_in_space() and unit.unit_type != bc.UnitType.Knight:
        x = unit.location.map_location().x
        y = unit.location.map_location().y
        if x < mapWidth/2:
            if y < mapHeight/2:
                quads[2] += 1
            else:
                quads[1] += 1
        else:
            if y < mapHeight/2:
                quads[3] += 1
            else:
                quads[0] += 1


def countDeployDirections(currentLoc):
    # the higher the score the better the location
    locationScore = 0
    for i in directions:
        testDirection = currentLoc.add(directions[i])
        if persistentMap.checkPassable(testDirection):
            locationScore+=1
    
    return locationScore