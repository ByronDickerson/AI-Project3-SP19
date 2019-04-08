import battlecode as bc
import random

directions = list(bc.Direction)
maxKnights = 10
maxMages = 5
maxRangers = 5
maxHealers = 5


def factoryLogic(unit, gc, unitCounter, persistentMap):
    currentResearch = gc.research_info()
    garrison = unit.structure_garrison()
    if len(garrison) > 0:
        d = random.choice(directions)
        if gc.can_unload(unit.id, d):
            print('unloaded a thing')
            gc.unload(unit.id, d)

    if len(unitCounter.currentWorkers)< 1:
        if gc.can_produce_robot(unit.id, bc.UnitType.Worker):
            try:
                gc.produce_robot(unit.id, bc.UnitType.Worker)
                print('produced a Worker!')
            except:
                print('Error producing a worker')
    elif len(unitCounter.currentKnights)<maxKnights:
        if gc.can_produce_robot(unit.id, bc.UnitType.Knight):
            try:
                gc.produce_robot(unit.id, bc.UnitType.Knight)
                print('produced a knight!')
            except:
                print('Error producing a knight')
    elif len(unitCounter.currentMages)<maxMages:
        if gc.can_produce_robot(unit.id, bc.UnitType.Mage):
            try:
                gc.produce_robot(unit.id, bc.UnitType.Mage)
                print('produced a Mage!')
            except:
                print('Error producing a Mage')
    elif len(unitCounter.currentRangers)<maxRangers:
        if gc.can_produce_robot(unit.id, bc.UnitType.Ranger):
            try:
                gc.produce_robot(unit.id, bc.UnitType.Ranger)
                print('produced a Ranger!')
            except:
                print('Error producing a Ranger')
    elif len(unitCounter.currentHealers)<maxHealers:
        if gc.can_produce_robot(unit.id, bc.UnitType.Healer):
            try:
                gc.produce_robot(unit.id, bc.UnitType.Healer)
                print('produced a Healer!')
            except:
                print('Error producing a Healer')

    