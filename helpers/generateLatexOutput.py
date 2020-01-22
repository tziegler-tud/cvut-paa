class GenerateLatexOutput:

    def __init__(self, string, maxError):
        self.string = string
        self.maxError = maxError
        n = self.genData(string)
        r = self.transformData()
        c = ""

        for i in range(0, len(r)):
            c = c + "(" + str(n[i]) + "," + str(r[i]) + ")"
        print(c)

    def genData(self, string):
        split = string.split("(")
        split.pop(0)
        l = len(split)
        self.n = [0 for i in range(0, l)]
        self.v = [0 for i in range(0, l)]

        for i in range(0, len(split)):
            s = split[i].split(",")
            self.n[i] = s[0]
            self.v[i] = s[1][:-1]
        return self.n

    def transformData(self):

        r = [0 for i in range(0, len(self.v))]
        for i in range(len(self.v)):
            r[i] = float(self.v[i]) / float(self.maxError)

        return r
