import random
class HarvestStrategy:
    def __init__(self,bc,gc,gradient,unit):
        self.gradient = gradient
        self.bc = bc
        self.gc = gc
        self.unit = unit
        self.path = []
    def get_location(self):
        return (self.unit.location.map_location().y,self.unit.location.map_location().x)
    def get_map_location(self):
        return self.unit.location.map_location()

    def find_closest_to_gradient(self):
        min_loc = 0
        min_dist = 10000
        for i in range(0,len(self.gradient)):
            for j in range(0,len(self.gradient[i])):
                ml = bc.MapLocation(bc.Planet(0),j,i)
                d = ml.distance_squared_to(get_map_location())
                if(d < min_dist and self.gradient[i][j] > 0):
                    min_dist = d
                    min_loc = ml
        return min_loc
    def move(self):
        gc = self.gc
        loc = self.get_map_location()
        directions = list(self.bc.Direction)
        if(self.gradient[loc.y][loc.x] > 0):
            self.follow_gradient()
        else:
            while(True):
                d = random.choice(directions)
                if(gc.can_move(self.unit.id,d)):
                    if(gc.is_move_ready(self.unit.id)):
                        gc.move_robot(self.unit.id,d)
                    break

    def follow_gradient(self):
        gc = self.gc
        ml = self.get_map_location()
        directions = list(self.bc.Direction)
        maxx = -1
        maxx_dir = self.bc.Direction(0)
        for d in directions:
            if(gc.can_move(self.unit.id,d)):
                ad = ml.add(d)
                tst = self.gradient[ad.y][ad.x]
                if(tst > maxx):
                    maxx = tst
                    maxx_dir = d
                    print(tst)
        if(gc.is_move_ready(self.unit.id) and gc.can_move(self.unit.id,maxx_dir)):
            gc.move_robot(self.unit.id,maxx_dir)
