#https://github.com/w4v3s/battlecode2018/blob/master/run.py
def mage(u):
    if u.location.is_on_map():
        nearby_en = gc.sense_nearby_units_by_team(u.location.map_location(), u.vision_range, op_team)
        nearby_at = gc.sense_nearby_units_by_team(u.location.map_location(), u.attack_range(), op_team)
        nearby_fr = gc.sense_nearby_units_by_team(u.location.map_location(), u.vision_range, my_team)
        nearby_rocket = gc.sense_nearby_units_by_type(u.location.map_location(), 2, bc.UnitType.Rocket)

        if gc.planet() == bc.Planet.Earth:
            if gc.round() > 600:
                if not board_rocket(u, nearby_rocket):
                    run_toward_rocket(u)

            if len(nearby_at) > 0:
                bad_guy = worst_enemy(u, nearby_at)
                battle(u, bad_guy)
            elif len(nearby_en) > 0:
                bad_guy = closest_enemy(u, nearby_en)
                chase(u, bad_guy)
            elif not board_rocket(u, nearby_rocket):
                if len(fight_loc) > 0:
                    pursue(u)
                else:
                    guard(u, nearby_fr)
        else:
            if len(nearby_at) > 0:
                bad_guy = worst_enemy(u, nearby_at)
                battle(u, bad_guy)
            elif len(nearby_en) > 0:
                bad_guy = closest_enemy(u, nearby_en)
                chase(u, bad_guy)
            elif len(fight_loc) > 0:
                pursue(u)
            else:
                guard(u, nearby_fr)
