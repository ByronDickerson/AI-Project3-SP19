import battlecode as bc 

# makes a new target object with the id of the unit and their current target
class newTarget:
    unit_id = 0
    mapTarget = 0
    def __init__(self, unit_id, mapTarget):
        self.unit_id = unit_id
        self.mapTarget = mapTarget
    
    def __repr__(self):
        return "newTarget()"

    def __str__(self):
        return "member of Test"

class targetList:
    
    def __init__(self):
        self.unitTargetList = []

    # add the current target of the unit_id to the list for later use
    def addToList(self, unit_id, mapTarget):
        unitFound = False
        for i in range(len(self.unitTargetList)):
            if self.unitTargetList[i].unit_id == unit_id:
                unitFound = True
        
        if not unitFound:
            unitTarget = newTarget(unit_id, mapTarget)
            self.unitTargetList.append(unitTarget)

    # returns the currentTarget for the unit
    def getCurrentTarget(self, unit_id):
        for i in range(len(self.unitTargetList)):
            if self.unitTargetList[i].unit_id == unit_id:
                return self.unitTargetList[i].mapTarget

    # used to check if the current unit has a valunit_id target
    def hasTarget(self, unit_id):
        for i in range(len(self.unitTargetList)):
            if self.unitTargetList[i].unit_id == unit_id:
                return True

        return False
    
    def targetAlreadyTaken(self, mapTarget):
        for i in range(len(self.unitTargetList)):
            if self.unitTargetList[i].mapTarget == mapTarget:
                return True

        return False

    # if the unit doesn't have a valunit_id target clear it so a new one can be added
    def clearCurrentTarget(self, unit_id):
        for i in range(len(self.unitTargetList)):
            if self.unitTargetList[i].unit_id == unit_id:
                del self.unitTargetList[i]
                break