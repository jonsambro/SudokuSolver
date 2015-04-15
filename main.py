import copy
from graphics import *
from os import listdir


class Sudoku:

    def __init__(self, puzzle):
        self.puzzle = copy.copy(puzzle)
        self.original = copy.copy(puzzle)
        self.win = GraphWin('Sudoku', 500, 500)
        self.texto = []
        textrow = []
        for i, row in enumerate(self.puzzle):
            for j, num in enumerate(row):
                if num != 0:
                    textrow.append(
                        Text(Point(j * 50 + 50, i * 50 + 50), str(num)))
                else:
                    textrow.append(Text(Point(j * 50 + 50, i * 50 + 50), ""))
            self.texto.append(copy.copy(textrow))
            textrow = []

        for i in range(10):
            hline = Line(Point(25 + 50 * i, 25), Point(25 + 50 * i, 475))
            hline.draw(self.win)

            vline = Line(Point(25, 25 + 50 * i), Point(475, 25 + 50 * i))
            vline.draw(self.win)

            if i % 3 == 0:
                hline.setWidth(10)
                vline.setWidth(10)

    @classmethod
    def fromScratch(cls, name):
        inwin = GraphWin('NewSudoku', 500, 600)

        entryob = [[]]
        for i in range(9):
            for j in range(9):
                entryob[i].append(Entry(Point(j * 50 + 50, i * 50 + 50), 1))
                entryob[i][j].draw(inwin)
            entryob.append([])

        for i in range(10):
            hline = Line(Point(25 + 50 * i, 25), Point(25 + 50 * i, 475))
            hline.draw(inwin)

            vline = Line(Point(25, 25 + 50 * i), Point(475, 25 + 50 * i))
            vline.draw(inwin)

            if i % 3 == 0:
                hline.setWidth(10)
                vline.setWidth(10)

        Rectangle(Point(270, 500), Point(500, 600)).draw(inwin)
        Text(Point(375, 550), 'Done').draw(inwin)

        f = open('Puzzles/' + name, 'w')
        done = False
        while not(done):
            m = inwin.getMouse()

            if m.getX() > 270 and m.getY() > 500:
                for i, row in enumerate(entryob):
                    for j, e in enumerate(row):
                        t = e.getText()
                        if t == '':
                            f.write("0")
                        else:
                            f.write(t)
                        if j != 8:
                            f.write(",")
                        elif i != 8:
                            f.write("\n")
                f.close()
                done = True

        inwin.close()

        return cls(getPuzzle(name))

    def puzzleComplete(self):

        complete = True
        for row in self.puzzle:
            if 0 in set(row):
                complete = False
                break
        return complete

    def printPuzzle(self):
        for row in self.puzzle:
            print row

    def drawPuzzle(self):
        for row in self.texto:
            for i in row:
                i.draw(self.win)

    def checkPuzzle(self, newNum, rowNum, colNum):
        col = []
        square = []

        rSq = rowNum % 3
        cSq = colNum % 3

        # Checks Squares
        if rSq == 0:
            if cSq == 0:
                for i in range(3):
                    for j in range(3):
                        square.append(self.puzzle[rowNum + i][colNum + j])
            elif cSq == 1:
                for i in range(3):
                    for j in range(-1, 2):
                        square.append(self.puzzle[rowNum + i][colNum + j])
            elif cSq == 2:
                for i in range(3):
                    for j in range(-2, 1):
                        square.append(self.puzzle[rowNum + i][colNum + j])

        elif rSq == 1:
            if cSq == 0:
                for i in range(-1, 2):
                    for j in range(3):
                        square.append(self.puzzle[rowNum + i][colNum + j])
            elif cSq == 1:
                if cSq == 0:
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            square.append(self.puzzle[rowNum + i][colNum + j])
            elif cSq == 2:
                if cSq == 0:
                    for i in range(-1, 2):
                        for j in range(-2, 1):
                            square.append(self.puzzle[rowNum + i][colNum + j])
        elif rSq == 2:
            if cSq == 0:
                for i in range(-2, 1):
                    for j in range(3):
                        square.append(self.puzzle[rowNum + i][colNum + j])
            elif cSq == 1:
                for i in range(-2, 1):
                    for j in range(-1, 2):
                        square.append(self.puzzle[rowNum + i][colNum + j])
            elif cSq == 2:
                for i in range(-2, 1):
                    for j in range(-2, 1):
                        square.append(self.puzzle[rowNum + i][colNum + j])

        for row in self.puzzle:
            col.append(row[colNum])

        if newNum in set(self.puzzle[rowNum]):
            return False

        elif newNum in set(col):
            return False

        elif newNum in set(square):
            return False

        else:
            return True

    def solvePuzzle(self, i, j):
        puz = self.puzzle

        if self.puzzleComplete():
            print "The puzzle is finished!"
            return True
        elif self.original[i][j] == 0:
            for k in range(puz[i][j], 11):
                if k == 10:
                    puz[i][j] = 0
                    self.texto[i][j].setText('')
                    return False
                elif self.checkPuzzle(k, i, j):
                    puz[i][j] = k
                    self.texto[i][j].setText(str(k))

                    if j != 8:
                        if self.solvePuzzle(i, j + 1):
                            return True
                    else:
                        if self.solvePuzzle(i + 1, 0):
                            return True
        else:
            if j != 8:
                return self.solvePuzzle(i, j + 1)
            else:
                return self.solvePuzzle(i + 1, 0)


def getPuzzle(n):
    n = "Puzzles/" + n
    print n
    f = open(n, 'r')
    x = []
    for i in f:
        x = x + [i.strip('\n').split(',')]
    for row in x:
        for i, val in enumerate(row):
            row[i] = int(val)
    return x


print ("Please enter the name of the puzzle you wish to solve " +
       "(type list to list puzzle names): ")
done = False
while not(done):
    try:
        diff = raw_input()
        if diff != "list":
            puz = getPuzzle(diff)
            mySudoku = Sudoku(puz)
            done = True
        else:
            print (os.listdir("Puzzles"),
                   "\n", "Please enter one of the above names")
    except IOError:
        makeNew = raw_input(
            "That file does not exist. " +
            "Would you like to create a new puzzle? [Y/N]: ")
        while not(done):
            if makeNew == "Y":
                mySudoku = Sudoku.fromScratch(diff)
                done = True
            elif makeNew == "N":
                print (os.listdir("Puzzles"),
                       "\n", "Please enter one of the above names")
                break

            else:
                makeNew = raw_input(
                    "That input was not recognized, try again: ")

mySudoku.drawPuzzle()
print "\n"
mySudoku.solvePuzzle(0, 0)
try:
    raw_input()
except SyntaxError:
    pass
mySudoku.win.close()
