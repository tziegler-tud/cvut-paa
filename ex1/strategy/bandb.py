from ex1.strategy.knapStrategy import KnapStrategy
from ex1.knap_enums.knaptype_enum import KnapTypeEnum


class Bandb(KnapStrategy):
    def __init__(self, name, knaptype):
        KnapStrategy.__init__(self, name, knaptype)
        self.StrategyType = "Branch & Bound"

