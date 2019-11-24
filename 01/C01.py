from enum import Enum
import statistics

class ColumnDataType(Enum):
     STRING = 's',
     NUMBER = 'n'

class C01:
    typeFileLines = None
    dataFileLines = None
    separator = ' '
    columnNameSymbol = 'a'

    def __init__(self, typeFileName, dataFileName):
        self.typeFileLines = []
        self.dataFileLines = []
        for line in open(typeFileName, "r").readlines():
            self.typeFileLines.append(line.replace('\n', ''))
        for line in open(dataFileName, "r").readlines():
            self.dataFileLines.append(line.replace('\n', ''))
        pass

    def main(self):
        lastColumnValues = self.getValuesForColumn(self.getLastColumnIndex(self.dataFileLines))
        uniqueValues = self.getUniqueValues(lastColumnValues)
        print('Istniejące klasy decyzyjne: ', uniqueValues)
        print('\n')

        print('Wielkość klas decyzyjnych:')
        for value in uniqueValues:
            print(value, ': ', self.getCountOfValue(lastColumnValues, value))
        print('\n')

        print('Indeksy kolumn o typie NUMERYCZNYM: ', self.getColumnIndexesByType(ColumnDataType.NUMBER))
        print('Indeksy kolumn o typie TEKSTOWYM: ', self.getColumnIndexesByType(ColumnDataType.STRING))
        print('\n')

        maxDict = self.getMaxValuesForColumns(self.getColumnIndexesByType(ColumnDataType.NUMBER))
        minDict = self.getMinValuesForColumns(self.getColumnIndexesByType(ColumnDataType.NUMBER))
        print('Maksymalne wartości dla atrybutów numerycznych:\n', maxDict)
        print('Minimalne wartości dla atrybutów numerycznych:\n', minDict)
        print('\n')

        print('Liczba różnych dostępnych wartości wszystkich atrybutów:')
        uniqueValuesDict = self.getUniqueValuesCountForColumns(self.getAllColumnIndexes(self.dataFileLines))
        for key in uniqueValuesDict.keys():
            print(f'{key}: {uniqueValuesDict[key]}')
        print('\n')

        print('Lista różnych dostępnych wartości wszystkich atrybutów:')
        uniqueValuesDict = self.getUniqueValuesForColumns(self.getAllColumnIndexes(self.dataFileLines))
        for key in uniqueValuesDict.keys():
            print(f'{key}: {uniqueValuesDict[key]}')
        print('\n')

        print('Odchylenia standardowe dla poszczegolnych atrybutow numerycznych:')
        stdDevNumeric = self.getStandardDeviationForColumnIndexes(self.getColumnIndexesByType(ColumnDataType.NUMBER))
        for key in stdDevNumeric.keys():
            print(f'{key}: {stdDevNumeric[key]}')
        print('\n')

        print('Odchylenia standardowe dla poszczegolnych atrybutow numerycznych dla poszczególnych klas decyzyjnych:')
        stdDevClasses = self.calculateStdDevForClassesForColumnIndexes(self.getColumnIndexesByType(ColumnDataType.NUMBER))
        for key in stdDevClasses.keys():
            print(f'{key}: {stdDevClasses[key]}')
        print('\n')

    def getLastColumnIndex(self, lines: list):
        return len(lines[0].split(self.separator)) - 1

    def getValuesForColumn(self, columnIndex):
        values = []
        for line in self.dataFileLines:
            values.append(line.split(self.separator)[columnIndex])
        return values

    def getValuesForColumnWithLines(self, columnIndex, lines = None):
        values = []
        for line in lines:
            values.append(line.split(self.separator)[columnIndex])
        return values

    def filterLinesByLastColumnValue(self, value, lines = None):
        filteredLines = []
        lines = self.dataFileLines if lines is None else lines
        columnIndex = self.getLastColumnIndex(lines)
        for line in lines:
            if line.split(self.separator)[columnIndex] == value:
                filteredLines.append(line)
        return filteredLines

    def getAllColumnIndexes(self, lines):
        return range(len(lines[0].split(self.separator)))

    def getUniqueValues(self, values):
        return list(set(values))

    def getCountOfValue(self, array, value):
        return array.count(value)

    def getColumnIndexesByType(self, dataType: ColumnDataType):
        typeIndexes = []
        for line in self.typeFileLines:
            readType = line.split(self.separator)[1]
            if (type(readType) is not str):
                raise TypeError('Invalid data type or no data')
            if (readType == dataType.value[0]):
                typeIndexes.append(int(line.split(self.separator)[0].split(self.columnNameSymbol)[1]) - 1)
        return typeIndexes

    def getMinValueForColumn(self, columnIndex):
        return min(map(lambda item: float(item), self.getValuesForColumn(columnIndex)))

    def getMaxValueForColumn(self, columnIndex):
        return max(map(lambda item: float(item), self.getValuesForColumn(columnIndex)))

    def getMinValuesForColumns(self, columnIndexes):
        dict: dict = {}
        for index in columnIndexes:
            dict[f'{self.columnNameSymbol}{(index + 1)}'] = self.getMinValueForColumn(index)
        return dict

    def getMaxValuesForColumns(self, columnIndexes):
        dict: dict = {}
        for index in columnIndexes:
            dict[f'{self.columnNameSymbol}{(index + 1)}'] = self.getMaxValueForColumn(index)
        return dict

    def getUniqueValuesForColumns(self, columnIndexes: [int]):
        dict: dict = {}
        for index in columnIndexes:
            dict[f'{self.columnNameSymbol}{(index + 1)}'] = self.getUniqueValues(self.getValuesForColumn(index))
        return dict

    def getUniqueValuesCountForColumns(self, columnIndexes: [int]):
        uniqueValuesDict = self.getUniqueValuesForColumns(columnIndexes)
        for key in uniqueValuesDict.keys():
            uniqueValuesDict[key] = len(uniqueValuesDict[key])
        return uniqueValuesDict

    def getStandardDeviation(self, items):
        return statistics.stdev(items)

    def getStandardDeviationForColumnIndexes(self, columnIndexes):
        dict: dict = {}
        for index in columnIndexes:
            dict[f'{self.columnNameSymbol}{(index + 1)}'] = self.getStandardDeviation(map(lambda item: float(item), self.getValuesForColumn(index)))
        return dict

    def getStandardDeviationForColumnIndexesAndLines(self, columnIndexes, lines = None):
        dict: dict = {}
        for index in columnIndexes:
            dict[f'{self.columnNameSymbol}{(index + 1)}'] = self.getStandardDeviation(map(lambda item: float(item), self.getValuesForColumnWithLines(index, lines)))
        return dict

    def calculateStdDevForClassesForColumnIndexes(self, columnIndexes):
        stdDevAttributesDict: dict = {}
        decisionClasses: [int] = self.getUniqueValues(self.getValuesForColumn(self.getLastColumnIndex(self.dataFileLines)))
        for classValue in decisionClasses:
            filteredLines = self.filterLinesByLastColumnValue(classValue, self.dataFileLines)
            stdDevAttributesDict[classValue] = self.getStandardDeviationForColumnIndexesAndLines(columnIndexes, filteredLines)
        return stdDevAttributesDict


C01("data/australian-type.txt", "data/australian.txt").main()
