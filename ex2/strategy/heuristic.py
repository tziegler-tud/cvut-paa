from ex2.strategy.knapStrategy import KnapStrategy
from ex2.knap_enums.knaptype_enum import KnapTypeEnum
from ex2.classes.knapInstance import KnapInstance
from ex2.classes.knapInstanceSolution import KnapInstanceSolution
from ex2.classes.knapNode import KnapNode


class SimpleHeuristicStrategy(KnapStrategy):
    def __init__(self, name, knaptype):
        KnapStrategy.__init__(self, name, knaptype)
        self.StrategyType = KnapTypeEnum.CONSTRUCTIVE
        self.instance = None
        self.candidateSolution = None
        self.maxProfit = 0

    def runStrategy(self, instance):
        self.recursionDepth = 0
        self.instance = instance

        # order instance items by cost/ weight ratio.
        # We use the item.itemid to keep track of which item we added.

        candidateItemList = instance.items.copy()
        candidateItemList.sort(key=lambda it: (it.getCost()/it.getWeight()), reverse=True)

        # initial setup: knapsack empty.

        capacity = instance.capacity
        currentWeight = 0
        itemnumber = instance.itemnumber
        xList = [0 for i in range(instance.itemnumber)]

        # run heuristic solver with sorted item list

        self.recursionStep(instance, candidateItemList, currentWeight, capacity, xList)
        return self.recursionDepth

    def recursionStep(self, instance, candidateItemList, currentWeight, capacity, xList):

        self.recursionDepth = self.recursionDepth + 1
        # get item with highest ratio
        item = candidateItemList[0]
        # Add to knapsack if item fits in, or skip if too heavy.
        if item.getWeight() <= (capacity-currentWeight):
            currentWeight = currentWeight + item.getWeight()
            xList[item.id] = 1

        # check if more items in queue
        if len(candidateItemList) >= 2:
            # items remaining. Continue with next item
            self.recursionStep(instance, candidateItemList[1:], currentWeight, capacity, xList)
        else:
            # reached leave. returning candidate solution
            self.valid(instance, xList)
            return












