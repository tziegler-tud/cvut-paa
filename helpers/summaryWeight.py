#summary weight of all items of one instance, max for each instance, and average above all instances in set
from statistics import mean
import os

from datetime import datetime


class SummaryWeight:

    def __init__(self, path):
        self.valueList = []
        self.path = path
        self.averageList = []
        self.maxColumns = 0
        self.maxWeight = 0
        self.averageItemWeight = 0
        self.averageItemWeightList = []
        self.valueList = self.readInstanceDataFromFile(path)
        self.averageList = self.getAverages(self.valueList)



    def readInstanceDataFromFile(self, path):
        valueList = []
        try:
            instanceFile = open(path, "r")
            instances = instanceFile.readlines()
        except:
            print("failed to read instance data from path: " + path)
            return
        else:
            print("read " + str(len(instances)) + " lines")

        for element in instances:
            line = element.split(" ")
            if len(line) > self.maxColumns:
                self.maxColumns = len(line)
            valueList.append(line)
        return valueList

    def getAverages(self, valueList):
        self.valueList = valueList

        for i in valueList:
            tmpList = []
            n = 3 # first item weight is here
            for j in range(int(i[1])):
                tmpList.append(int(i[n]))
                if int(i[n]) > self.maxWeight:
                    self.maxWeight = int(i[n])
                n = n+2

            avg = mean(tmpList)
            sumCost = sum(tmpList)
            self.averageItemWeightList.append(avg)
            self.averageList.append(sumCost)

        self.averageItemWeight = mean(self.averageItemWeightList)
        self.createOutput(self.averageList)
        return self.averageList

    def createOutput(self, averageList):
        print("input file: " + self.path)
        print("average summary weight:")
        print(mean(averageList))
        print("max item weight:")
        print(self.maxWeight)
        print("average item weight:")
        print(mean(self.averageItemWeightList))
        print("Summary weight values:")
        print(averageList)
        print("\n")

        self.createOutputListFile(averageList, "out/weight.dat")

    def createOutputListFile(self, averageList, filepath):
        index = filepath.rfind("/")
        path = filepath[:index]
        # filename = filepath[index]

        timestamp = datetime.now().strftime("%A, %d %b %Y %H:%M:%S %p")
        c = "time:" + str(timestamp) + "input file: " + self.path +"\n" + "average summary weight:" + str(mean(averageList)) + "\n" + \
            "max item weight:" + str(self.maxWeight) + "\n" + "average item weight:" + \
            str(mean(self.averageItemWeightList)) + "\n" + "Summary weight values:" + str(averageList) + "\n"


        if path == "stdout":
            print(c)
        else:
            try:
                if not os.path.exists(path):
                    os.makedirs(path)
                solution = open(filepath, "a+")
                solution.write(c)
            except:
                print("Error: failed to write solution file at " + filepath + ". Check file system permissions.")

    def returnAverageItemWeight(self):
        return self.averageItemWeight
