import battlecode as bc
import random
import MyInfo

possibleDirections = list(bc.Direction)


def factoryLogic(unit, gc):
    counter = [1, 2, 3]
    count = random.choice(counter)
    if not unit.structure_is_built():
        return

    # Try to unload existing units from structure's garrison
    for direction in possibleDirections:
        if gc.can_unload(unit.id, direction):
            gc.unload(unit.id, direction)
            return

    if gc.round()<675:
        if count==1 and MyInfo.getNumUnits(bc.UnitType.Knight, gc)< 10:
            if gc.can_produce_robot(unit.id, bc.UnitType.Knight):
                gc.produce_robot(unit.id, bc.UnitType.Knight)
                return

        elif count==2 and MyInfo.getNumUnits(bc.UnitType.Ranger, gc)< 5:
            if gc.can_produce_robot(unit.id, bc.UnitType.Ranger): 
                gc.produce_robot(unit.id, bc.UnitType.Ranger)
                return

        elif count==3 and MyInfo.getNumUnits(bc.UnitType.Healer, gc)< 5:
            if gc.can_produce_robot(unit.id, bc.UnitType.Healer):
                gc.produce_robot(unit.id, bc.UnitType.Healer)
                return
    return
