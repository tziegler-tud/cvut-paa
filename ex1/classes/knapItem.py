class KnapItem:
    def __init__(self, itemid, weight, cost):
        self.cost = cost
        self.weight = weight
        self.id = itemid


    def getCost(self):
        return self.cost

    def getWeight(self):
        return self.weight
