from ex1.knap_enums.state_enum import StrategyStateEnum
from ex1.knap_enums.knaptype_enum import KnapTypeEnum


class KnapStrategy:
    def __init__(self, name, knaptype):
        self.name = name
        self.type = knaptype
        self.strategyType = "unset"
        self.state = StrategyStateEnum.UNSET
        print("initializing strategy object")

    def run(self, instance):
        print("cannot call abstract function")

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
            return capCheck
        else:
            # print("Capacity: " + str(w) + "/" + str(instance.getCapacity()))
            # print("Cost: " + str(c) + "/" + str(instance.getMinCost()))
            return capCheck and costCheck

    def getName(self):
        return self.name

    def getStrategyType(self):
        return self.strategyType

    def getKnapType(self):
        return self.type







