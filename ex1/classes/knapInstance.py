from ex1.knap_enums.knaptype_enum import KnapTypeEnum


class KnapInstance:
    def __init__(self, knaptype, instanceid, itemnumber, capacity, mincost, items):
        self.knaptype = knaptype
        self.id = instanceid
        self.itemnumber = itemnumber
        self.capacity = capacity
        self.minCost = mincost
        self.items = items

    def getMinCost(self):
        return self.minCost

    def getCapacity(self):
        return self.capacity

