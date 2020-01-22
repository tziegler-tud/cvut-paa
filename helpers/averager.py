#read input and average column values
from statistics import mean


class Averager:

    def __init__(self, path):
        self.valueList = []
        self.path = path
        self.averageList = []
        self.maxColumns = 0
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
        self.averageList = [0 for i in range(self.maxColumns)]
        for i in range(self.maxColumns):
            tmpList=[]
            for element in valueList:
                try:
                    tmpList.append(int(element[i]))
                    self.averageList[i] = int(mean(tmpList))
                except:
                    continue

        self.createOutput(self.averageList)

    def createOutput(self, averageList):
        print("Average values:\n")
        print(averageList)