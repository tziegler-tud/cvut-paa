class KnapNode:
    def __init__(self, level, upperBound, profit, weight, items, instance):
        self.level = level
        self.upperBound = upperBound
        self.profit = profit
        self.weight = weight
        self.items = items
        self.instance = instance

    def addItem(self, item):
        self.items.append(item)

    def createXList(self):
        xList = [0] * self.instance.itemnumber

        for i in self.items:
            xList[i.id] = 1

        return xList

    def getUpperBound(self):
        return int(self.upperBound)





