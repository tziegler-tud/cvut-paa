from ex2.strategy.knapStrategy import KnapStrategy
from ex2.knap_enums.knaptype_enum import KnapTypeEnum
from ex2.classes.knapInstance import KnapInstance
from ex2.classes.knapInstanceSolution import KnapInstanceSolution
from ex2.classes.knapNode import KnapNode
from ex2.classes.knapItem import KnapItem


class ExtendedHeuristicStrategy(KnapStrategy):
    def __init__(self, name, knaptype):
        KnapStrategy.__init__(self, name, knaptype)
        self.StrategyType = KnapTypeEnum.CONSTRUCTIVE
        self.instance = None
        self.candidateSolution = None
        self.maxProfit = 0

    def runStrategy(self, instance):
        self.recursionDepth = 0
        self.instance = instance

        # initial setup: knapsack empty.

        capacity = instance.capacity
        currentWeight = 0
        itemnumber = instance.itemnumber
        xList = [0 for i in range(instance.itemnumber)]

        # order instance items by cost/ weight ratio.
        # We use the item.itemid to keep track of which item we added.

        candidateItemList = instance.items.copy()
        candidateItemList.sort(key=lambda it: (it.getCost()/it.getWeight()), reverse=True)

        # find the item with the highest cost that fits into the knapsack
        # this works, but doesnt allow counting the computation steps:
        # ItemListByCost = instance.items.copy()
        # ItemListByCost.sort(key=lambda it: (it.getCost()), reverse=True)

        # let's use this instead
        highestCostItem = KnapItem(-1, 0, 0)    # create dummy item
        for item in instance.items:
            self.recursionDepth = self.recursionDepth + 1
            if item.getWeight() <= capacity and item.getCost() > highestCostItem.getCost():
                highestCostItem = item

        # run heuristic solver with sorted item list

        self.recursionStep(instance, candidateItemList, currentWeight, capacity, xList, highestCostItem)
        return self.recursionDepth

    def recursionStep(self, instance, candidateItemList, currentWeight, capacity, xList, highestCostItem):

        self.recursionDepth = self.recursionDepth + 1

        # get item with highest ratio
        item = candidateItemList[0]
        # Add to knapsack if item fits in, or return if too heavy.
        if item.getWeight() <= (capacity-currentWeight):
            currentWeight = currentWeight + item.getWeight()
            xList[item.id] = 1

        # check if more items in queue
        if len(candidateItemList) >= 2:
            # items remaining. Continue with next item
            self.recursionStep(instance, candidateItemList[1:], currentWeight, capacity, xList, highestCostItem)
        else:
            # reached leave. returning candidate solution
            self.compareWithHighestCostAndValidate(instance, xList, highestCostItem)
            return

    def compareWithHighestCostAndValidate(self, instance, xList, highestCostItem):

        # create candidate solution object
        sol = KnapInstanceSolution(instance, xList)

        # check if there is an item that fits in the knapsack

        if highestCostItem is None:
            # the heuristic solution must be empty as well, but we will propagade it to the solver anyway.
            self.valid(instance, xList)
            return

        # create solution object containing only the item with the highest cost
        highestCostList = [0 for i in range(instance.itemnumber)]
        highestCostList[highestCostItem.id] = 1
        highestCostItemSolution = KnapInstanceSolution(instance, highestCostList)

        if sol.getCost() >= highestCostItemSolution.getCost():
            self.valid(instance, xList)
        else:
            self.valid(instance, highestCostList)
        return












