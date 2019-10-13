from ex1.strategy.knapStrategy import KnapStrategy
from ex1.knap_enums.knaptype_enum import KnapTypeEnum


class BruteForceStrategy(KnapStrategy):
    def __init__(self, name, knaptype):
        KnapStrategy.__init__(self, name, knaptype)
        self.StrategyType = "Bruteforce"
        self.instance = None

    def run(self, instance):
        self.instance = instance
        print("Bruteforce running")
        print("calculating instance with id: " + str(instance.id))
        print("Number of items: " + str(instance.itemnumber))

        # create vector [x1,...,xn] and initialize with 0s
        xList = [0 for i in range(instance.itemnumber)]

        # begin recursion
        self.recursionStep(instance, xList, 0)

    def recursionStep(self, instance, xList, index):

        if index == instance.itemnumber:
            if self.valid(instance, xList):
                print("found solution: instance id: " + str(instance.id) + " Assignment: " + str(xList))
            return
        xList[index] = 0
        self.recursionStep(instance, xList, index + 1)

        xList[index] = 1
        self.recursionStep(instance, xList, index + 1)





