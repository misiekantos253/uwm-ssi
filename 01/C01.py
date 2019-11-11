class C01:
    file

    def __init__(self, fileName):
        self.file = open(fileName, "r")
        pass

    def main(self):
        for line in self.file.readlines():
            print(line)


excercise = C01("data/australian-type.txt")
excercise.main()
