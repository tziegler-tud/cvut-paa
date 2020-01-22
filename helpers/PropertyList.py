import os


class PropertyList:

    def __init__(self):
        self.data = {}

    def addItem(self, key, value):
        self.data[key] = value

    def getData(self):
        return self.data

    def clear(self):
        self.data = {}

    def createOutputListFile(self, filepath):
        index = filepath.rfind("/")
        path = filepath[:index]
        filename = filepath[index]

        c = ""
        for k, v in self.data.items():
            c = c + "(" + str(k) + "," + str(v) + ")"

        if path == "stdout":
            print(c)
        else:
            try:
                if not os.path.exists(path):
                    os.makedirs(path)
                solution = open(filepath, "w+")
                solution.write(c)
            except:
                print("Error: failed to write solution file at " + filepath + ". Check file system permissions.")