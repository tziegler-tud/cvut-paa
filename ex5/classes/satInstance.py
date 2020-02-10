class SatInstance:

    def __init__(self, variables, weights, clauses):
        self.variables = variables
        self.weights = weights
        self.clauses = clauses
        self.clausesCount = len(clauses)
        self.summaryWeight = self.calcSummaryWeight(weights)

    def isSatisfied(self, assignment):
        # assignment is bool list of variables
        # check if assignment has as many variables as instance
        if len(assignment) != self.variables:
            raise ValueError("Assignment and instance variables do not match!")

        # in order for the formula to be satisfied, every clause must evaluate to true.
        for c in self.clauses:
            if not self.checkClause(c, assignment):
                return False
        return True

    def checkClause(self, clause, assignment):
        # one literal must be true in order for the clause to be true.
        for lit in clause:
            if lit < 0:
                # negated variable
                if not assignment[-1*lit - 1]:
                    return True
            else:
                if assignment[lit - 1]:
                    return True
        return False

    def calcSummaryWeight(self, weights):
        s = 0
        for w in weights:
            s = s + w
        return s

    def getSummaryWeight(self):
        return self.summaryWeight

    def getAssignmentWeight(self, assignment):
        # if len(assignment) != self.variables:
        #     raise ValueError("Assignment and instance variables do not match!")
        s = 0
        for index, var in enumerate(assignment):
            if var:
                s = s + self.weights[index]
        return s

    def checkAssignment(self, assignment):
        # assignment is bool list of variables
        # check if assignment has as many variables as instance
        # if len(assignment) != self.variables:
        #     raise ValueError("Assignment and instance variables do not match!")

        satisfiedClauses = 0
        # count the number of satisfied clauses
        for c in self.clauses:
            if self.checkClause(c, assignment):
                satisfiedClauses = satisfiedClauses + 1

        return satisfiedClauses

