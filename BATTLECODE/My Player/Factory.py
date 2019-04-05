import battlecode as bc
import random
import MyInfo

possibleDirections = list(bc.Direction)


def factoryLogic(unit, gc):
    counter = [1, 2, 3]
    count = random.choice(counter)

    #if it's not built then chillax
    if not unit.structure_is_built():
        #print('Build status is ', str(unit.health), 'out of 300 health')
        return

    # Try to unload existing units from structure's garrison
    for direction in possibleDirections:
        if gc.can_unload(unit.id, direction):
            gc.unload(unit.id, direction)
            #print(unit.id, " Factory just unloaded a..something ")
            return
    #up until round 675 we will produce random bots
    if gc.round()<675:
        if count==1 and MyInfo.getNumUnits(bc.UnitType.Knight, gc)< 15:
            if gc.can_produce_robot(unit.id, bc.UnitType.Knight):
                gc.produce_robot(unit.id, bc.UnitType.Knight)
                #print(unit.id, " Factory making a knight ")
                return

        elif count==2 and MyInfo.getNumUnits(bc.UnitType.Ranger, gc)< 10:
            if gc.can_produce_robot(unit.id, bc.UnitType.Ranger): 
                gc.produce_robot(unit.id, bc.UnitType.Ranger)
                #print(unit.id, " Factory making a ranger ")
                return

        elif count==3 and MyInfo.getNumUnits(bc.UnitType.Healer, gc)< 10:
            if gc.can_produce_robot(unit.id, bc.UnitType.Healer):
                gc.produce_robot(unit.id, bc.UnitType.Healer)
                #print(unit.id, " Factory making a healer ")
                return
    return
