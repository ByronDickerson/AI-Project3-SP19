#The info file was inspired from Slink3's extra info.py
import battlecode as bc

gc = 0

directions = list(bc.Direction)


def getNumUnits(unitType, gcParam):
    global gc
    gc = gcParam

    numR = 0
    numK = 0
    numH = 0
    numF = 0
    numW = 0
    numRockets = 0

    for unit in gc.my_units():
        if unit.unit_type == bc.UnitType.Ranger:
            numR+= 1
        elif unit.unit_type == bc.UnitType.Knight:
            numK+= 1
        elif unit.unit_type == bc.UnitType.Healer:
            numH+= 1
        elif unit.unit_type == bc.UnitType.Factory:
            numF+= 1
        elif unit.unit_type == bc.UnitType.Rocket:
            numRockets+= 1
        elif unit.unit_type == bc.UnitType.Worker:
            numW+= 1


    if unitType == bc.UnitType.Ranger:
        return numR
    elif unitType == bc.UnitType.Knight:
        return numK
    elif unitType == bc.UnitType.Healer:
        return numH
    elif unitType == bc.UnitType.Factory:
        return numF
    elif unitType == bc.UnitType.Rocket:
        return numRockets
    elif unitType == bc.UnitType.Worker:
        return numW

def nearbyEnemies(unit, gcParam):
    gc = gcParam
    nearbyEnemies = []
    
    if unit.team == bc.Team.Red:
        #nearbyEnemies = gc.sense_nearby_units(unit.location.map_location(), unit.attack_range())
        nearbyEnemies = gc.sense_nearby_units_by_team(unit.location.map_location(), unit.attack_range(), bc.Team.Blue)
    else:
        #nearbyEnemies = gc.sense_nearby_units(unit.location.map_location(), unit.attack_range())
        nearbyEnemies = gc.sense_nearby_units_by_team(unit.location.map_location(), unit.attack_range(), bc.Team.Red)
    return nearbyEnemies

