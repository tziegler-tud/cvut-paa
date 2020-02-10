from ex5.classes.satInstance import SatInstance


class SolutionInputParser:

    def __init__(self):
        return

    def parseSolution(self, path, cap):

        fileNames = []
        optimalSolutions = []

        # open file
        instanceFile = open(path, "r")
        # read by line
        lines = instanceFile.readlines()

        lineIterator = iter(lines)
        i = 0

        while i < cap:
            line = next(lineIterator)
            # read first solution file name
            terms = line.split(" ")
            instanceFileName = terms[0]
            fileNames.append(instanceFileName)
            optimalSolutions.append(terms[1])
            i = i + 1
        return [fileNames, optimalSolutions]
