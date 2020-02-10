
import math
import random
import numpy
import statistics
import os
from datetime import datetime

import sys

import matplotlib.pyplot as plt
import matplotlib.animation as animation


class GeneticStrategy:
    def __init__(self, **options):
        self.instance = None
        self.path = "out/"
        # self.filename = "Gen" + "?" + "_" + datetime.now().strftime("%d%b%Y-%H:%M") + ".geninfo"
        self.filename = "Gen" + "?" + ".geninfo"

        # default parameters
        generationCapDefault = 1000
        populationSizeDefault = 50
        instanceSizeDefault = 20

        elitismDefault = 1
        crossoverRateDefault = 0.8
        mutationRateDefault = 0.02

        # default settings
        enablePlotDefault = False
        logGenerationResultsDefault = False
        outputFrequencyDefault = 250
        outputIdDefault = self.createId()



        self.errorCap = 0.1
        self.setErrorCap = False
        self.opt = 0
        self.adaptive = False

        # get options
        self.populationSize = options.get("instanceSize", instanceSizeDefault)
        self.populationSize = options.get("populationSize", populationSizeDefault)
        self.generationCap = options.get("generationCap", generationCapDefault)
        self.elitism = options.get("elitism", elitismDefault)
        self.crossoverRate = options.get("crossoverRate", crossoverRateDefault)
        self.mutationRate = options.get("mutationRate", mutationRateDefault)
        self.instanceSize = options.get("mutationRate", instanceSizeDefault)

        self.enablePlot = options.get("enablePlot", enablePlotDefault)
        self.logGenerationResults = options.get("logGenerationResults", logGenerationResultsDefault)
        self.outputFrequency = options.get("outputFrequency", outputFrequencyDefault)
        self.uniqueRunId = options.get("outputId", outputIdDefault)
        self.scaleMax = int(options.get("scaleMax", 30))

        # self.setErrorCap = options.get("setErrorCap")
        # self.errorCap = options.get("errorCap")

    def setRunId(self, id):
        self.uniqueRunId = id
        # self.filename = str(id) + ".geninfo"

    def setOptimalSolution(self, opt):
        self.opt = opt

    # overwrite default run function, as we need some other measures here
    def run(self, instance, measureCpuTime):

        results = self.runStrategy(instance)
        return results

    def runStrategy(self, instance):
        self.recursionDepth = 0
        self.instance = instance
        self.instanceSize = instance.variables

        minGenerations = 50

        bestLastChanged = 0
        avgLastChanged = 0
        avgFrameList = [0]


        # reset iteration counter
        it = 0

        # reset output log counter
        outputCounter = 1

        # initial population: randomly created individuals.
        # one individual is a bool list of len(instanceSize)
        # an individual can be considered a variable assignment
        pop = []  # population is list of individuals
        for i in range(self.populationSize):
            ind = []
            # create random individual
            for j in range(self.instanceSize):
                ind.append(bool(random.randint(0, 1)))
            pop.append(ind)


        # decide whether to stop after a certain amount of generations, or when a certain relative error is achieved
        if self.setErrorCap:
            print("not yet implemented. please choose generation cap.")
            # TODO: implement this

        else:
            self.print_progress(0, self.generationCap, prefix='Progress:', suffix='Complete', bar_length=50)

            best = numpy.zeros(self.generationCap)
            avg = numpy.zeros(self.generationCap)
            worst = numpy.zeros(self.generationCap)

            while it < self.generationCap:

                self.print_progress(it, self.generationCap, prefix='Progress:', suffix='Complete', bar_length=50)

                # result = [stats, new population]
                result = self.processGeneration(instance, pop)

                # stats = [best, worst, average]
                stats = result[0]
                pop = result[1]

                # after each generation, write progress to file in a tikz-friendly format
                if self.logGenerationResults:
                    # self.writeGenerationResult(pop, stats, it)
                    #log only every <lim> generations
                    if outputCounter >= self.outputFrequency:
                        self.writeLatexOutput(pop, stats, it)
                        self.writeLatexErrorOutput(pop, stats, it, self.opt)
                        outputCounter = 0

                best[it] = stats[0]
                avg[it] = stats[2]
                worst[it] = stats[1]

                # adaptive generation cap
                if self.adaptive and it > 0:
                    if stats[0] != best[it - 1]:
                        bestLastChanged = it

                    avgFrame = int(statistics.mean(avg[math.floor(it*3/4):it]))
                    avgFrameList.append(avgFrame)
                    if avgFrame > avgFrameList[it-1]:
                        avgLastChanged = it

                    # if bestLastChanged < math.floor(it/2) and avgLastChanged < math.floor(it*3/4) and it > minGenerations:
                    if bestLastChanged < math.floor(it/2) and best[it] > 0 and it > minGenerations:
                        self.generationCap = it
                        best = best[:it]
                        avg = avg[:it]
                        worst = worst[:it]
                        break

                it = it + 1
                outputCounter = outputCounter + 1

                ## we experience heavy degeneration after only a few generations. trying to measure it to find causalities...
                ## Edit: no longer an issue, but i will leave that code here just in case...

                # diversity = 0
                # diversityMatrix = [[0 for i in range(len(pop))] for j in range(len(pop))]
                # for p in range(len(pop)):
                #     for t in range(len(pop)):
                #         if p == t:
                #             continue
                #         d = 0
                #         for i, j in zip(pop[p], pop[t]):
                #             d = d + abs(i - j)
                #         diversityMatrix[p][t] = d
                # p = 0 # debugging breakpoint

            # plot results
            if self.enablePlot:
                xplot = numpy.arange(self.generationCap)

                fig = plt.figure()
                ax = fig.add_subplot(111)
                line, = ax.plot(xplot, avg, color='red')

                fig2 = plt.figure()
                ax2 = fig2.add_subplot(111)
                line2, = ax2.plot(xplot, best)
                # line, = ax.plot(xplot, worst, color='orange')

                # fig3 = plt.figure()
                # ax3 = fig3.add_subplot(111)
                # line2, = ax3.plot(xplot, worst, color='orange')

                fig4 = plt.figure()
                ax4 = fig4.add_subplot(111)
                line41, = ax4.plot(xplot, best, color='red')
                line42, = ax4.plot(xplot, avg)
                line43, = ax4.plot(xplot, worst, color='orange')

                plt.draw()
                plt.show()

        # return Solution of fittest individual of final population for evaluation
        # sortedIndices = list(numpy.argsort(self.evaluatePopulation(instance, pop)))
        # sortedIndices.reverse()
        return [it, len(pop), stats[0]]

    def processGeneration(self, instance, pop):
        popSize = len(pop)
        # generate fitness of population
        popScore = self.evaluatePopulation(instance, pop)  # list of scores for each individuum

        # we use ranking selection strategy for now (might implement another one later if I find the time)
        ## create ranking by sorting the fitness list
        ### we use numpy to obtain the indices of the ordered list. These correspond to the ranks, i.e. s[i] is the number of the indiv. of rank i
        sortedIndices = list(numpy.argsort(popScore))
        sortedIndices.reverse()

        # obtain best, worst and average fitness for evaluation
        stats = [0, 0, 0]
        stats[0] = popScore[sortedIndices[0]]
        stats[1] = popScore[sortedIndices[len(sortedIndices)-1]]
        stats[2] = statistics.mean(popScore)



        # create new generation

        newPop = []

        ## first, preserve elite individuals
        for i in range(self.elitism):
            newPop.append(pop[sortedIndices[i]].copy())

        # parent selection
        sortedIndicesFactor = [None for i in range(self.populationSize)]
        parentsCandidates = []
        # we use ranked selection with linear scaling
        # first, add copies of parents based on their rank
        # we just keep track of the indices to reduce memory usage
        scale_min = 1
        # scale_max = 30
        scale_max = self.scaleMax

        for rank in range(popSize):
            # scaleFactor = (scale_min + popScore[sortedIndices[rank]]-stats[1]) * (scale_max - scale_min)/(stats[0] - stats[1])
            # scaleFactor € [0, 1] relative fitness
            scaleFactor = (scale_min) + (popScore[sortedIndices[rank]] - stats[1]) * (scale_max-scale_min + 1) / (stats[0] - stats[1] + 1)
            # scaleFactor = 1

            #rankFactor
            # rankFactor = (popSize - rank)
            rankFactor = 1

            #totalFactor
            totalFactor = rankFactor * scaleFactor

            # sortedIndicesFactor[rank] = totalFactor

            for copies in range(int(totalFactor)):
                parentsCandidates.append(sortedIndices[rank])

        # now, select parents for next generation by randomly drawing from scaled pool
        # we need popSize - elitism potential parents
        # allow each parent only once!

        parentsPool = []
        for i in range(popSize-self.elitism):
            p = parentsCandidates[random.randint(0, len(parentsCandidates)-1)]
            if random.uniform(0, 1) < self.crossoverRate:
                parentsPool.append(pop[i].copy())
            else:
                newPop.append(pop[p].copy())

        # parentsPool = []
        #
        # def weighted_random_choice(population, popScore, max):
        #     pick = random.uniform(0, max)
        #     current = 0
        #     for ind in range(len(population)):
        #         current += popScore[ind]
        #         if current >= pick:
        #             return ind
        #
        # max = sum(sortedIndicesFactor[ind] for ind in range(self.populationSize))
        #
        # for i in range(popSize-self.elitism):
        #     ind = weighted_random_choice(pop, sortedIndicesFactor, max)
        #     if random.uniform(0, 1) < self.crossoverRate:
        #         parentsPool.append(pop[sortedIndices[ind]].copy())
        #     else:
        #         newPop.append(pop[sortedIndices[ind]].copy())


        ### we use one-point crossover, though this might conceive invalid configurations (capacity exceeded)
        ### get random crossover position

        randPos = random.randint(0, self.instanceSize - 1)
        # randPos = int(self.instanceSize/2)

        while len(parentsPool) > 0:
            ### draw parent and remove from pool
            parent = parentsPool.pop(0)

            #try to find mating partner
            if len(parentsPool) > 0:
                mate = parentsPool.pop(0)

                #### perform crossover
                c1 = [0 for i in range(self.instanceSize)]
                c2 = [0 for i in range(self.instanceSize)]
                for i in range(randPos):
                    c1[i] = parent[i]
                    c2[i] = mate[i]

                for i in range(randPos, self.instanceSize):
                    c1[i] = mate[i]
                    c2[i] = parent[i]

                ## add to population
                newPop.append(c1.copy())
                newPop.append(c2.copy())

            else:
                #### keep parents
                c1 = parent
                newPop.append(c1.copy())


        ## mutation
        ### probability for mutation
        for j in range(self.elitism, len(newPop)):
            c = newPop[j].copy()

            for gene in range(len(c)):
                if random.uniform(0, 1) < self.mutationRate:
                    ## select a random gene and flip it
                    if c[gene] == True:
                        c[gene] = False

                    else:
                        c[gene] = True



            # replace population
            newPop[j] = c

        # return new generation
        return [stats, newPop]

    def evaluatePopulation(self, instance, pop):
        popScore = []
        for ind in pop:
            fit = self.fitness(instance, ind)
            popScore.append(fit)
        return popScore

    def fitness(self, instance, individual):

        satisfiedClauses = instance.checkAssignment(individual)
        # return satisfiedClauses
        # fitness is summary weight if formula is satisfied, 0 otherwise
        if (instance.clausesCount - satisfiedClauses) == 0:
            return instance.getAssignmentWeight(individual)
        else:
            return satisfiedClauses - instance.clausesCount

    def writeGenerationResult(self, pop, stats, gen):
        path = self.path
        filename = self.filename
        pos = self.filename.split("?")
        filepath = path + pos[0] + str(self.uniqueRunId) + pos[1]

        c = "generation: " + str(gen) + "\n" + "stats:" + str(stats)

        timestamp = datetime.now().strftime("%A, %d %b %Y %H:%M:%S %p")
        # c = c + "time: " + timestamp + "\n"\
        # c = c + "\n" + "population: " + str(pop)

        c =  c + "\n"

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

    def writeLatexOutput(self, pop, stats, gen):
        path = self.path
        filename = self.filename[:self.filename.rfind(".")]

        t = ["best", "worst", "average"]

        for i in range(len(t)):
            fn = filename + "_" + t[i] + ".tikz"

            pos = fn.split("?")
            filepath = path + pos[0] + str(self.uniqueRunId) + pos[1]

            c = "(" + str(gen) + ", " + str(stats[i]) + ")"

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
    #
    def writeLatexErrorOutput(self, pop, stats, gen, opt):
        path = self.path
        filename = self.filename[:self.filename.rfind(".")]

        fn = filename + "_" + "ERROR" + ".tikz"

        pos = fn.split("?")
        filepath = path + pos[0] + str(self.uniqueRunId) + pos[1]

        c = "(" + str(gen) + ", " + str(1-stats[0]/opt) + ")"

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
    #

    # Print iterations progress
    def print_progress(self, iteration, total, prefix='', suffix='', decimals=1, bar_length=100):
        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            bar_length  - Optional  : character length of bar (Int)
        """
        str_format = "{0:." + str(decimals) + "f}"
        percents = str_format.format(100 * (iteration / float(total)))
        filled_length = int(round(bar_length * iteration / float(total)))
        bar = '█' * filled_length + '-' * (bar_length - filled_length)

        sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),

        if iteration == total:
            sys.stdout.write('\n')
        sys.stdout.flush()

    def createId(self):
        def checkIfPathExists(path):
            return os.path.exists(path)
        i = 1
        pos = self.filename.split("?")
        p = pos[1].split(".")
        prefix = self.path + pos[0] + str(i) + p[0]
        while checkIfPathExists(prefix + "." + p[1]) or checkIfPathExists(prefix + "_best.tikz") or checkIfPathExists(prefix + "_average.tikz") or checkIfPathExists(prefix + "worst.tikz"):
            i = i + 1
            prefix = self.path + pos[0] + str(i) + p[0]
        return i













