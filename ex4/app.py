from ex4.classes.knapSolver import KnapSolver
from ex4.classes.knapSolverGenetics import KnapSolverGenetics
from ex4.strategy.knapStrategy import KnapStrategy
from ex4.strategy.geneticStrategy import GeneticStrategy
from ex4.knap_enums.knaptype_enum import KnapTypeEnum
from helpers.PropertyList import PropertyList


class App:
    def run(self):

        # sets = ["ZKC30_10"]
        # sets = ["test30"]
        i = "test30"
        # i = "ZKC30_10"
        experiment = "mutationDetails0"

        # vals = [2125,2375,2625,2750,2875,3125,3250,3375,3625,3750,3875,4125, 4250, 4375,4625,4750,4875]
        # vals = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1]
        # vals = [0.5, 0.55, 0.6, 0.625, 0.65, 0.675, 0.7, 0.725, 0.75, 0.775, 0.8, 0.825, 0.85, 0.875, 0.9, 0.925, 0.95, 0.975, 1]
        # vals = [0, 0.02 ,0.2]
        vals = [0.2]

        generationCap = 500
        populationSize = 50
        instanceSize = 30
        elitism = 1
        crossoverRate = 0.8
        mutationRate = 0.01

        enablePlot = False
        parameter = "genetic"

        maxErrorList = PropertyList()
        avgErrorList = PropertyList()

        for v in vals:
            knapStrategy = GeneticStrategy("genetic", KnapTypeEnum.CONSTRUCTIVE,
                                           instanceSize=instanceSize,
                                           generationCap=generationCap,
                                           populationSize=populationSize,
                                           elitism=elitism,
                                           crossoverRate=crossoverRate,
                                           mutationRate=mutationRate,
                                           enablePlot=enablePlot,
                                           logGenerationResults=True,
                                           outputFrequency=1
                                           )

            knapSolver = KnapSolverGenetics(
                knapStrategy,
                "data/" + "genetic" + "/" + str(i) + ".dat",
                "solutions/" + experiment + "/" + str(v),
                KnapTypeEnum.CONSTRUCTIVE,
                measureRecursionDepth=True,
                measureCpuTime=False,
                measureError=True,
                # measureError=True,
                instanceSolutionPath="data/" + "genetic" + "/" + str(i) + "_sol.dat"
                )
            knapSolver.init()
            # res = [avgRecursionDepth, maxRecursionDepth, avgError, maxError]
            res = knapSolver.run()
            avgErrorList.addItem(v, res[0])
            maxErrorList.addItem(v, res[1])

        maxErrorList.createOutputListFile("results/" + "genetic" + "/" + experiment + "/maxError.dat")
        avgErrorList.createOutputListFile("results/" + "genetic" + "/" + experiment + "/avgError.dat")
