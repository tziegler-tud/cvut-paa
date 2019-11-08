from ex2.strategy.knapStrategy import KnapStrategy
from ex2.knap_enums.knaptype_enum import KnapTypeEnum
from ex2.classes.knapInstance import KnapInstance
from ex2.classes.knapInstanceSolution import KnapInstanceSolution
from ex2.classes.knapItem import KnapItem

import math


class FptasStrategy(KnapStrategy):
    def __init__(self, name, knaptype, maxError):
        KnapStrategy.__init__(self, name, knaptype)
        self.StrategyType = KnapTypeEnum.CONSTRUCTIVE
        self.instance = None
        self.candidateSolution = None
        self.maxProfit = 0
        self.error = maxError

        self.W = [[]]

    def runStrategy(self, instance):
        self.recursionDepth = 0
        self.instance = instance



        # initial setup: knapsack empty.

        capacity = instance.capacity
        itemnumber = instance.itemnumber

        items = instance.items
        currentItem = items[0]
        xList = [0 for i in range(itemnumber)]

        # check if there is at least one item that fits in the knapsack
        isPossible = False
        for it in items:
            if it.getWeight() <= capacity:
                isPossible = True
        if not isPossible:
            # reply with empty solution
            self.valid(instance, xList)
            return None

        # apply cost rounding to items
        # get most expensive item value, but exclude items which are too heavy for the knapsack
        maxCost = 0
        for it in items:
            if it.getCost() > maxCost and it.getWeight() <= capacity:
                maxCost = it.getCost()

        # calculate K
        k = (self.error * maxCost) / itemnumber

        # create updated items

        roundedItems = []
        for it in items:
            roundedItems.append(KnapItem(it.id, it.getWeight(), math.floor(it.getCost()/k)))

        # decomposition by cost

        # calculate sum of cost for the instance items as we can limit our map to this value.
        # also calculate total weight of all items to use as case without solution (instead of +infinity)
        sumCost = 0
        sumWeight = 0

        for it in roundedItems:
            sumCost = sumCost + it.getCost()
            sumWeight = sumWeight + it.getWeight()

        # create 2-dimensional array to store computation results
        # the rows contain the cost values, the columns the items
        # after computation, the array will be of size [sumCost+1] rows and [itemnumber+1] columns

        # access the array as [columns][rows]
        self.W = [[None for j in range(sumCost+1)] for i in range(itemnumber+1)]

        # fill trivial cases
        # when no items are added, the weight of the knapsack is considered +inf (the cost values cannot be achieved)
        for i in range(sumCost+1):
            self.W[0][i] = sumWeight

        # W[0][0] initialized to 0
        self.W[0][0] = 0

        # run dynamic solver

        self.recursionDepth = self.dynamicSolver(sumCost, sumWeight, roundedItems)

        # find the field containing the result
        res = 0
        resIndex = 0

        # iterate from lowest cost value to highest. Whenever the weight fits into the knapsack we update cost value.
        for i in range(sumCost+1):
            val = self.W[itemnumber][i]
            if val <= capacity:
                res = val
                resIndex = i

        solList = self.reconstructSolutionByCost(resIndex, itemnumber, roundedItems, xList)
        self.valid(instance, solList)
        return self.recursionDepth

    def dynamicSolver(self, cost, weight, items):
        recursionDepth = 0

        for it in items:
            for w in range(cost+1):
                recursionDepth = recursionDepth + 1
                # two nested for loops.
                # the complexity is O(number of items * (sumCost+1))

                weightWithoutItem = self.W[it.id][w]   # this works because we filled the trivial cases with +inf
                weightWithItem = weight                     # initialize to +inf, we will update later

                if w >= it.getCost():                        # check if current items fits cost
                    weightWithItem = it.getWeight()          # if yes, the field value is at least the value of the item

                    remainingCost = w - it.getCost()     # lets see how much cost is left
                    weightWithItem = weightWithItem + self.W[it.id][remainingCost]    # add value from the previous column

                if weightWithItem < weightWithoutItem:        # add the higher value to the map
                    self.W[it.id+1][w] = weightWithItem
                else:
                    self.W[it.id+1][w] = weightWithoutItem
        return recursionDepth

    def reconstructSolutionByCost(self, cost, index, items, xList):

        # index equals item with id [index-1]

        if index <= 0:
            # last item considered, return solution
            return xList

        res = self.W[index][cost]

        # if the value stays the same, the item is not used in the solution
        if self.W[index-1][cost] == res:
            xList[index-1] = 0
        else:
            xList[index-1] = 1
            cost = cost - items[index-1].getCost()

        xList = self.reconstructSolutionByCost(cost, index-1, items, xList)
        return xList















