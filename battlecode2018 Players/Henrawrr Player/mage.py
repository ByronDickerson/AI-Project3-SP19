import battlecode as bc
import random
import sys
import traceback
import time
from random import randint
import os

class Mage:
	def __init__(self, gc, unit):
		self.unit = unit
		self.gc = gc
	
	def teamup(self, bc, bcUnit):
		self.gc.sense_nearby_units_by_team(location, radius, team)

	def target(self):
		team = self.gc.team()
		otherteam = None
		if(team == bc.Team.Red):
			otherteam = bc.Team.Blue
		else:
			otherteam = bc.Team.Red
		possibles=self.gc.sense_nearby_units_by_team(self.unit.location.map_location(), self.unit.attack_range(), otherteam)
		maxkills = 0
		maxneardeath = 0
		maxlocation = None
		
		for units in possibles:
			kills = 0
			neardeath = 0
			enemylocation = units.location.map_location()
			x = enemylocation.x
			y = enemylocation.y
			if units.health <=60:
				kills = kills+1
			elif units.health <=120:
				neardeath = neardeath +1 
			surround = self.gc.sense_nearby_units_by_team(enemylocation, 1, otherteam)
			for thing in surround:
				if thing.health <=60:
					kills=kills+1
				elif thing.health <=120:
					neardeath = neardeath +1
			if kills > maxkills:
				maxkills = kills
				maxlocation = enemylocation
			elif kills == maxkills:
				if neardeath > maxneardeath:
					maxneardeath = neardeath
					maxlocation = enemylocation

		return maxlocation

			# for i in range(-1,1):
			# 	for j in range(-1,1):
			# 		if()


