class KnapItem:
    def __init__(self, itemid, weight, cost):
        self.cost = cost
        self.weight = weight
        self.id = itemid
        self.costWeightRatio = self.calcCostWeightRatio(cost, weight)

    def getCost(self):
        return self.cost

    def getWeight(self):
        return self.weight

    def getCostWeightRatio(self):
        return self.costWeightRatio

    def calcCostWeightRatio(self, cost, weight):
        if weight == 0:
            return 0
        else:
            return cost/weight
