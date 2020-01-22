from helpers.generateLatexOutput import GenerateLatexOutput
from helpers.averager import Averager
from helpers.summaryCost import SummaryCost
from helpers.summaryWeight import SummaryWeight

import os



class App:
    def run(self):

        c = ""

        path = "out"
        filepath = "out/averages.tz"

        avgList = []

        #light
        # data = [1579.26, 1522.9, 1461.49, 1461.13, 1443.57, 1413.02, 1442.58, 1394.76, 1447.64, 1419.42, 1314.28, 1281.32, 1302.73, 1287.02, 1301.29, 1291.62, 1274.26, 1262.63, 1268.1]

        #heavy
        data = [1587.88, 1620.46, 1616.03, 1640.96, 1640.08, 1666.32, 1520.1, 1553.07, 1624.53, 1536.03, 1456.4, 1244.07, 1246.69, 1087.39, 942.06, 935.05, 833.8, 821.53, 686.5]

        # set = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        # set = ["uni", "corr", "strong"]

        # set = ["light01", "light02", "light03", "light04", "light05", "light06", "light07", "light08", "light09", "light1", "light2", "light3", "light4", "light5", "light6", "light7", "light8", "light9", "light10"]
        set = ["heavy01", "heavy02", "heavy03", "heavy04", "heavy05", "heavy06", "heavy07", "heavy08", "heavy09", "heavy1", "heavy2", "heavy3", "heavy4", "heavy5", "heavy6", "heavy7", "heavy8", "heavy9", "heavy10"]

        for i in set:
            # generateLatexOutput = GenerateLatexOutput("(4,0.13493975903614458)(10,0.018066284575130823)(15,0.007310924369747899)(20,0.004748660199443728)(22,0.00380723896943778)(25,0.0025945435961946695)(27,0.0024995834027662055)(30,0.002243855288594311)(32,0.0017896743570789402)(35,0.0013639702024971147)(37,0.001265636497424577)(40,0.0014192598822539949)", 0.2)
            # averager = Averager("averageData/costWeightCorr/inst15-"+str(i) + ".dat")
            # sum = SummaryCost("averageData/maxCost/inst15-"+str(i) + ".dat")
            sum = SummaryWeight("../ex3/data/granularity/inst15-"+str(i) + ".dat")
            avg_weight = int(sum.returnAverageItemWeight())

            avgList.append(avg_weight)
        for a, d in zip(avgList, data):
            c = c + "(" + str(a) + ", " + str(d) + ")"

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
        #
