# a box of handy shortcut methods to make coding unit AI easier

import random


# tells unit which way to walk to get closer to target
# returns a direction
def pathfind(bc, unit, target):
    # direction to walk in, should get changed below
    d = bc.Direction.Center 
                
    ourX = unit.location.map_location().x
    ourY = unit.location.map_location().y
    otherX = target.location.map_location().x
    otherY = target.location.map_location().y

    # if distanceX is negative, the enemy is to the west
    distanceX = ourX - otherX
    # if distanceY is negative, the enemy is to the south
    distanceY = ourY - otherY 

    # determine which direction is best to move in
    # 'abs()' returns the absolute value of a number
    if abs(distanceX) > abs(distanceY):
        if distanceX < 0:
            d = bc.Direction.West
        else:
            d = bc.Direction.East
    elif distanceY < 0:
        d = bc.Direction.South
    else:
        d = bc.Direction.North

    return d

# return a random direction
def pathrand(bc):
    return random.choice(list(bc.Direction))

# is other unit an enemy?
# returns true if other is an enemy
def enemy(gc, other):
    return other.team != gc.team()

# does our unit have low health?
# returns true if health is below 20%
def lowHealth(unit):
   return unit.health < (unit.max_health / 5)
