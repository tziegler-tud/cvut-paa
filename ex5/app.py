from ex5.classes.SatSolverGenetics import SatSolverGenetics
from ex5.classes.InputParser import InputParser
from ex5.classes.SolutionInputParser import SolutionInputParser
from ex5.classes.geneticStrategy import GeneticStrategy
from helpers.PropertyList import PropertyList

import statistics


class App:
    def run(self):

        generationCap = 10000
        populationSize = 100
        instanceSize = 50
        elitism = 5
        crossoverRate = 0.9
        mutationRate = 0.01

        enablePlot = False
        parameter = "genetic"
        experiment = "qualityM20"

        avgErrorList = PropertyList()
        avgGenList = PropertyList()

        errorList = []
        genList = []

        # read solutions and associated file names
        # solFile = "data/genetic/wuf-M/wuf50-201-M-opt.dat"
        # solFile = "data/genetic/wuf-N/wuf50-201-N-opt.dat"
        solFile = "data/genetic/wuf-M/wuf20-78-M-opt.dat"
        # solFile = "data/genetic/wuf-N/wuf20-78-N-opt.dat"
        # solFile = "data/genetic/wuf-Q/wuf20-78-Q-opt.dat"
        # solFile = "data/genetic/wuf-Q/wuf50-201-Q-opt.dat"
        solIP = SolutionInputParser()
        cap = 33
        # solData = [<List> filenames, <list> optimalSolutions]
        solData = solIP.parseSolution(solFile, cap)
        for v in [500]:

            for index, filename in enumerate(solData[0]):
                print("processing file: " + str(index) + "/" + str(cap))
                # set instance filename
                fn = filename
                sol = int(solData[1][index])
                # parse input file
                ip = InputParser()
                path = "data/genetic/wuf-M/wuf20-78-M/w" + fn + ".mwcnf"
                # path = "data/genetic/wuf-M/wuf50-201-M/w" + fn + ".mwcnf"
                # path = "data/genetic/wuf-N/wuf50-201-N/w" + fn + ".mwcnf"
                # path = "data/genetic/wuf-N/wuf20-78-N/w" + fn + ".mwcnf"
                # path = "data/genetic/wuf-Q/wuf20-78-Q/w" + fn + ".mwcnf"
                # path = "data/genetic/wuf-Q/wuf50-201-Q/w" + fn + ".mwcnf"
                satInstance = ip.parseMWCNF(path)

            # set instance path
            # path = "data/genetic/wuf-M/wuf20-78-M/wuf20-01.mwcnf"
            # path = "data/genetic/wuf-M/wuf50-201-M/wuf50-012.mwcnf"
            # path = "data/genetic/wuf-Q/wuf20-78-Q/wuf20-02.mwcnf"
            # path = "data/genetic/wuf-A/wuf20-88-A/wuf20-018-A.mwcnf"

            # read input
            # ip = InputParser()
            # satInstance = ip.parseMWCNF(path)



                satStrategy = GeneticStrategy(instanceSize=instanceSize,
                                              generationCap=v,
                                              populationSize=populationSize,
                                              elitism=elitism,
                                              crossoverRate=crossoverRate,
                                              mutationRate=mutationRate,
                                              enablePlot=False,
                                              logGenerationResults=False,
                                              outputFrequency=1,
                                              scaleMax = 5
                                              )
                # res = [generations, popSize, best score]
                res = satStrategy.run(satInstance, False)

                # calc relative error
                relError = 1 - (res[2]/sol)
                errorList.append(relError)
                genList.append(res[0])

            print("\n")
            print("avg error: " + str(statistics.mean(errorList)))
            print("avg generations: " + str(statistics.mean(genList)))

            avgErrorList.addItem(v, statistics.mean(errorList))
            avgGenList.addItem(v, statistics.mean(genList))
    #
    # maxErrorList.createOutputListFile("results/" + "genetic" + "/" + experiment + "/maxError.dat")
        avgErrorList.createOutputListFile("results/" + "genetic" + "/" + experiment + "/avgError.dat")
        avgGenList.createOutputListFile("results/" + "genetic" + "/" + experiment + "/avgGen.dat")
