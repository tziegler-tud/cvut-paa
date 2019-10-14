from ex1.classes.knapSolver import KnapSolver
from ex1.strategy.knapStrategy import KnapStrategy
from ex1.strategy.bruteforce import BruteForceStrategy
from ex1.strategy.bandb import BandbStrategy

from ex1.knap_enums.knaptype_enum import KnapTypeEnum


class App:
    def run(self):
        knapStrategy = BandbStrategy("BranchAndBound", KnapTypeEnum.DECISIVE)
        # knapStrategy = BruteForceStrategy("Bruteforce-Naive", KnapTypeEnum.DECISIVE)

        # knapSolver = KnapSolver(knapStrategy, "data/NR/NR4_inst.dat", "solutions/NR", KnapTypeEnum.DECISIVE)
        # knapSolver.init()
        # knapSolver.run()
        #
        knapSolver = KnapSolver(knapStrategy, "data/NR/NR20_inst.dat", "solutions/NR/bandb", KnapTypeEnum.DECISIVE)
        knapSolver.init()
        knapSolver.run()

        # knapSolver = KnapSolver(knapStrategy, "data/NR/NR15_inst.dat", "solutions/NR", KnapTypeEnum.DECISIVE)
        # knapSolver.init()
        # knapSolver.run()

