class KnapItem:
    def __init__(self, weight, cost):
        self.cost = cost
        self.weight = weight

    def getCost(self):
        return self.cost

    def getWeight(self):
        return self.weight
