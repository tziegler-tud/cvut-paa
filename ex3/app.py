from ex3.classes.knapSolver import KnapSolver
from ex3.classes.knapSolverPermutations import KnapSolverPermutations
from ex3.strategy.knapStrategy import KnapStrategy
from ex3.strategy.heuristic import SimpleHeuristicStrategy
from ex3.strategy.extendedHeuristic import ExtendedHeuristicStrategy
from ex3.strategy.dynamic import DynamicProgrammingStrategy
from ex3.strategy.dynamicByCost import DynamicProgrammingByCostStrategy
from ex3.strategy.fptas import FptasStrategy
from ex3.strategy.bandb import BandbStrategy
from helpers.PropertyList import PropertyList

from ex3.knap_enums.knaptype_enum import KnapTypeEnum


class App:
    def run(self):

        # sets = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        # sets = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 650, 700, 750, 800, 850, 900, 950]
        sets = ["uni", "corr", "strong"]

        # sets = ["light01", "light02", "light03", "light04", "light05", "light06", "light07", "light08", "light09",
        #        "light1", "light2", "light3", "light4", "light5", "light6", "light7", "light8", "light9", "light10"]

        # sets = ["heavy01", "heavy02", "heavy03", "heavy04", "heavy05", "heavy06", "heavy07", "heavy08", "heavy09", "heavy1", "heavy2", "heavy3", "heavy4", "heavy5", "heavy6", "heavy7", "heavy8", "heavy9", "heavy10"]
        # sets = ["bal"]
        parameter = "costWeightCorr"
        # parameter = "costWeightCorr"

        # knapStrategy = ExtendedHeuristicStrategy("extendedHeuristicC", KnapTypeEnum.CONSTRUCTIVE)
        # strategy = "extHeuristic"

        # knapStrategy = DynamicProgrammingByCostStrategy("dynamicProgrammingByCost", KnapTypeEnum.CONSTRUCTIVE)
        # strategy = "dpByCost"

        # knapStrategy = DynamicProgrammingStrategy("dynamicProgramming", KnapTypeEnum.CONSTRUCTIVE)
        # strategy = "dpByWeight"

        knapStrategy = BandbStrategy("branchAndBound", KnapTypeEnum.CONSTRUCTIVE)
        strategy = "bandb"

        avgRecList = PropertyList()
        avgErrorList = PropertyList()


        for i in sets:

            knapSolver = KnapSolver(
                knapStrategy,
                "data/" + parameter + "/inst152-" + str(i) + ".dat",
                "solutions/" + strategy + "/" + parameter + "/solutions",
                KnapTypeEnum.CONSTRUCTIVE,
                measureRecursionDepth=True,
                measureCpuTime=False,
                measureError=False,
                # measureError=True,
                instanceSolutionPath="data/" + parameter + "/solutions/inst151-" + str(i) + ".dat"
                )
            knapSolver.init()
            # res = [avgRecursionDepth, maxRecursionDepth, avgError, maxError]
            res = knapSolver.run()
            avgRecList.addItem(i, res[0])
            avgErrorList.addItem(i, res[2])
        avgRecList.createOutputListFile("results/" + strategy + "/" + parameter + "/complexity.dat")
        avgErrorList.createOutputListFile("results/" + strategy + "/" + parameter + "/error.dat")

        ##################################
        #      for permutations:         #
        ##################################

        # sets = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        #
        #
        # knapStrategy = ExtendedHeuristicStrategy("extendedHeuristicC", KnapTypeEnum.CONSTRUCTIVE)
        # strategy = "extHeuristic"
        # #
        # # knapStrategy = DynamicProgrammingByCostStrategy("dynamicProgrammingByCost", KnapTypeEnum.CONSTRUCTIVE)
        # # strategy = "dpByCost"
        # #
        # # knapStrategy = DynamicProgrammingStrategy("dynamicProgramming", KnapTypeEnum.CONSTRUCTIVE)
        # # strategy = "dpByWeight"
        # #
        # # knapStrategy = BandbStrategy("branchAndBound", KnapTypeEnum.CONSTRUCTIVE)
        # # strategy = "bandb"
        #
        # stdevList = PropertyList()
        # varList = PropertyList()
        # stdErrorList = PropertyList()
        # varErrorList = PropertyList()
        #
        # for i in sets:
        #     knapSolver = KnapSolverPermutations(knapStrategy, "data/encoding/inst15-" + str(i) + ".dat",
        #                             "solutions/" + strategy + "/encoding/solutions",
        #                             KnapTypeEnum.CONSTRUCTIVE, measureRecursionDepth=True, measureCpuTime=False,
        #                             measureError=True,
        #                             instanceSolutionPath="data/encoding/solutions/inst15-" + str(i) + ".dat")
        #     knapSolver.init()
        #     # res = [stdevComplexity, varianceComplexity, stdevError, varianceError]
        #     res = knapSolver.run()
        #     stdevList.addItem(i, res[0])
        #     varList.addItem(i, res[1])
        #     stdErrorList.addItem(i, res[2])
        #     varErrorList.addItem(i, res[3])
        #
        # stdevList.createOutputListFile("results/" + strategy + "/encoding/stdev.dat")
        # varList.createOutputListFile("results/" + strategy + "/encoding/variance.dat")
        # stdErrorList.createOutputListFile("results/" + strategy + "/encoding/errorStdev.dat")
        # varErrorList.createOutputListFile("results/" + strategy + "/encoding/errorVar.dat")
