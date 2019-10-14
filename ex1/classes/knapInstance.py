from ex1.knap_enums.knaptype_enum import KnapTypeEnum


class KnapInstance:
    def __init__(self, knaptype, instanceid, itemnumber, capacity, mincost, items):
        self.knaptype = knaptype
        self.id = instanceid
        self.itemnumber = itemnumber
        self.capacity = capacity
        self.mincost = mincost
        self.items = items

    @classmethod
    def fromInstanceObject(cls, instance):
        return cls(instance.knaptype, instance.id, instance.itemnumber,
                   instance.capacity, instance.mincost, instance.items)

    def getMinCost(self):
        return self.mincost

    def getCapacity(self):
        return self.capacity

