from ex3.knap_enums.state_enum import StrategyStateEnum
from ex3.knap_enums.knaptype_enum import KnapTypeEnum
from ex3.classes.knapInstance import KnapInstance
from ex3.classes.knapInstanceSolution import KnapInstanceSolution

import time


class KnapStrategy:
    def __init__(self, name, knaptype):
        self.name = name
        self.type = knaptype
        self.strategyType = "unset"
        self.state = StrategyStateEnum.UNSET
        self.candidateSolutionList = []
        self.optSolutionList = []
        self.recursionDepth = 0

    def run(self, instance, measureCpuTime):
        self.optSolutionList = []
        self.candidateSolutionList = []

        # reset error measures


        # reset process time counter
        t = time.process_time()

        # run the strategy on the instance
        recursionDepth = self.runStrategy(instance)

        # measure elapsed time
        cpuTime = time.process_time() - t

        # repeat several times if time is too short to measure
        if measureCpuTime and cpuTime < 0.01:
            # loop amount of times so that cpu time becomes measureable, but at least 4 more times.
            loops = int(1/cpuTime + 4)
            for i in range(loops):
                recursionDepth = self.runStrategy(instance)
            cpuTime = (time.process_time() - t) / (loops+1)

        sol = self.findBestSolution(self.optSolutionList, instance)
        # sol = self.findBestSolution(self.candidateSolutionList, instance)

        return [recursionDepth, cpuTime, sol]

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

        if self.type.equals(KnapTypeEnum.CONSTRUCTIVE):
            # print("Capacity: " + str(w) + "/" + str(instance.getCapacity()))
            if capCheck:
                self.candidateSolutionList.append(KnapInstanceSolution(instance, xList.copy()))
                self.optSolutionList.append(KnapInstanceSolution(instance, xList.copy()))
                return True

        else:
            c = 0
            for i in range(instance.itemnumber):
                c = c + xList[i] * instance.items[i].getCost()
            costCheck = c >= instance.getMinCost()

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







