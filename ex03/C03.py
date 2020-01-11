import random
from ex02 import C02


class Estimate:
    dataFileLines: [float] = []
    bayesFileLines: [float] = []
    separator: str = ' '
    bayesSeparator: str = ';'

    def __init__(self, dataFileName):
        for line in open(dataFileName, "r").readlines():
            lineArr = line.replace('\n', '').split(self.separator)
            self.dataFileLines.append(list(map(float, lineArr)))

    def main(self):
        pass

    def trainAndTest(self, ratio: float = 0.5):
        if ratio < 0 or ratio > 1:
            raise Exception(f'Invalid ratio! (given: {ratio})')
        #  divide data file bo ratio
        count = int(len(self.dataFileLines) * ratio)
        trnIndexes = list(random.sample(range(len(self.dataFileLines)), count))
        tstIndexes = list(filter(lambda idx: idx not in trnIndexes, range(len(self.dataFileLines))))

        #  saving selected indexes by data file
        self.saveToFile("australian_TRN.txt", trnIndexes)
        self.saveToFile("australian_TST.txt", tstIndexes)

        #  print statistics
        print("Train & Test - statystyki podziału:\n")
        print(f'• Łączna ilość elementów: {len(self.dataFileLines)}\n• Ilość elementów TRN: {len(trnIndexes)}\n• Ilość elementów TST: {len(tstIndexes)}')

    def saveToFile(self, fileName: str, indexes: [int], baseFileLines=None):
        if baseFileLines is None:
            baseFileLines = self.dataFileLines
        file = open(fileName, "w+")
        lines: [str] = []
        for line in list(map(lambda idx: baseFileLines[idx], indexes)):
            fileLine = ""
            for item in line:
                fileLine = fileLine + f'{item} '
            lines.append(fileLine + "\n")
        file.writelines(lines)
        file.close()


Estimate("../data/australian.txt").trainAndTest()
C02.Bayes("australian_TST.txt", "australian_TRN.txt").main()