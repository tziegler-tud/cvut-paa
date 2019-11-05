from ex2.classes.knapSolver import KnapSolver
from ex2.strategy.knapStrategy import KnapStrategy
from ex2.strategy.heuristic import SimpleHeuristicStrategy
from ex2.strategy.extendedHeuristic import ExtendedHeuristicStrategy

from ex2.knap_enums.knaptype_enum import KnapTypeEnum


class App:
    def run(self):

        sets = [4, 10, 15, 20, 22, 25, 27, 30, 32, 35, 37, 40]
        # knapStrategy = ExtendedHeuristicStrategy("extendedHeuristic", KnapTypeEnum.CONSTRUCTIVE)
        knapStrategy = SimpleHeuristicStrategy("simpleHeuristic", KnapTypeEnum.CONSTRUCTIVE)

        for i in sets:

            knapSolver = KnapSolver(knapStrategy, "data/ZKW/ZKW"+str(i)+"_inst.dat", "solutions/ZKW/simpleHeuristic",
                                    KnapTypeEnum.CONSTRUCTIVE, measureRecursionDepth=True, measureCpuTime=True, measureError=True,
                                    instanceSolutionPath="data/ZKW/ZKW"+str(i)+"_sol.dat")
            knapSolver.init()
            knapSolver.run()

