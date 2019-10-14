from ex1.knap_enums.state_enum import StrategyStateEnum
from ex1.knap_enums.knaptype_enum import KnapTypeEnum
from ex1.classes.knapInstance import KnapInstance
from ex1.classes.knapInstanceSolution import KnapInstanceSolution


class KnapStrategy:
    def __init__(self, name, knaptype):
        self.name = name
        self.type = knaptype
        self.strategyType = "unset"
        self.state = StrategyStateEnum.UNSET
        self.candidateSolutionList = []
        self.optSolutionList = []

    def run(self, instance):
        self.optSolutionList = []
        self.candidateSolutionList = []
        self.runStrategy(instance)
        # sol = self.findBestSolution(self.optSolutionList, instance)
        sol = self.findBestSolution(self.candidateSolutionList, instance)

        return sol

    def valid(self, instance, xList):
        # print("instance id: " + str(instance.id))
        # print("xList: " + str(xList))
        capCheck = False
        costCheck = False
        #   check knapsack capacity
        w = 0
        for i in range(instance.itemnumber):
            w = w + xList[i] * instance.items[i].getWeight()
        capCheck = w <= instance.getCapacity()

        c = 0
        for i in range(instance.itemnumber):
            c = c + xList[i] * instance.items[i].getCost()
        costCheck = c >= instance.getMinCost()

        if self.type.equals(KnapTypeEnum.CONSTRUCTIVE):
            # print("Capacity: " + str(w) + "/" + str(instance.getCapacity()))
            if capCheck:
                self.candidateSolutionList.append(KnapInstanceSolution(instance, xList.copy()))
                self.optSolutionList.append(KnapInstanceSolution(instance, xList.copy()))
                return True

        else:
            # print("Capacity: " + str(w) + "/" + str(instance.getCapacity()))
            # print("Cost: " + str(c) + "/" + str(instance.getMinCost()))
            if capCheck:
                self.optSolutionList.append(KnapInstanceSolution(instance, xList.copy()))
            if capCheck and costCheck:
                self.candidateSolutionList.append(KnapInstanceSolution(instance, xList.copy()))
                return True
        return None

    def findBestSolution(self, candidatesList, instance):
        opt = KnapInstanceSolution(instance, [0]*instance.itemnumber)
        for s in candidatesList:
            if s.getCost() > opt.getCost():
                opt = s

        return opt

    def runStrategy(self, instance):
        print("cannot call abstract function.")
        return None

    def getName(self):
        return self.name

    def getStrategyType(self):
        return self.strategyType

    def getKnapType(self):
        return self.type







