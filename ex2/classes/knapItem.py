class KnapItem:
    def __init__(self, itemid, weight, cost):
        self.cost = cost
        self.weight = weight
        self.id = itemid
        self.costWeightRatio = cost/weight

    def getCost(self):
        return self.cost

    def getWeight(self):
        return self.weight

    def getCostWeightRatio(self):
        return self.costWeightRatio
