import os
import time
from datetime import datetime

from statistics import mean


class SatSolverGenetics:

    # SatSolver object is used to run a certain SatStrategy on a given set of instances.
    # The instances are read from the path specified.
    # The instances are expected to be as described here: https://moodle-vyuka.cvut.cz/mod/assign/view.php?id=48024

    # an instance is created by inputParser and is of type: [<int> variables, <List<int>> weights, List<List<int>> clauses]
    def __init__(self, strategy, instance, outputPath, **options):
        self.strategy = strategy
        self.instance = instance
        self.options = options
        return

    def init(self):
        print("initializing sat solver...")
        print("reading instance data...")

    def run(self):
        self.strategy.run(self.instance)







