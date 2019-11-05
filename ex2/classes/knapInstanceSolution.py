from ex2.classes.knapInstance import KnapInstance


class KnapInstanceSolution(KnapInstance):
    def __init__(self, instance, xList):
        KnapInstance.__init__(self, instance.knaptype, instance.id, instance.itemnumber,
                     instance.capacity, instance.mincost, instance.items)
        self.xList = xList
        self.solcap = self.calcSolCap()
        self.solcost = self.calcSolCost()

    def setXList(self, xList):
        self.xList = xList

    def generateSolutionOutput(self):
        return str(str(abs(self.id)) + " " + str(self.itemnumber) + " " +
                   str(self.solcost) + " " + self.xListToString(self.xList))

    def calcSolCap(self):
        w = 0
        for i in range(self.itemnumber):
            w = w + self.xList[i] * self.items[i].getWeight()
        return w

    def calcSolCost(self):
        c = 0
        for i in range(self.itemnumber):
            c = c + self.xList[i] * self.items[i].getCost()
        return c

    def decide(self):
        return self.capacity >= self.solcap and self.mincost <= self.solcost

    def getCost(self):
        return self.solcost

    def xListToString(self, xList):
        s = ""
        for x in xList:
            s = s + str(x) + " "

        return s[0:len(s)-1]
