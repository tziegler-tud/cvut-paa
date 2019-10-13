from ex1.strategy import *
from ex1.classes.knapInstance import KnapInstance
from ex1.classes.knapItem import KnapItem
from ex1.knap_enums.knaptype_enum import KnapTypeEnum


class KnapSolver:

    def __init__(self, knapstrategy, instancePath, knapType):
        self.knapType = knapType
        self.knapStrategy = knapstrategy
        self.knapInstanceList = None
        self.instancePath = instancePath

    def init(self):
        print("initializing knapsack solver...")
        print("loading knapsack strategy...")
        try:
            print("strategy name: " + self.knapStrategy.getName())
            print("strategy type: " + self.knapStrategy.getStrategyType())
            print("knap type: " + self.knapStrategy.getKnapType().getName())
            print(self.knapType.getName())
            if not self.knapStrategy.getKnapType().equals(self.knapType):
                 raise Exception("Types of Knapsack problem for Strategy and Solver do not match: " + self.knapStrategy.getKnapType().getName() + " (Strategy) vs. " + self.knapType.getName() + " (Solver)")
        except:
            print("strategy failed to initialize. Aborting...")
            return False
        else:
            print("strategy initiation successfull.")

        print("loading knapsack instances...")
        try:
            self.knapInstanceList = self.readInstanceDataFromFile(self.instancePath, self.knapType)
            print(str(len(self.knapInstanceList)) + " instances found")
        except AttributeError:
            print("instances failed to initialize. Aborting...")
            return False
        else:
            print("instance initiation successfull.")
        print("Solver ready to run.")
        return True

    def run(self):
        for i in self.knapInstanceList:
            self.knapStrategy.run(i)

    def readInstanceDataFromFile(self, path, knapType):

        knapInstanceList = []
        try:
            instanceFile = open(path, "r")
            instances = instanceFile.readlines()
        except:
            print("failed to read instance data from path: " + path)
            return
        else:
            print("read " + str(len(instances)) + " lines")

        for element in instances:
            # print(element)
            data = []
            try:
                line = element.split(" ")
                i = 0
                for d in line:
                    data.append(int(d))

            except:
                print("failed to create instance data")
                return False

            instanceid = data[0]
            itemnumber = data[1]
            capacity = data[2]
            items = []
            offset = self.knapType.getDataOffset()
            if offset:
                mincost = data[3]
            else:
                mincost = None
            for i in range(itemnumber):
                items.append(KnapItem(data[2*i + offset + 3], data[2*i + offset + 4]))

            knapInstanceList.append(KnapInstance(knapType, instanceid, itemnumber, capacity, mincost, items))
        return knapInstanceList





