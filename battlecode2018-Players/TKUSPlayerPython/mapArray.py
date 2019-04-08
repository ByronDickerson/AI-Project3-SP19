class Data(object):
	pass


class smartMap:
	earthMap = 0
	marsMap = 0
	earth = 0
	mars = 0
	
	def __init__(self,gc,bc):
		self.gc = gc
		self.bc = bc

		#downloading earth information
	def initializeMapArrays(self):

		self.earth = self.gc.starting_map(self.bc.Planet.Earth)
		self.mars = self.gc.starting_map(self.bc.Planet.Mars)

		self.earthMap = [[0 for x in range(self.earth.width)] for y in range(self.earth.height)]
		self.marsMap = [[0 for x in range(self.mars.width)] for y in range(self.mars.height)]

		# download karbonite and passable terrain locations for Earth

		for j in range(self.earth.height):
		    for i in range(self.earth.width):
		        thisLocation = self.bc.MapLocation(self.bc.Planet.Earth, i, j)
		        newData = Data()
		        newData.x = i
		        newData.y = j
		        newData.unit = 'unknown'
		        newData.team = 'neutral'
		        newData.passable = True
		        newData.karbonite = 0

		        if self.earth.is_passable_terrain_at(thisLocation):
		            newData.passable = True
		            if self.earth.initial_karbonite_at(thisLocation):
		            	newData.karbonite = self.earth.initial_karbonite_at(thisLocation)
		            	# print(earth.initial_karbonite_at(thisLocation), " Karbonite found!")
		            else:
		            	newData.karbonite = 0
		        else:
		            newData.passable = False 
		            newData.karbonite = 0

		       	self.earthMap[i][j] = newData

		# download karbonite and passable terrain locations for Mars
		for d in range(self.mars.width):
		    for c in range(self.mars.height):
		        thisLocation = self.bc.MapLocation(self.bc.Planet.Mars, c, d)
		        newData = Data()
		        newData.x = c
		        newData.y = d
		        newData.unit = 'unknown'
		        newData.team = 'neutral'

	        	if self.mars.is_passable_terrain_at(thisLocation):
	        		newData.passable = True
	        		if self.mars.initial_karbonite_at(thisLocation):
			        	newData.karbonite = self.mars.initial_karbonite_at(thisLocation)
			        	# print(mars.initial_karbonite_at(thisLocation), " Karbonite found!")
			        else:
			        	newData.karbonite = 0
	        	else:
	        		newData.passable = False
	        		newData.karbonite = 0

		       	self.marsMap[c][d] = newData

	def updateKarbonite(self, mapLoc, amount):
		if mapLoc.planet == self.bc.Planet.Earth:
			self.earthMap[mapLoc.x][mapLoc.y].karbonite -= amount
			print(self.earthMap[mapLoc.x][mapLoc.y].karbonite)
		else:
			self.marsMap[mapLoc.x][mapLoc.y].karbonite -= amount

	def updateUnit(self, mapLoc, unitType, team):
		# print("updating map")
		if mapLoc.planet == self.bc.Planet.Earth:
			self.earthMap[mapLoc.x][mapLoc.y].unit = unitType
			self.earthMap[mapLoc.x][mapLoc.y].team = team
			self.earthMap[mapLoc.x][mapLoc.y].passable = False
		
		if mapLoc.planet == self.bc.Planet.Mars:
			self.marsMap[mapLoc.x][mapLoc.y].unit = unitType
			self.marsMap[mapLoc.x][mapLoc.y].team = team
			self.marsMap[mapLoc.x][mapLoc.y].passable = False

	def getMapData(self, mapLocation):
		if mapLocation.planet == self.bc.Planet.Earth:
			return self.earthMap[mapLocation.x][mapLocation.y]

		if mapLocation.planet == self.bc.Planet.Mars:
			return self.marsMap[mapLocation.x][mapLocation.y]
	
	def checkPassable(self, mapLocation):
		if mapLocation.planet == self.bc.Planet.Earth:
			if mapLocation.x <= self.earth.width and mapLocation.y <= self.earth.height:
				if self.earthMap[mapLocation.x][mapLocation.y].passable:
					return True
				else:
					return False

		if mapLocation.planet == self.bc.Planet.Mars:
			if mapLocation.x <= self.mars.width and mapLocation.y <= self.mars.height:

				if self.marsMap[mapLocation.x][mapLocation.y].passable:
					return True
				else:
					return False