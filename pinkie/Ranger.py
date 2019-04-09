import battlecode as bc 
import Info

possibleDirections = list(bc.Direction)
unit = 0
gc = 0

def rangerMars(unitParam, gcParam):
    global unit 
    global gc
    unit = unitParam
    gc = gcParam
    
    # If ranger is in garrison or space, then do nothing
    if unit.location.is_in_garrison():
        return

    if unit.ranger_is_sniping():
        return

    #if nothing is ready do nothing
    if not gc.is_attack_ready(unit.id):
        if not gc.is_move_ready(unit.id):
            return

    if not gc.is_move_ready(unit.id):
        return
    
    #Current unit location
    unitLocation = unit.location.map_location()

    #If there is a known mars entity, attempt to snipe or regular shoot
    #if you cant do either of those then move towards it
    if Info.marsTarget is not None:
        enemy = Info.marsTarget
        if unit.is_ability_unlocked():
            if gc.is_begin_snipe_ready(unit.id):
                if gc.can_begin_snipe(unit.id, enemy.location.map_location()):
                    gc.begin_snipe(unit.id, enemy.location.map_location())
                    return
        
        elif gc.can_attack(unit.id, enemy.id) and gc.is_attack_ready(unit.id):
                gc.attack(unit.id, enemy.id)
        else:
            d = Info.pathfind(unit, enemy)
            trymove(gc, unit.id, d)

    #target immediate enemies
    if unit.team == bc.Team.Red:
        enemies = gc.sense_nearby_units_by_team(unit.location.map_location(), 2, bc.Team.Blue)
    else:
        enemies = gc.sense_nearby_units_by_team(unit.location.map_location(), 2, bc.Team.Red)

    if len(enemies) > 0:
        if Info.marsTarget is not None:
            Info.marsTarget = enemies[0]
        for e in enemies:
            if gc.can_attack(unit.id, e.id) and gc.is_attack_ready(unit.id):
                gc.attack(unit.id, e.id)
                return


    #Nearby Enemy Location
    enemies = Info.nearbyEnemiesAbility(unit, gc)
    
    #If there are enemies, attack
    if len(enemies)>0:
        for enemy in enemies:
           #try to snipe enemies
            if unit.is_ability_unlocked():
                if gc.is_begin_snipe_ready(unit.id):
                    if gc.can_begin_snipe(unit.id, enemy.location.map_location()):
                        gc.begin_snipe(unit.id, enemy.location.map_location())
                        return

    if gc.can_attack(unit.id, enemy.id) and gc.is_attack_ready(unit.id) :
        gc.attack(unit.id, enemy.id)
        print("A Ranger Attacked")
        
    elif gc.planet() == bc.Planet.Earth:
        if gc.round() > 600:
            nearby_rocket = gc.sense_nearby_units_by_type(unit.location.map_location(), 2, bc.UnitType.Rocket)
            for r in nearby_rocket: # if there are no nearby rockets then it just continues doin other stuff
                if len(r.structure_garrison()) < 8: # don't bother if it's already full
                #actually run toward even if it is full, to defend it
                    run_toward_rocket(gc, unit, r)

    else: # Move randomly
        d = Info.pathrand()
        if gc.can_move(unit.id, d):
            gc.move_robot(unit.id, d)
            return

#I used Slink3 and TKUS's ranger classes and tried to combine them into this
def rangerLogic(unitParam, gcParam):
    global unit
    global gc
    unit = unitParam
    gc = gcParam
    
    # If ranger is in garrison or space, then do nothing
    if unit.location.is_in_garrison():
        return

    if unit.ranger_is_sniping():
        return

    #if nothing is ready do nothing
    if not gc.is_attack_ready(unit.id):
        if not gc.is_move_ready(unit.id):
            return

    if not gc.is_move_ready(unit.id):
        return
    
    #Current unit location
    unitLocation = unit.location.map_location()


    #target immediate enemies
    if unit.team == bc.Team.Red:
        enemies = gc.sense_nearby_units_by_team(unit.location.map_location(), 2, bc.Team.Blue)
    else:
        enemies = gc.sense_nearby_units_by_team(unit.location.map_location(), 2, bc.Team.Red)

    if len(enemies) > 0:
        for e in enemies:
            if gc.can_attack(unit.id, e.id) and gc.is_attack_ready(unit.id):
                gc.attack(unit.id, e.id)


    #Nearby Enemy Location
    enemies = Info.nearbyEnemiesAbility(unit, gc)
    
    #If there are enemies, attack
    if len(enemies)>0:
        for enemy in enemies:
           #try to snipe enemies
            if unit.is_ability_unlocked():
                if gc.is_begin_snipe_ready(unit.id):
                    if gc.can_begin_snipe(unit.id, enemy.location.map_location()):
                        gc.begin_snipe(unit.id, enemy.location.map_location())
                        return

        if gc.can_attack(unit.id, enemy.id) and gc.is_attack_ready(unit.id) :
            gc.attack(unit.id, enemy.id)
            print("A Ranger Attacked")
        
    elif gc.planet() == bc.Planet.Earth:
        if gc.round() > 600:
            nearby_rocket = gc.sense_nearby_units_by_type(unit.location.map_location(), 2, bc.UnitType.Rocket)
            for r in nearby_rocket: # if there are no nearby rockets then it just continues doin other stuff
                #if len(r.structure_garrison()) < 8: # don't bother if it's already full
                #actually run toward even if it is full, to defend it
                run_toward_rocket(gc, unit, r)

    else: # Move randomly
        d = Info.pathrand()
        if gc.can_move(unit.id, d):
            gc.move_robot(unit.id, d)
            return

# run towards the given rocket... 
def run_toward_rocket(gc, unit, r):
    if r.unit_type == bc.UnitType.Rocket:
        dir = Info.pathfind(unit,r)
    trymove(gc, unit.id, dir)

#custom move function for clarity. completely unnecessary but whatver
def trymove(gc, id, dir):
    if gc.is_move_ready(id) and gc.can_move(id, dir):
        gc.move_robot(id,dir)
