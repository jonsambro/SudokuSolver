import copy
from graphics import *
from os import listdir

class Sudoku:

    def  __init__(self, puzzle):
        self.puzzle = copy.copy(puzzle)
        self.original = copy.copy(puzzle)
        self.win = GraphWin(Sudoku,500,500)
        self.texto = []
        textrow = []
        for i, row in enumerate(self.puzzle):
            for j, num in enumerate(row):
                if num != 0:
                    textrow.append(Text(Point(j*50 + 50, i*50 + 50), str(num)))
                else:
                    textrow.append(Text(Point(j*50 + 50, i*50 + 50), ""))
            self.texto.append(copy.copy(textrow))
            textrow = []

        for i in range(10):
            hline = Line(Point(25+50*i,25),Point(25+50*i,475))
            hline.draw(self.win)

            vline = Line(Point(25, 25+50*i),Point(475, 25+50*i))
            vline.draw(self.win)

            if i%3 == 0:
                hline.setWidth(10)
                vline.setWidth(10)

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

        rSq = rowNum%3
        cSq = colNum%3

        #Checks Squares
        if rSq == 0:
            if cSq ==0:
                for i in range(3):
                    for j in range(3):
                        square.append(self.puzzle[rowNum + i][colNum+j])
            elif cSq == 1:
                for i in range(3):
                    for j in range(-1,2):
                        square.append(self.puzzle[rowNum + i][colNum+j])
            elif cSq == 2:
                for i in range(3):
                    for j in range(-2,1):
                        square.append(self.puzzle[rowNum + i][colNum+j])

        elif rSq == 1:
            if cSq ==0:
                for i in range(-1,2):
                    for j in range(3):
                        square.append(self.puzzle[rowNum + i][colNum+j])
            elif cSq == 1:
                if cSq ==0:
                    for i in range(-1,2):
                        for j in range(-1,2):
                            square.append(self.puzzle[rowNum + i][colNum+j])
            elif cSq == 2:
                if cSq ==0:
                    for i in range(-1,2):
                        for j in range(-2,1):
                            square.append(self.puzzle[rowNum + i][colNum+j])
        elif rSq ==2:
            if cSq ==0:
                for i in range(-2,1):
                    for j in range(3):
                        square.append(self.puzzle[rowNum + i][colNum+j])
            elif cSq == 1:
                for i in range(-2,1):
                    for j in range(-1,2):
                        square.append(self.puzzle[rowNum + i][colNum+j])
            elif cSq == 2:
                for i in range(-2,1):
                    for j in range(-2,1):
                        square.append(self.puzzle[rowNum + i][colNum+j])


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

    def solvePuzzle(self,i,j):
        puz = self.puzzle

        if self.puzzleComplete():
            print "The puzzle is finished!"
            return True
        elif self.original[i][j] == 0:
            for k in range(puz[i][j],11):
                if k == 10:
                    ##print "Dead end at ", i,j
                    puz[i][j] = 0
                    self.texto[i][j].setText('')
                    return False
                elif self.checkPuzzle(k,i,j):
                    puz[i][j] = k
                    self.texto[i][j].setText(str(k))

                    if j != 8:
                        if self.solvePuzzle(i,j+1):
                            return True
                    else:
                        if self.solvePuzzle(i+1,0):
                            return True
        else:
            if j != 8:
                return self.solvePuzzle(i,j+1)
            else:
                return self.solvePuzzle(i+1,0)

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
    print x
    return x


print "Which difficulty should the solver demonstrate?"
# diff = 'Medium'
print "Please enter the name of the puzzle you wish to solve (type list to list puzzle names): "

while True:
    try:
        diff = raw_input()
        if diff != "list":
            puz = getPuzzle(diff)
            break
        else:
            print os.listdir("Puzzles"), "\n", "Please enter one of the above names"
    except IOError:
        print "That file does not exist. Please try again."


# if diff == "Impossible":
#     row1 = [8,0,0,0,0,0,0,0,0]
#     row2 = [0,0,3,6,0,0,0,0,0]
#     row3 = [0,7,0,0,9,0,2,0,0]
#     row4 = [0,5,0,0,0,7,0,0,0]
#     row5 = [0,0,0,0,4,5,7,0,0]
#     row6 = [0,0,0,1,0,0,0,3,0]
#     row7 = [0,0,1,0,0,0,0,6,8]
#     row8 = [0,0,8,5,0,0,0,1,0]
#     row9 = [0,9,0,0,0,0,4,0,0]

# elif diff == "Medium":
#     row1 = [5,0,0,0,9,0,0,0,0]
#     row2 = [0,2,9,0,0,0,7,0,0]
#     row3 = [8,7,0,2,5,0,0,0,0]
#     row4 = [1,6,0,0,0,0,0,0,0]
#     row5 = [0,4,5,6,2,9,8,3,0]
#     row6 = [0,0,0,0,0,0,0,6,2]
#     row7 = [0,0,0,0,7,5,0,9,4]
#     row8 = [0,0,3,0,0,0,2,7,0]
#     row9 = [0,0,0,0,4,0,0,0,6]


mySudoku = Sudoku(puz)
mySudoku.drawPuzzle()
print "\n"
mySudoku.solvePuzzle(0,0)
input()
mySudoku.win.close()