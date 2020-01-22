from ex3.strategy.knapStrategy import KnapStrategy
from ex3.knap_enums.knaptype_enum import KnapTypeEnum
from ex3.classes.knapInstance import KnapInstance
from ex3.classes.knapInstanceSolution import KnapInstanceSolution
from ex3.classes.knapNode import KnapNode


class BandbStrategy(KnapStrategy):
    def __init__(self, name, knaptype):
        KnapStrategy.__init__(self, name, knaptype)
        self.StrategyType = "Branch & Bound"
        self.instance = None
        self.candidateSolution = None
        self.maxProfit = 0
        self.knaptype = knaptype

    def runStrategy(self, instance):
        self.recursionDepth = 0
        self.instance = instance

        # initial setup: knapsack empty, queue filled

        self.maxProfit = 0

        initNode = KnapNode(-1, 0, 0, 0, [], instance)

        queue = [initNode]

        # print("processing instance with id: " + str(instance.id))

        # begin branchAndBound algorithm
        self.branchAndBound(instance, queue)

        return self.recursionDepth

    def branchAndBound(self, instance, queue):

        itemnumber = instance.itemnumber
        a = 0

        while not len(queue) == 0:
            self.recursionDepth += 1
            #   retrieve first item in queue
            it = queue.pop()
            n = KnapNode(0, 0, 0, 0, [], instance)
            l = KnapNode(0, 0, 0, 0, [], instance)

            n.items = it.items.copy()
            l.items = it.items.copy()

            # reached leaf node
            if it.level == itemnumber - 1:
                continue

            # explore next level
            n.level = it.level + 1
            l.level = it.level + 1

            # add profit and weight of next node
            n.profit = it.profit + instance.items[n.level].getCost()
            n.weight = it.weight + instance.items[n.level].getWeight()
            n.addItem(instance.items[n.level])

            # check if weight is still ok
            if n.weight <= instance.getCapacity():

                # check if profit is grt than current maxProfit and update in that case
                if n.profit > self.maxProfit:
                    self.maxProfit = n.profit

                    # add n as potential solution
                    self.valid(instance, n.createXList())

                # calc upper bound of profit for the node
                n.upperBound = self.calcBound(n, instance, n.level)

                # if upper Bound is above current maxProfit, queue node for consideration
                if n.upperBound > self.maxProfit:
                    queue.append(n)

            # now dont take the item in the knapsack, but still consider following nodes
            l.profit = it.profit
            l.weight = it.weight
            l.upperBound = self.calcBound(l, instance, l.level)
            if l.upperBound > self.maxProfit:
                queue.append(l)

    def calcBound(self, node, instance, currentItemLevel):

        if node.weight > instance.getCapacity():
            return 0

        weight = node.weight
        bound = node.profit
        for i in range(currentItemLevel + 1, instance.itemnumber):
            # newweight = weight + instance.items[i].getWeight()
            # newbound = bound + instance.items[i].getCost()
            # if newweight > instance.getCapacity():
            #     continue
            # else:
            #     if newbound > bound:
            #         weight = newweight
            #         bound = newbound

            bound = bound + instance.items[i].getCost()

        return bound









