from ex1.classes.knapSolver import KnapSolver
from ex1.strategy.knapStrategy import KnapStrategy
from ex1.strategy.bruteforce import BruteForceStrategy

from ex1.knap_enums.knaptype_enum import KnapTypeEnum


class App:
    def run(self):
        knapStrategy = BruteForceStrategy("testStrategy", KnapTypeEnum.DECISIVE)
        knapSolver = KnapSolver(knapStrategy, "data/NR/NR10_inst.dat", KnapTypeEnum.DECISIVE)
        knapSolver.init()
        knapSolver.run()

