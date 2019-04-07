import battlecode as bc
import random
import Info

def healerLogic(unit, gc)
    #find nearby teammates
    team = Info.neabyTeam(unit, gc)
    
    # If unit is not on map, then do nothing
    if not unit.location.is_on_map():
        return
