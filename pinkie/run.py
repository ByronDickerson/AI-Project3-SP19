import battlecode as bc
import random
import sys
import traceback
import time


import Info, Factory, Ranger, Worker, Knight, Rocket, Mage, Healer

import os
print(os.getcwd())

print("pystarting") 


# A GameController is the main type that you talk to the game with.
# Its constructor will connect to a running game.
gc = bc.GameController()
directions = list(bc.Direction)

print("pystarted")

# It's a good idea to try to keep your bots deterministic, to make debugging easier.
# determinism isn't required, but it means that the same things will happen in every thing you run,
# aside from turns taking slightly different amounts of time due to noise.
random.seed(6138)

# let's start off with some research!
# we can queue as much as we want.
for i in range(10):
    gc.queue_research(bc.UnitType.Rocket)
    gc.queue_research(bc.UnitType.Worker)
    gc.queue_research(bc.UnitType.Ranger)
    gc.queue_research(bc.UnitType.Knight)
    gc.queue_research(bc.UnitType.Healer)
    gc.queue_research(bc.UnitType.Mage)

my_team = gc.team()

while True:
    # We only support Python 3, which means brackets around print()
  ##### print('pyround:', gc.round(), 'time left:', gc.get_time_left_ms(), 'ms')

    # frequent try/catches are a good idea
    try:

        
        # walk through our units:
        for unit in gc.my_units():
            
            # first, factory logic
            if unit.unit_type == bc.UnitType.Factory:
                Factory.factoryLogic(unit, gc)

            if unit.unit_type == bc.UnitType.Ranger:
                Ranger.rangerLogic(unit, gc)

            if unit.unit_type == bc.UnitType.Worker:
                #worker = Factory.Worker(unit) #instantiate custom worker object
                if gc.planet() == bc.Planet.Mars:
                    Worker.workerMars(gc, unit)
                else:
                    Worker.workerLogic(gc, unit)
            
            if unit.unit_type == bc.UnitType.Rocket:
                #if rocket.location.map_location().planet == bc.Planet.Mars:
                if gc.planet() == bc.Planet.Mars:
                    Rocket.rocketMars(unit,gc)
                else:
                    Rocket.rocketLogic(unit, gc)
                    
            if unit.unit_type == bc.UnitType.Knight:
                Knight.knightAction(gc,unit)

            if unit.unit_type == bc.UnitType.Mage:
                if gc.planet() == bc.Planet.Earth:
                    Mage.mageAction(gc, unit)
                else:
                    Mage.mageActionMars(gc, unit)
            
            if unit.unit_type == bc.UnitType.Healer:
                Healer.healerLogic(unit, gc)
               
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
