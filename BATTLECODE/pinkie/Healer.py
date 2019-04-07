import battlecode as bc
import random
import Info

def healerLogic(unit, gc)
    # If unit is not on map, then do nothing
    if not unit.location.is_on_map():
        return

    #find nearby teammates
    teamAbility = Info.nearbyTeamAbility(unit, gc)
    team = Info.nearbyTeam(unit, gc)
    nearDeath = unit #just to set it as the same type
    for t in team:
        if Info.lowHealth(t) and t.health < nearDeath.health:
            nearDeath = t

    if can_heal(unit.id, nearDeath.id) and is_heal_ready(unit.id, nearDeath.id):
        heal(unit.id, nearDeath.id)
        
