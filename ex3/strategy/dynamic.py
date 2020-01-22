from ex3.strategy.knapStrategy import KnapStrategy
from ex3.knap_enums.knaptype_enum import KnapTypeEnum
from ex3.classes.knapInstance import KnapInstance
from ex3.classes.knapInstanceSolution import KnapInstanceSolution
from ex3.classes.knapNode import KnapNode


class DynamicProgrammingStrategy(KnapStrategy):
    def __init__(self, name, knaptype):
        KnapStrategy.__init__(self, name, knaptype)
        self.StrategyType = KnapTypeEnum.CONSTRUCTIVE
        self.instance = None
        self.candidateSolution = None
        self.maxProfit = 0

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

        # decomposition by capacity

        # create 2-dimensional array to store computation results
        # the rows contain the weight units, the columns the items
        # after computation, the array will be of size [capacity+1] rows and [itemnumber+1] columns

        # access the array as [columns][rows] !
        self.W = [[None for j in range(capacity+1)] for i in range(itemnumber+1)]

        # fill trivial cases
        # when no items are added, the weight must be 0
        for i in range(capacity+1):
            self.W[0][i] = 0

        # run dynamic solver

        self.recursionDepth = self.dynamicSolver(capacity, items)

        # start at the last field, containing the result
        solList = self.reconstructSolution(capacity, itemnumber, items, xList)
        self.valid(instance, solList)
        return self.recursionDepth

    def dynamicSolver(self, capacity, items):
        recursionDepth = 0

        for it in items:
            for w in range(capacity+1):
                recursionDepth = recursionDepth + 1
                # two nested for loops.
                # the complexity is O(number of items * (capacity+1))

                valWithoutItem = self.W[it.id][w]   # this works because we filled the trivial cases with 0s
                valWithItem = 0                         # initialize to 0, we will update later

                if w >= it.getWeight():          # check if current items fits in
                    valWithItem = it.getCost()          # if yes, the field value is at least the value of the item

                    remainingCapacity = w - it.getWeight()   # lets see how much space is left
                    valWithItem = valWithItem + self.W[it.id][remainingCapacity]    # add value from the previous column

                if valWithItem > valWithoutItem:        # add the higher value to the map
                    self.W[it.id+1][w] = valWithItem
                else:
                    self.W[it.id+1][w] = valWithoutItem
        return recursionDepth

    def reconstructSolution(self, capacity, index, items, xList):

        # index equals item with id [index-1]

        if index <= 0:
            # last item considered, return solution
            return xList

        res = self.W[index][capacity]

        # if the value stays the same, the item is not used in the solution
        if self.W[index-1][capacity] == res:
            xList[index-1] = 0
        else:
            xList[index-1] = 1
            capacity = capacity - items[index-1].getWeight()

        xList = self.reconstructSolution(capacity, index-1, items, xList)
        return xList















