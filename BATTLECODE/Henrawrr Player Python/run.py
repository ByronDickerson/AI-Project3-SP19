import battlecode as bc
import random
import sys
import traceback
import time
import random
from random import randint
import os
from gaussian_blur import GaussianBlur
from worker_harvest import HarvestStrategy
from mage import Mage
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
random.seed(6137)

# let's start off with some research!
# we can queue as much as we want.

gc.queue_research(bc.UnitType.Knight)
gc.queue_research(bc.UnitType.Rocket)
#gc.queue_research(bc.UnitType.Ranger)
gc.queue_research(bc.UnitType.Worker)


my_team = gc.team()
gb = GaussianBlur(gc)
gd = gb.get_gauss()
rocket_id = -1
unit_rocket = 0
while True:
    # We only support Python 3, which means brackets around print()
    ###print('pyround:', gc.round(), 'time left:', gc.get_time_left_ms(), 'karbonite:', gc.karbonite(), 'ms')

    # frequent try/catches are a good idea
    try:
        # walk through our units:
        for unit in gc.my_units():
            move = 0;
            # first, factory logic
            if unit.unit_type == bc.UnitType.Factory:
                garrison = unit.structure_garrison()
                x = randint(1,10)
                if len(garrison) > 0:
                    d = random.choice(directions)
                    if gc.can_unload(unit.id, d):
                        print('unloaded a knight!')
                        gc.unload(unit.id, d)
                        continue
                elif gc.can_produce_robot(unit.id, bc.UnitType.Knight):
                    gc.produce_robot(unit.id, bc.UnitType.Knight)
                    print('produced a knight!')
                    continue
                if gc.can_produce_robot(unit.id, bc.UnitType.Mage):
                    gc.produce_robot(unit.id, bc.UnitType.Mage)
                    print('produced a mage!')
                    continue
                #elif x > 3 and gc.can_produce_robot(unit.id, bc.UnitType.Ranger):
                #    gc.produce_robot(unit.id, bc.UnitType.Ranger)
                #    print('produced a ranger!')
                #    continue
            if unit.unit_type == bc.UnitType.Worker:
                for x in directions:
                    if gc.can_harvest(unit.id, x):
                        gc.harvest(unit.id, x)
                        continue
                    if gc.round() < 10 and gc.can_replicate(unit.id, x):
                        gc.replicate(unit.id, x)
                        continue
                if(random.random() < 0.5):
                    hs = HarvestStrategy(bc,gc,gd,unit)
                    hs.move()

            if unit.unit_type == bc.UnitType.Mage:
                # for x in directions: #random movement for now
                #     if gc.is_move_ready(unit.id) and gc.can_move(unit.id, x) and move == 0:
                #         gc.move_robot(unit.id, x)
                m = Mage(gc, unit)
                if unit.location.is_in_garrison() == False:
                    m.target()


            # first, let's look for nearby blueprints to work on
            location = unit.location
            if location.is_on_map():
                nearby = gc.sense_nearby_units(location.map_location(), 1000)
                #m = MapLocation
                for other in nearby:
                    if unit.unit_type == bc.UnitType.Worker and gc.can_build(unit.id, other.id):
                        gc.build(unit.id, other.id)
                        move = 1;
                        # print('built a factory!')
                        print(other.unit_type)
                        if(other.unit_type == bc.UnitType.Rocket):
                            rocket_id = other.id
                        # move onto the next unit

                    if other.team != my_team and unit.unit_type == bc.UnitType.Knight and gc.is_attack_ready(unit.id):
                        if gc.can_attack(unit.id, other.id):
                            print('attacked a thing!')
                            gc.attack(unit.id, other.id)
                    if(rocket_id != -1):
                        if(other.unit_type == bc.UnitType.Worker and gc.can_load(rocket_id,other.id)):
                            unit_rocket+=1
                            gc.load(rocket_id,other.id)

            if((gc.round() > 700 or unit_rocket > 3) and unit.unit_type == bc.UnitType.Rocket):
                mapp = gc.starting_map(bc.Planet(1))
                for x in range(0,self.mapp.height):
                    for y in range(0,self.map.width):
                        if(gc.can_launch_rocket(unit.id,bc.MapLocation(bc.Planet(1),y,x))):
                            gc.launch_rocket(unit.id,bc.MapLocation(bc.Planet(1),y,x))





                        #elif gc.is_move_ready(unit.id) and gc.can_move(unit.id, .direction_to(other.location.map_location())):
                        #    print('moving unit')
                        #    gc.move_robot(unit.id. d)
                        #    gc.move_robot(unit.id, gc.direction_to(other.location.map_location()))


            #print(str(gc.karbonite))
            # okay, there weren't any dudes around
            # pick a random direction:
            d = random.choice(directions)

            # or, try to build a factory:
            if gc.karbonite() > bc.UnitType.Factory.blueprint_cost() and gc.can_blueprint(unit.id, bc.UnitType.Factory, d):
                gc.blueprint(unit.id, bc.UnitType.Factory, d)
            elif gc.round() > 200 and gc.karbonite() > bc.UnitType.Rocket.blueprint_cost() and gc.can_blueprint(unit.id, bc.UnitType.Rocket, d):
               gc.blueprint(unit.id, bc.UnitType.Rocket, d)

            # and if that fails, try to move
            elif gc.is_move_ready(unit.id) and gc.can_move(unit.id, d) and move == 0:
                gc.move_robot(unit.id, d)

            # if(gc.round() > 200):
            #     if(gc.can_launch)

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
