import battlecode as bc
import random
import sys
import traceback
import time

import MyInfo
import Factory
import MyRanger
import Worker
import knight

import os
print(os.getcwd())

# print("pystarting")


# A GameController is the main type that you talk to the game with.
# Its constructor will connect to a running game.
gc = bc.GameController()
directions = list(bc.Direction)

# print("pystarted")

# It's a good idea to try to keep your bots deterministic, to make debugging easier.
# determinism isn't required, but it means that the same things will happen in every thing you run,
# aside from turns taking slightly different amounts of time due to noise.
random.seed(6137)

# let's start off with some research!
# we can queue as much as we want.
gc.queue_research(bc.UnitType.Rocket)
gc.queue_research(bc.UnitType.Worker)
gc.queue_research(bc.UnitType.Ranger)
gc.queue_research(bc.UnitType.Knight)

my_team = gc.team()


while True:
    # We only support Python 3, which means brackets around print()
    ####print('pyround:', gc.round(), 'time left:', gc.get_time_left_ms(), 'ms')

    # frequent try/catches are a good idea
    try:
        # walk through our units:
        for unit in gc.my_units():

            # first, factory logic
            if unit.unit_type == bc.UnitType.Factory:
                Factory.factoryLogic(unit, gc)

            elif unit.unit_type == bc.UnitType.Ranger:
                MyRanger.rangerLogic(unit, gc)

            elif unit.unit_type == bc.UnitType.Worker:
                Worker.workerLogic(gc, unit)
            
            elif unit.unit_type == bc.UnitType.Knight:
                knight.knightAction(gc, unit)
                
            elif gc.is_move_ready(unit.id) and gc.can_move(unit.id, d):
                gc.move_robot(unit.id, d)
            # okay, there weren't any dudes around
            # pick a random direction:
            d = random.choice(directions)

            # or, try to build a factory:
            if gc.karbonite() > bc.UnitType.Factory.blueprint_cost() and gc.can_blueprint(unit.id, bc.UnitType.Factory, d):
                if MyInfo.getNumUnits(bc.UnitType.Factory, gc) < 10:
                    gc.blueprint(unit.id, bc.UnitType.Factory, d)
            # and if that fails, try to move
            

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
