import battlecode as bc
import random
import sys
import traceback
import mapArray
import unitCounter
import rocketMan
import factory
import worker
import knight
import ranger
import mage
import healer
import helperFunctions

print("pystarting")

# A GameController is the main type that you talk to the game with.
# Its constructor will connect to a running game.
gc = bc.GameController()
directions = list(bc.Direction)

print("pystarted")

# It's a good idea to try to keep your bots deterministic, to make debugging easier.
# determinism isn't required, but it means that the same things will happen in every thing you run,
# aside from turns taking slightly different amounts of time due to noise.
random.seed(6137)

# let's start off with some research!
# we can queue as much as we want.
gc.queue_research(bc.UnitType.Rocket)
gc.queue_research(bc.UnitType.Ranger)
gc.queue_research(bc.UnitType.Ranger)
gc.queue_research(bc.UnitType.Ranger)

my_team = gc.team()



# earth = gc.starting_map(bc.Planet.Earth)
# mars = gc.starting_map(bc.Planet.Mars)

persistentMap = mapArray.smartMap(gc,bc)
persistentMap.initializeMapArrays()
unitCounter = unitCounter.unitCounter()




# earthMap = [[0 for x in range(20)] for y in range(20)]



while True:
    # We only support Python 3, which means brackets around print()
    # print('pyround:', gc.round())
    # print('karboynite total:',gc.karbonite())
    
    # frequent try/catches are a good idea
    try:
        #reset unit counter and count units this code only executes once per turn
        unitCounter.resetCount()
        for unit in gc.units():
            if unit.unit_type == bc.UnitType.Factory:
                unitCounter.currentFactories.append(unit)
            elif unit.unit_type == bc.UnitType.Rocket:
                unitCounter.currentRockets.append(unit)
            elif unit.unit_type == bc.UnitType.Worker:
                unitCounter.currentWorkers.append(unit)
            elif unit.unit_type == bc.UnitType.Knight:
                unitCounter.currentKnights.append(unit)
            elif unit.unit_type == bc.UnitType.Mage:
                unitCounter.currentMages.append(unit)
            elif unit.unit_type == bc.UnitType.Ranger:
                unitCounter.currentRangers.append(unit)
            else:
                unitCounter.currentHealers.append(unit)

        quads = [0, 0, 0, 0] #quads[0] = quadrant 1, quads[1] = quadrant 2, etc

        # walk through our units:
        for unit in gc.my_units():

            mapHeight = 0
            mapWidth = 0

            #save the height and width of the map depending on which planet the unit is on
            if unit.location.is_on_planet(bc.Planet.Earth):
                mapHeight = gc.starting_map(bc.Planet.Earth).height
                mapWidth = gc.starting_map(bc.Planet.Earth).width
            else:
                mapHeight = gc.starting_map(bc.Planet.Mars).height
                mapWidth = gc.starting_map(bc.Planet.Mars).width
            
            #adds a number to the global quads variable based ono the units quad
            helperFunctions.addToQuad(quads, unit, mapWidth, mapHeight, gc)


            #factory logic
            if unit.unit_type == bc.UnitType.Factory:
                factory.factoryLogic(unit, gc, unitCounter, persistentMap)
                persistentMap.updateUnit(unit.location.map_location(), 'Factory', 'Friendly')

            #Rocket Logic
            if unit.unit_type == bc.UnitType.Rocket:
                rocketMan.handleRocket(unit, gc, persistentMap)
                persistentMap.updateUnit(unit.location.map_location(), 'Rocket', 'Friendly')

            #Worker logic
            elif unit.unit_type == bc.UnitType.Worker:
                worker.workerLogic(unit, gc, unitCounter, persistentMap)

            #knight logic
            elif unit.unit_type == bc.UnitType.Knight:
                knight.knightLogic(unit, quads, mapWidth, mapHeight, gc)

            #Ranger logic
            elif unit.unit_type == bc.UnitType.Ranger:
                ranger.rangerLogic(unit, gc)

            #Mage logic
            elif unit.unit_type == bc.UnitType.Mage:
                mage.mageLogic(unit, gc)

            #Healer Logic
            elif unit.unit_type == bc.UnitType.Healer:
                healer.healerLogic(unit, gc)





    except Exception as e:
        print('Error:', e)
        # use this to show where the error was
        traceback.print_exc()

    # send the actions we've performed, and wait for our next turn.
    gc.next_turn()

    # these lines are not strictly necessary, but it helps make the logs make more sense.
    # it forces everything we've written this turn to be written to the manager.
    sys.stdout.flush()
    sys.stderr.flush()