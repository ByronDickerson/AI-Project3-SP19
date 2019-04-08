def runRangerLogic(unit, unitInfo, mapInfo, gc):
    # If ranger is in garrison or space, then do nothing
    if not unit.location.is_on_map():
        return

    if unit.ranger_is_sniping():
        return

    # Current location of the unit
    unitLocation = unit.location.map_location()

    if not gc.is_attack_ready(unit.id):
        if not gc.is_move_ready(unit.id):
            return

        if unit.location.map_location().planet == bc.Planet.Earth:
            FriendlyUnitLocation = findFriendlyUnitLocation(gc, unit, unitInfo.earthFriendlyUnitsLocation)
        else:
            FriendlyUnitLocation = findFriendlyUnitLocation(gc, unit, unitInfo.marsFriendlyUnitsLocation)

        if not FriendlyUnitLocation is None:
            direction = unitLocation.direction_to(FriendlyUnitLocation)
            if gc.is_move_ready(unit.id):
                if gc.can_move(unit.id, direction):
                    #gc.move_robot(unit.id, direction)
                    move.goto(gc, unit.id, unitLocation.add(direction))
                    return
        return

    # Randomize array of directions each turn
    randomDirections = move.directions
    random.shuffle(randomDirections)

    # Attack the closest units
    nearbyEnemyUnits = gc.sense_nearby_units_by_team(unitLocation, unit.attack_range(), unitInfo.enemyTeam)
    for nearbyEnemyUnit in nearbyEnemyUnits:
        if gc.can_attack(unit.id, nearbyEnemyUnit.id):
            gc.attack(unit.id, nearbyEnemyUnit.id)
            return
    
    # If there are enemy units in ability range, then try to snipe them
    if unit.is_ability_unlocked():
        if gc.is_begin_snipe_ready(unit.id):
            if unit.location.map_location().planet == bc.Planet.Earth:
                visibleEnemyUnitsLocation = unitInfo.earthVisibleEnemyUnitsLocation
            else:
                visibleEnemyUnitsLocation = unitInfo.marsVisibleEnemyUnitsLocation

            for eachEnemyUnitLocation in visibleEnemyUnitsLocation:
                '''
                # Snipe only knights, rangers and mages
                if eachEnemyUnitLocation.unit_type == bc.UnitType.Worker or eachEnemyUnitLocation.unit_type == bc.UnitType.Rocket or eachEnemyUnitLocation.unit_type == bc.UnitType.Factory:
                    break
                '''
                if gc.can_begin_snipe(unit.id, eachEnemyUnitLocation):
                    gc.begin_snipe(unit.id, eachEnemyUnitLocation)
                    return

    '''
    visibleEnemyUnits = gc.sense_nearby_units_by_team(unitLocation, unit.vision_range, unitInfo.enemyTeam)
    for visibleEnemyUnit in visibleEnemyUnits:
        # If there are visible enemy units nearby, then try to move closer to them
        direction = unitLocation.direction_to(visibleEnemyUnit.location.map_location())
        if gc.is_move_ready(unit.id):
            if gc.can_move(unit.id, direction):
                #gc.move_robot(unit.id, direction)
                move.goto(gc, unit.id, unitLocation.add(direction))
                return
    '''
        
    if not gc.is_move_ready(unit.id):
        return

    # Try to move to closest enemyUnit
    if unit.location.map_location().planet == bc.Planet.Earth:
        EnemyUnitLocation = findEnemyUnitLocation(gc, unit, unitInfo.earthVisibleEnemyUnitsLocation)
    else:
        EnemyUnitLocation = findEnemyUnitLocation(gc, unit, unitInfo.marsVisibleEnemyUnitsLocation)

    if not EnemyUnitLocation is None:
        direction = unitLocation.direction_to(EnemyUnitLocation)
        if gc.can_move(unit.id, direction):
            #gc.move_robot(unit.id, direction)
            move.goto(gc, unit.id, unitLocation.add(direction))
            return

    # Try to move to starting enemy location
    for startingEnemyLocation in mapInfo.startingEnemyLocations:
        direction = unitLocation.direction_to(startingEnemyLocation)
        if gc.can_move(unit.id, direction):
            #gc.move_robot(unit.id, direction)
            move.goto(gc, unit.id, unitLocation.add(direction))
            return

    # Move randomly
    for direction in randomDirections:
        if gc.can_move(unit.id, direction):
            #gc.move_robot(unit.id, direction)
            move.goto(gc, unit.id, unitLocation.add(direction))
            return

    return
