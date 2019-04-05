import battlecode as bc
import random
import sys
import traceback
import time
from random import randint
import os
print(os.getcwd())

class GaussianBlur:
    def __init__(self,gc):
        self.gc = gc
        p = bc.Planet
        self.map = gc.starting_map(bc.Planet(0))

    def get_gauss(self):
        print(self.map.width)
        # grid = [self.map.height()][self.map.width()]
        grid = [[0 for x in range(self.map.width)] for y in range(self.map.height)]
        # print(grid)
        for x in range(0,self.map.height):
            for y in range(0,self.map.width):
                b = self.gc.starting_map(bc.Planet(0))
                grid[x][y] = b.initial_karbonite_at(bc.MapLocation(bc.Planet(0),y,x))
        gauss = [[0 for x in range(self.map.width)] for y in range(self.map.height)]

        for r in range(1,len(grid)-1):
            for c in range(1,len(grid[r])-1):
                avg = int((grid[r][c] + grid[r-1][c] + grid[r+1][c] + grid[r-1][c-1] + grid[r+1][c+1] +grid[r][c-1] + grid[r][c+1] + grid[r-1][c+1] + grid[r+1][c-1])/9);
                gauss[r][c] = avg
        # for i in gauss:
        #     print(i)
        #     print()
        grid = gauss
        for r in range(1,len(grid)-1):
            for c in range(1,len(grid[r])-1):
                avg = int((grid[r][c] + grid[r-1][c] + grid[r+1][c] + grid[r-1][c-1] + grid[r+1][c+1] +grid[r][c-1] + grid[r][c+1] + grid[r-1][c+1] + grid[r+1][c-1])/9);
                gauss[r][c] = avg
        grid = gauss
        for r in range(1,len(grid)-1):
            for c in range(1,len(grid[r])-1):
                avg = int((grid[r][c] + grid[r-1][c] + grid[r+1][c] + grid[r-1][c-1] + grid[r+1][c+1] +grid[r][c-1] + grid[r][c+1] + grid[r-1][c+1] + grid[r+1][c-1])/9);
                gauss[r][c] = avg
        grid = gauss
        for r in range(1,len(grid)-1):
            for c in range(1,len(grid[r])-1):
                avg = int((grid[r][c] + grid[r-1][c] + grid[r+1][c] + grid[r-1][c-1] + grid[r+1][c+1] +grid[r][c-1] + grid[r][c+1] + grid[r-1][c+1] + grid[r+1][c-1])/9);
                gauss[r][c] = avg
        for i in gauss:
            print(i)
            print()
        return gauss
