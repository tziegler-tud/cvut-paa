#summary cost of all items, average
from statistics import mean


class SummaryCost:

    def __init__(self, path):
        self.valueList = []
        self.path = path
        self.averageList = []
        self.maxColumns = 0
        self.maxCost = 0
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
            n = 4 # first item cost is here
            for j in range(int(i[1])):
                tmpList.append(int(i[n]))
                if int(i[n]) > self.maxCost:
                    self.maxCost = int(i[n])
                n = n+2

            sumCost = sum(tmpList)
            self.averageList.append(sumCost)

        self.createOutput(self.averageList)
        return self.averageList

    def createOutput(self, averageList):
        print("average summary cost:")
        print(mean(averageList))
        print("max item cost:")
        print(self.maxCost)
        print("Summary cost values:")
        print(averageList)