from ex1.strategy.knapStrategy import KnapStrategy
from ex1.knap_enums.knaptype_enum import KnapTypeEnum
from ex1.classes.knapInstance import KnapInstance
from ex1.classes.knapInstanceSolution import KnapInstanceSolution


class BruteForceStrategy(KnapStrategy):
    def __init__(self, name, knaptype):
        KnapStrategy.__init__(self, name, knaptype)
        self.StrategyType = "Bruteforce"
        self.instance = None
        self.candidateSolution = None


    def runStrategy(self, instance):
        self.recursionDepth = 0
        self.instance = instance

        # print("processing instance with id: " + str(instance.id))

        # create vector [x1,...,xn] and initialize with 0s
        xList = [0 for i in range(instance.itemnumber)]

        # begin recursion
        self.recursionStep(instance, xList, 0)

        return self.recursionDepth

    def recursionStep(self, instance, xList, index):

        if index == instance.itemnumber:
            # reached node. Incrementing Depth
            self.recursionDepth += 1

            # check if solution is valid
            self.valid(instance, xList)
            return

        yxList = xList.copy()
        yxList[index] = 0
        self.recursionStep(instance, yxList, index + 1)

        yxList[index] = 1
        self.recursionStep(instance, yxList, index + 1)







