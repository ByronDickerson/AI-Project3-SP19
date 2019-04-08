import battlecode as bc
import random
import Info

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
        count = 4
        #otherwise make more units in this order:
        #(or maybe randomly?)
        #Ranger
        #Knight
        #Healer
        #Mage
        #if we are low on workers, make some
        nums = [Info.getNumUnits(bc.UnitType.Knight, gc), 
        Info.getNumUnits(bc.UnitType.Ranger, gc), 
        Info.getNumUnits(bc.UnitType.Healer, gc), 
        Info.getNumUnits(bc.UnitType.Mage, gc)]

        buildme_index = nums.index(min(nums))


        if Info.getNumUnits(bc.UnitType.Worker, gc) < 3:
            make(gc, unit,bc.UnitType.Worker)

        if buildme_index == 0 and nums[0] < Info.maxKnights:
                make(gc, unit, bc.UnitType.Knight)

        elif buildme_index == 1 and nums[1] < Info.maxRangers:
                make(gc, unit, bc.UnitType.Ranger)
        
        elif buildme_index == 2 and nums[2] < Info.maxHealers:
            make(gc, unit, bc.UnitType.Healer)

        elif buildme_index == 3 and nums[3] < Info.maxMages:
            make(gc, unit, bc.UnitType.Mage)

    return


def make(gc, factory, utype):
    if gc.can_produce_robot(factory.id, utype):
        gc.produce_robot(factory.id, utype)
        #print('Produced a ', utype)
        