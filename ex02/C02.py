from operator import *
import random


class Param:
    c: float  # decision class value
    result: float  # param calculated result
    tstRowIdx: int  # tst data row index
    proper: bool = False  # flag defining selected decision
    decisionEquals: bool = False  # flag defining that if calculated decision equals expert's hidden decision

    def __init__(self, c, result, tstRowIdx):
        self.c = c
        self.result = result
        self.tstRowIdx = tstRowIdx

    def __eq__(self, o: object) -> bool:
        return self.c == o.c and self.result == o.result and self.tstRowIdx == o.tstRowIdx and self.proper == o.proper

    def __ne__(self, o: object) -> bool:
        return self.c != o.c or self.result != o.result or self.tstRowIdx != o.tstRowIdx or self.proper != o.proper

    #  only for debugging
    def toString(self):
        print(
            f'C = {self.c} : {self.result}  ; proper: {self.proper} ; decEQ: {self.decisionEquals}       ; idx: {self.tstRowIdx}')


class Bayes:
    tstFileLines: [float] = []
    trnFileLines: [float] = []
    separator: str = ' '
    results: [Param] = []

    def __init__(self, tstFileName, trnFileName):
        #  reading tst and trn data files to double dimensional arrays (easier to operate while making calculations)
        for line in open(tstFileName, "r").readlines():
            lineArr = line.replace('\n', '').split(self.separator)
            lineArr.remove(lineArr[len(lineArr) - 1])  # removes empty space at end of line (caused by data_splitter)
            self.tstFileLines.append(list(map(float, lineArr)))
        for line in open(trnFileName, "r").readlines():
            lineArr = line.replace('\n', '').split(self.separator)
            lineArr.remove(lineArr[len(lineArr) - 1])
            self.trnFileLines.append(list(map(float, lineArr)))
        pass

    def main(self):

        #  calculating param values
        idx: int = 0
        for x in self.tstFileLines:
            for c in self.getDecisionClasses():
                linesForC = self.getLinesWithClass(self.trnFileLines, c)
                linesForCCount = len(linesForC)
                trnLinesCount = len(self.trnFileLines)
                sumOfLinesCountForCAndA = 0
                xColIdx = 0
                for a in x[:-1]:
                    linesCountForCAndA = self.countLinesForAttributeValue(linesForC, xColIdx, a)
                    sumOfLinesCountForCAndA = sumOfLinesCountForCAndA + linesCountForCAndA
                    xColIdx = xColIdx + 1
                result = (sumOfLinesCountForCAndA / linesForCCount) * (linesForCCount / trnLinesCount)
                self.results.append(Param(c, result, idx))
            idx = idx + 1

        #  calculating decisions
        for idx in range(len(self.tstFileLines)):
            tstParamsForIdx: [Param] = list(filter(lambda item: item.tstRowIdx == idx, self.results))
            paramDecision: Param = self.findParamWithProperDecision(tstParamsForIdx)
            found: Param = next((p for p in self.results if p == paramDecision), None)
            if found is not None:
                found.proper = True
                found.decisionEquals = self.tstFileLines[idx][-1] == found.c

        #  debugging only
        p: Param
        for p in self.results:
            print(p.toString())

        #  calculating global accuracy
        countOfProperQualifiedTstObjects: int = len(list(filter(lambda p: p.decisionEquals, self.results)))
        countOfQualifiedTstObjects: int = len(self.tstFileLines)
        glAcc = f'{countOfProperQualifiedTstObjects / countOfQualifiedTstObjects}'

        #  calculating balanced accuracy
        sumOfClassesAccuracy: float = 0
        countOfDecisionClasses = len(self.getDecisionClasses())
        for c in self.getDecisionClasses():
            countOfProperQualifiedTstObjectsInClass: int = len(
                list(filter(lambda p: p.decisionEquals == True and p.c == c, self.results)))
            countOfTstObjectWithClass: int = len(self.getLinesWithClass(self.tstFileLines, c))
            sumOfClassesAccuracy = sumOfClassesAccuracy + (
                    countOfProperQualifiedTstObjectsInClass / countOfTstObjectWithClass)
        balAcc = f'{sumOfClassesAccuracy / countOfDecisionClasses}'

        #  writing accuracies to file (CSV format)
        accFile = open("acc_bayes.txt", "w+")
        accFile.writelines(["global_accuracy;balanced_accuracy\n", f'{glAcc};{balAcc}'])
        accFile.close()

        #  writing decisions to file (CSV format)
        decLines: [str] = ["obiekt_tst;ukryta_decyzja_eksperta;decyzja_klasyfikatora\n"]
        for idx in range(len(self.tstFileLines)):
            decLines.append(
                f'x{idx + 1};{self.tstFileLines[idx][-1]};{list(filter(lambda p: p.tstRowIdx == idx and p.proper == True, self.results))[0].c}\n')
        decFile = open("dec_bayes.txt", "w+")
        decFile.writelines(decLines)
        decFile.close()

    #  util methods

    def getDecisionClasses(self):
        values: [float] = []
        lines: [float] = self.tstFileLines + self.trnFileLines
        for line in lines:
            values.append(line[len(line) - 1])
        return self.getUniqueValues(values)

    def getUniqueValues(self, values):
        return list(set(values))

    def getLinesWithClass(self, lines, c):
        values = []
        for line in lines:
            if line[len(line) - 1] == c:
                values.append(line)
        return values

    def countLinesForAttributeValue(self, lines, colIdx, attributeValue):
        count = 0
        for line in lines:
            if line[colIdx] == attributeValue:
                count = count + 1
        return count

    def findParamWithProperDecision(self, params) -> Param:
        results = list(map(lambda p: p.result, params))
        res: Param = max(params, key=attrgetter('result'))
        if len(set(results)) == len(results):
            return res
        else:
            return random.choice(list(filter(lambda p: p.result == res.result, params)))


Bayes("data/australian_TST.txt", "data/australian_TRN.txt").main()
