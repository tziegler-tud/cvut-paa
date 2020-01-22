from ex3.strategy import *
from ex3.classes.knapInstance import KnapInstance
from ex3.classes.knapInstanceSolution import KnapInstanceSolution
from ex3.classes.knapItem import KnapItem
from ex3.knap_enums.knaptype_enum import KnapTypeEnum

import os
import time
from datetime import datetime

from statistics import mean


class KnapSolver:

    # KnapSolver object is used to run a certain KnapStrategy on a given set of instances.
    # The instances are read from the path specified.
    # The instances are expected to be as described here: https://moodle-vyuka.cvut.cz/mod/page/view.php?id=55370

    def __init__(self, knapstrategy, instancePath, solutionPath, knapType, **options):
        self.knapType = knapType
        self.knapStrategy = knapstrategy
        self.knapInstanceList = None
        self.knapInstanceSolutionList = None
        self.instancePath = instancePath
        self.solutionPath = solutionPath
        self.solutionFilePath = self.generateFilePath(instancePath, solutionPath, "")
        self.solutionFilePath_desc = self.generateFilePath(instancePath, solutionPath, "_desc")
        self.infoFilePath = self.generateFilePath(instancePath, solutionPath, "_info")
        self. measureCpuTime = False

        self.measureRecursionDepth = options.get("measureRecursionDepth")
        self.measureCpuTime = options.get("measureCpuTime")
        self.measureError = options.get("measureError")
        self.instanceSolutionPath = options.get("instanceSolutionPath")

    def init(self):
        print("initializing knapsack solver...")
        print("loading knapsack strategy...")
        try:
            print("strategy name: " + self.knapStrategy.getName())
            print("strategy type: " + self.knapStrategy.getStrategyType())
            print("knap type: " + self.knapStrategy.getKnapType().getName())
            print(self.knapType.getName())
            if not self.knapStrategy.getKnapType().equals(self.knapType):
                raise Exception("Types of Knapsack problem for Strategy and Solver do not match: " +
                                self.knapStrategy.getKnapType().getName() + " (Strategy) vs. " +
                                self.knapType.getName() + " (Solver)")
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

        # read solution file if enabled

        try:
            self.knapInstanceSolutionList = self.readSolutionDataFromFile(self.instanceSolutionPath, self.knapType)
        except AttributeError:
            print("solution failed to read. Aborting...")
            return False
        else:
            print("solution initiation successfull.")

        # create output files

        try:
            if not os.path.exists(self.solutionPath):
                os.makedirs(self.solutionPath)
            solution = open(self.solutionFilePath, "w+")
            if self.knapType.equals(KnapTypeEnum.DECISIVE):
                solution2 = open(self.solutionFilePath_desc, "w+")
                solution2.close()
            solution.close()
            info = open(self.infoFilePath, "w+")
            info.close()
        except:
            print("Error: failed to write solution file. Check file system permissions.")

        print("Solver ready to run.")
        return True

    def run(self):

        print("starting solver.")

        # init maxRecursionDepth and avgRecursionDepth variables
        maxRecursionDepth = 0
        maxRecursionDepthId = 0
        avgRecursionDepth = 0
        recDepthList = []

        # init maxCpuTime, avgCpuTime variables
        maxCpuTime = 0
        maxCpuTimeId = 0
        avgCpuTime = 0
        cpuTimeList = []

        # init error measures
        maxError = 0
        error = 0
        errorList = []
        maxErrorId = None

        # we dont have information about the instance size here, but we can use the instances to read it later
        instanceSize = 0

        # process one instance at a time
        for index, i in enumerate(self.knapInstanceList):

            progressOut = "[" + "#" * int(20 * (abs(index) / len(self.knapInstanceList))) + \
                          "-" * (20 - int(20 * (abs(index) / len(self.knapInstanceList)))) + "]  " + \
                          str(int(((abs(index) / len(self.knapInstanceList))*100))) + "%"
            print(progressOut)

            # guess instance size from last element
            instanceSize = i.itemnumber

            #   run the strategy. returns a list [<int> recursionDepth, <int> cpuTime, <KnapInstanceSolution> sol]
            info = self.knapStrategy.run(i, self.measureCpuTime)

            recursionDepth = info[0]
            cpuTime = info[1]
            sol = info[2]

            if self.measureRecursionDepth:
                if recursionDepth is not None:
                    recDepthList.append(int(recursionDepth))


                    if maxRecursionDepth < recursionDepth:
                        maxRecursionDepth = recursionDepth
                        maxRecursionDepthId = i.id


            if self.measureCpuTime:
                cpuTimeList.append(cpuTime)
                if maxCpuTime < cpuTime:
                        maxCpuTime = cpuTime
                        maxCpuTimeId = i.id

            # measure Error if enabled
            if self.measureError:
                # retrieve given solution instance

                # optSolution = self.knapInstanceSolutionList[i.id-1]
                # ^ does no longer work because of the messy id in the ZKW sets...

                # careful, it's a python dictionary now!
                optSolution = self.knapInstanceSolutionList.get(i.id)

                if optSolution != 0:
                    # skip if no solution exists
                    error = (optSolution - sol.getCost()) / optSolution
                    errorList.append(error)
                    if maxError < error:
                        maxError = error
                        maxErrorId = i.id

            # generate optimal solution output
            if isinstance(sol, KnapInstanceSolution):
                solutionFile = open(self.solutionFilePath, "a+")
                solutionFile.write(sol.generateSolutionOutput() + "\n")

            # generate decision version solution output.
            if self.knapType.equals(KnapTypeEnum.DECISIVE):
                descSolutionFile = open(self.solutionFilePath_desc, "a+")
                descSolutionFile.write(str(1 if sol.decide() else 0) + "\n")

        # generate runtime and complexity information
        timestamp = datetime.now().strftime("%A, %d %b %Y %H:%M:%S %p")

        avgRecursionDepth = 0
        avgCpuTime = 0
        avgError = 0

        if self.measureRecursionDepth:
            avgRecursionDepth = mean(recDepthList)

        if self.measureCpuTime:
            avgCpuTime = mean(cpuTimeList)

        if self.measureError:
            avgError = mean(errorList)

        try:
            infoFile = open(self.infoFilePath, "a+")
            infoFile.write("Knapsack Solution Information\n" + "Date: " + str(timestamp) + "\n\n" +
                           "Type of Knapsack problem: " + self.knapType.getName() + "\n" +
                           "Strategy: " + self.knapStrategy.getName() +
                           "\n" +
                           "Input file: " + self.instancePath + "\n" +
                           "Solution outputs: \n" + "      " + self.solutionFilePath + "\n" +
                           str("      " + self.solutionFilePath_desc + "\n" if self.knapType.equals(KnapTypeEnum.DECISIVE) else "") +
                           "\n" +
                           "Instance size: " + str(instanceSize) + "\n" +
                           "Number of instances: " + str(len(self.knapInstanceList)) + "\n" +
                           "\n" +
                           "Average visited notes: " + str(avgRecursionDepth) + "\n"
                           "maximum visited notes: " + str(maxRecursionDepth) + " at instance id: " + str(maxRecursionDepthId) + "\n"
                           "Average cpu time: " + str(avgCpuTime) + "\n" +
                           "maximum cpu time: " + str(maxCpuTime) + " at instance id: " + str(maxCpuTimeId) + "\n" +
                           "Average error: " + str(avgError) + "\n" +
                           "maximum error: " + str(maxError) + " at instance id: " + str(maxErrorId) + "\n" +
                           "\n" + "end of generated file.")
        except:
            print("failed to write information file.")
        else:
            print("Finished Solver. Find evaluation information here: " + self.infoFilePath)

        return [avgRecursionDepth, maxRecursionDepth, avgError, maxError]

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
                items.append(KnapItem(i, data[2*i + offset + 3], data[2*i + offset + 4]))

            knapInstanceList.append(KnapInstance(knapType, instanceid, itemnumber, capacity, mincost, items))
        return knapInstanceList

    def readSolutionDataFromFile(self, path, knapType):

        knapOptSolutionMap = {}

        try:
            instanceFile = open(path, "r")
            instances = instanceFile.readlines()
        except:
            print("failed to read instance solution data from path: " + path)
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
                    try:
                        data.append(int(d))
                    except ValueError:
                        continue


            except:
                print("failed to create instance solution data")
                return False

            instanceid = data[0]
            cost = data[2]

            knapOptSolutionMap[instanceid] = cost
        return knapOptSolutionMap

    def generateFilePath(self, instancePath, solPath, name_mod):
        s = instancePath.split("/")
        f = ""
        if len(s) == 1:
            f = s
        else:
            f = s[len(s)-1]
        f = f.split("_")
        if len(f) == 2:
            g = f[1].split(".")[1]
            return solPath + "/" + f[0] + "_sol" + name_mod + "." + g
        else:
            return solPath + "/" + f[0] + name_mod







