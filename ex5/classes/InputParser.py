from ex5.classes.satInstance import SatInstance


class InputParser:

    def __init__(self):
        return

    def parseMWCNF(self, path):
        # open file
        instanceFile = open(path, "r")
        # read by line
        lines = instanceFile.readlines()

        hasPs = False
        hasW = False
        weights = []

        problemDesc = ""
        variables = None
        clausesCount = None

        clauses = []

        lineIterator = iter(lines)

        for l in lineIterator:
            # find out line type by looking at first letter
            # ignore comments
            if l[0] == "c":
                continue

            # find problem statement first - if first entry is not ps, fail
            if l[0] == "p":

                hasPs = True
                # remove line identifier + whitespace
                t = l[1:]
                while t[0] == " ":
                    # remove leading whitespace, if any
                    t = t[1:]
                # split by whitespace to obtain tokens
                terms = t.split(" ")
                problemDesc = terms[0]
                variables = int(terms[1])
                clausesCount = int(terms[2])

                if problemDesc != "mwcnf":
                    raise ValueError('Instance is not of type mwcnf!')
                continue

            if l[0] == "w":
                if not hasPs:
                    raise ValueError('Failed to parse Input: problem statement not first line')
                # read problem statement
                # remove line identifier
                t = l[1:]
                while t[0] == " ":
                    # remove leading whitespace, if any
                    t = t[1:]
                # split by whitespace to obtain tokens
                terms = t.split(" ")
                weights = []
                for split in terms:
                    if len(split) == 0:
                        continue
                    while split[0] == " ":
                        # remove leading whitespace, if any
                        split = split[1:]
                    weights.append(int(split))
                # parse to int to remove line breaks, etc...
                while weights[len(weights)-1] != 0:
                    # end not reached, checking next line
                    nextLine = next(lineIterator)
                    # no line identifier expected here, but checking for safety reasons...
                    if nextLine[0] == "w":
                        nextLine = nextLine[1:]
                        if nextLine[0] == " ":
                            # remove leading whitespace, if any
                            nextLine = nextLine[1:]
                    # find terms and check for 0 at the end
                    terms = nextLine.split(" ")
                    for split in terms:
                        weights.append(int(split))
                # all weights read, removing trailing 0
                checkForZero = int(weights.pop())
                if checkForZero != 0:
                    raise ValueError('Expected weights to be ended by 0, but ' + str(checkForZero) + 'found')
                # check if number of weights equals number of variables
                if len(weights) != variables:
                    raise ValueError('Number of weights and variables dont match: ' + str(len(weights)) + "weights found and " + str(variables) + "found.")
                # alright, weights are set correctly! Now, we expect the clauses to follow.
                for i in range(clausesCount):
                    clauseLine = next(lineIterator)
                    if clauseLine[0] == "c":
                        clauseLine = next(lineIterator)
                    while clauseLine[0] == " ":
                        clauseLine = clauseLine[1:]
                    # we expect at most 3 variables
                    # variable identifiers are seperated by white space, tab or newline
                    clauseIt = iter(clauseLine)
                    readBuffer = ""
                    terms = []
                    for c in clauseIt:
                        if c == " " or c== "\n" or c == "\t":
                            # seperator found
                            terms.append(int(readBuffer))
                            readBuffer = ""
                        else:
                            if c == "0" and readBuffer == "":
                                # End of clause reached
                                clauses.append(terms)
                                break
                            else:
                                readBuffer = readBuffer + c
                # clauses succesfully read. We have everythin we need. Lets ignore the rest of the file.
                return SatInstance(variables, weights, clauses)
