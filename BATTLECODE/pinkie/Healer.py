import battlecode as bc
import random
import Info

def healerLogic(unit, gc):
    directions = list(bc.Direction)
    # If unit is not on map, then do nothing
    if not unit.location.is_on_map():
        return

    #check for enemies
    enemies = []
    
    if unit.team == bc.Team.Red:
        nearbyEnemies = gc.sense_nearby_units_by_team(unit.location.map_location(), 5, bc.Team.Blue)
    else:
        nearbyEnemies = gc.sense_nearby_units_by_team(unit.location.map_location(), 5, bc.Team.Red)

    #Healer should runaway from enemies
    if len(enemies) > 0:
        for e in enemies:
            d = Info.pathfind(unit, e)
            if d == bc.Direction.North:
                d == bc.Direction.South
                
            elif d == bc.Direction.South:
                d == bc.Direction.North
                
            elif d == bc.Direction.East:
                d == bc.Direction.West
                
            elif d == bc.Direction.West:
                d == bc.Direction.East
                
            if gc.can_move(unit.id, d):
                print("Healer Flees!")
                gc.move_robot(unit.id, d)

        
    #find nearby teammates
    teamAbility = Info.nearbyTeamAbility(unit, gc)
    team = Info.nearbyTeam(unit, gc)
    nearDeath = unit #just to set it as the same type
    for t in team:
        if Info.lowHealth(t) and t.health < nearDeath.health:
            nearDeath = t

    if gc.can_heal(unit.id, nearDeath.id) and gc.is_heal_ready(unit.id) and not nearDeath.id == unit.id:
        gc.heal(unit.id, nearDeath.id)
        print("Healed an ally!")

    highHeat = unit #just to set typying
    for t in team:
        if t.unit_type != bc.UnitType.Rocket and t.unit_type != bc.UnitType.Factory:
            if t.ability_cooldown() > highHeat.ability_cooldown():
                if t.attack_cooldown() > highHeat.attack_cooldown() and t.ability_cooldown() > highHeat.ability_cooldown():
                    highHeat = t
                highHeat = t

    if gc.can_overcharge(unit.id, t.id) and gc.is_overcharge_ready(unit.id):
        gc.overcharge(unit.id, t.id)
    
