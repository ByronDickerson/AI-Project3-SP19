import battlecode as bc
import random
import sys
import traceback
import time

import os
print(os.getcwd())

class Rocket:
    
    def __init__(self, id):
        self.id = id
        self.health = 0
        self.max_health = 200
    
    
class Worker:

    def __init__(self, id):
        self.id = id
    

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
gc.queue_research(bc.UnitType.Worker)
gc.queue_research(bc.UnitType.Knight)

my_team = gc.team()



rocket_count = 0
rocket_builder_id = 0
rocket_id = 0

teamrocket = []
teamscavenge = []
teambuildfactory = []
unassigned = []

for unit in gc.my_units():
    unassigned.append(unit)

class TeamRocket:
    builders = []
    def __init__(self, rocket,builder):
        self.rocket = rocket
        self.builders.append(builder)
        
        
def runWorker(worker, gc):
    # if you are in the middle of building a rocket, keep doing that







while True:
    # We only support Python 3, which means brackets around print()
    print('pyround:', gc.round(), 'time left:', gc.get_time_left_ms(), 'ms')

    # frequent try/catches are a good idea
    try:
        for unit in teamrocket:
            #rocket logic
            #while the rocket is being built, build it
            #once it's done being built...set a flag or something to get everyone in the rocket            
            
            if unit.unit_type == bc.UnitType.Rocket:
                rocket_id = unit.id
                print('I am a rocket! heehe!')
                print('My built status is...' + str((unit.structure_is_built())))
                print('health:' + str(unit.health) + ' out of ' + str(unit.max_health))
            
        for unit in teamscavenge:
            #workers and whatever
            
        for unit in teambuildfactory:
            #build...that...
            
        for unit in unassigned:
            #uhh assign em
            
            if type(unit) == Worker:
                
                d = random.choice(directions)
                if gc.is_move_ready(unit.id) and gc.can_move(unit.id, d):
                    gc.move_robot(1, d)
            
                
                
            
                
                
                
                
                
                
            
            # first, factory logic
            # If i am a factory...
            '''
            
            if unit.unit_type == bc.UnitType.Factory:
                #fetch the garrison (thing that holds other units)
                garrison = unit.structure_garrison()
                #if there's somebody in the garrison,
                if len(garrison) > 0:
                    #Choose a random direction. if that, works, then unload the unit.
                    d = random.choice(directions)
                    if gc.can_unload(unit.id, d):
                        print('didnt unloaded a knight!')
                        #gc.unload(unit.id, d) #params are my own ID, and the direction im unloading. we dunno what the unit is...
                        continue
                #If im empty and able to make a knight...do that.
                elif gc.can_produce_robot(unit.id, bc.UnitType.Knight):
                    #gc.produce_robot(unit.id, bc.UnitType.Knight)
                    print('didnt produced a knight!')
                    continue
            '''
            
            #Not a factory
            # first, let's look for nearby blueprints to work on
            location = unit.location
            if location.is_on_map(): #?? no doc for this...is it just a check for errors or actually logic?
                nearby = gc.sense_nearby_units(location.map_location(), 2) #also no doc for this function...
                for other in nearby: #if we sense units nearby..
                    #if im a worker then work on building whatever Im sensing
                    if unit.unit_type == bc.UnitType.Worker and gc.can_build(unit.id, other.id):
                        gc.build(unit.id, other.id)
                        print('built a ' + str(other.id))
                        # move onto the next unit
                        continue
                    #if its an enemy and I can attack, then attack.
                    if other.team != my_team and gc.is_attack_ready(unit.id) and gc.can_attack(unit.id, other.id):
                        print('attacked a thing!')
                        gc.attack(unit.id, other.id)
                        continue

            # okay, there weren't any dudes around
            # pick a random direction:
            d = random.choice(directions)

            # or, try to build a factory:
            #if gc.karbonite() > bc.UnitType.Factory.blueprint_cost() and gc.can_blueprint(unit.id, bc.UnitType.Factory, d):
            #    gc.blueprint(unit.id, bc.UnitType.Factory, d)
            # and if that fails, try to move
            if unit.id == rocket_builder_id:
                try:
                    gc.build(unit.id, rocket_id)
                except:
                    continue
                continue

            if rocket_count < 1 and gc.karbonite() > bc.UnitType.Rocket.blueprint_cost() and gc.can_blueprint(unit.id, bc.UnitType.Rocket, d):
                gc.blueprint(unit.id, bc.UnitType.Rocket, d)
                rocket_count += 1 #increment how many rockets we got...so we only build 1...
                rocket_builder_id = unit.id
                print('built a rocket!')
                # move onto the next unit
                continue
            elif gc.is_move_ready(unit.id) and gc.can_move(unit.id, d):
                gc.move_robot(unit.id, d)














            
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
    
    

    
    
    
    
    
    
    
    
    
