#Sudoku solver, by Eugene Raether
import random, sys

#defines a sudoku state, used by the sudoku solver stack in order to back up to an earlier, stable state if no solution can be found
class PossibleMove:
    def __init__(self, sudoku, x, y, possibilities, movesApplied):
        self.sudoku = sudoku;
        self.x = x;
        self.y = y;
        self.possibilities = possibilities;
        self.movesApplied = movesApplied;
        
class Utils:
    @staticmethod
    def union(listA, listB):
        union = []
        for i in listA:
            if i in listB:
                union.append(i);
        return union;


class SudokuSolver:
    #Printing to the console in python, for whatever reason, is quite slow.  To counter act this, printing is optional for more performance-oriented applications
    def __init__(self, sudoku, printState=True):
        self.sudoku = sudoku;
        self.possibleMoves = []
        self.movesTaken = 0;
        self.printState = printState;

    def internalSolve(self):
        maxX = -1
        maxY = -1
        looping = True
        instability = False;
        while(looping):
            looping = False
            maxPossibilities = 10
            for i in range(0,9):
                for j in range(0,9):
                    if(instability):
                        looping = False;
                        break;
                
                    if self.sudoku.isValueKnown(i,j):
                        continue

                    numbers = self.sudoku.findPossibleValuesForPoint(i,j);
                    if(len(numbers) < maxPossibilities):
                        maxX = i
                        maxY = j
                        maxPossibilities = len(numbers)

                    #if there are no possible values for an empty slot, then there is no solution to the puzzle in its current state
                    if(len(numbers) == 0):
                        instability = True;
                    
                    #if there is only one value the cell can take, apply it immediately.  We won't have to restore to a previous state after this action
                    #because this is the only possible move for us to apply
                    if len(numbers) == 1:
                        self.applyMove(i,j,numbers[0], numbers);
                        looping = True

        if(self.sudoku.isSolved() == False):
            #if we're in an unsolvable state
            if instability:
                if self.printState:
                    print 'Unsolvable state detected';
                if len(self.possibleMoves) == 0:
                    print 'could not solve puzzle'
                    return;
            
                possibleMove = self.possibleMoves.pop();
                self.sudoku = possibleMove.sudoku;
                self.printMovesNotShown(possibleMove);
                if self.printState:
                    print "Popping stack, and re-guessing ("+str(possibleMove.x)+","+str(possibleMove.y)+") to be "+str(possibleMove.possibilities[-1])+", "+str(possibleMove.possibilities)+" available.";
                move = possibleMove.possibilities.pop();
                
                if(len(possibleMove.possibilities) != 0):
                    self.possibleMoves.append(PossibleMove(self.sudoku.duplicate(),possibleMove.x,possibleMove.y,possibleMove.possibilities, self.movesTaken));
                
                self.applyMove(possibleMove.x, possibleMove.y, move);

                #uncomment this line if you want to see the tries the game attempted
                #print self.sudoku;
                
                self.internalSolve()
            #select an available choice randomly and try to solve the resulting sudoku, storing the current valid state in case the choice leads to
            #an unsolvable puzzle
            else:
                moves = self.sudoku.findPossibleValuesForPoint(maxX, maxY);
                moveID = int(random.random()*len(moves));
                if(len(self.possibleMoves) != 0):
                    self.printMovesNotShown(self.possibleMoves[-1]);
                if self.printState:
                    print "Guessing ("+str(maxX)+","+str(maxY)+") to be "+str(moves[moveID])+", "+str(moves)+" available.";
                val = moves.pop(moveID);
                self.possibleMoves.append(PossibleMove(self.sudoku.duplicate(),maxX,maxY,moves, self.movesTaken+1));
                self.applyMove(maxX, maxY, val);
                self.internalSolve()
            
        else:
            print "Sudoku successfully solved!";
            print "Moves taken: "+str(self.movesTaken);
    def printMovesNotShown(self, possibleMove):
        return 
        diff = self.movesTaken-possibleMove.movesApplied;
        out = "["+str(diff)+" since push, "+str(self.movesTaken)+" total]"
        if(diff != 0):
            print out;
        
    def applyMove(self, x, y, value, possibleMoves=None):
        disp = "";
        if possibleMoves != None:
            if len(possibleMoves) == 1:
                disp = "Applying only possible move: ";
            else:
                disp = "Out of "+str(possibleMoves)+" ";
                disp += 'Setting ('+str(x)+","+str(y)+') to '+str(value);
                print disp;
        self.sudoku.setValue(x, y, value);
        self.movesTaken+=1;
        
    def solve(self):
        self.reset();
        self.internalSolve();
        
    def reset(self):
        self.possibleMoves = [];
        self.movesTaken = 0;

    def getSudoku(self):
        return self.sudoku;
      
    
class Sudoku:
    #column / row structure
    def __init__(self, rawSudokuData):
        self.sudoku = rawSudokuData

    def duplicate(self):
        dup = []
        for i in range(0,9):
            line = []
            for j in range(0, 9):
                line.append(self.sudoku[i][j])
            dup.append(line);
        return Sudoku(dup);
    
    def isSolved(self):
        for i in range(0,9):
            for j in range(0, 9):
                if self.isValueKnown(i,j) == False:
                    return False;

        return True;
    
    def findMissingValuesInRow(self, row):
        numbers = range(1,10);
        for i in range(0,9):
            if(self.sudoku[row][i] in numbers):
                numbers.remove(self.sudoku[row][i]);
        return numbers;
    
    def findMissingValuesInColumn(self, col):
        numbers = range(1,10)
        for i in range(0,9):
            if(self.sudoku[i][col] in numbers):
                numbers.remove(self.sudoku[i][col]);
        return numbers;
    
    def findMissingValuesInQuadrant(self, quadrant):
        quadX = int(quadrant/3)*3
        quadY = int(quadrant%3)*3
        numbers = range(1,10)
        for x in range(quadX,quadX+3):
            for y in range(quadY,quadY+3):
                if(self.sudoku[x][y] in numbers):
                    numbers.remove(self.sudoku[x][y]);

        return numbers;
    def calculateQuadrantForPoint(self, x,y):
        quadX = int(x/3)*3
        quadY = int((y/3)%3)
        return quadX+quadY;

    
    def findPossibleValuesForPoint(self, x, y):
        col = self.findMissingValuesInColumn(y)
        row = self.findMissingValuesInRow(x)
        quad = self.findMissingValuesInQuadrant(self.calculateQuadrantForPoint(x,y))
        return Utils.union(Utils.union(col, row),quad);
    
    def isValueKnown(self, x, y):
        return self.sudoku[x][y] != 0;

    def setValue(self, x, y, value):
        self.sudoku[x][y] = value;
        
    def __str__(self):
        res = "";
        for i in range(len(self.sudoku)):
            for j in range(len(self.sudoku[i])):
                if self.sudoku[i][j] != 0:
                    res += str(self.sudoku[i][j]);
                else:
                    res += '-';
            if i != len(self.sudoku)-1:
                res += '\n';
        return res;

#Solves a given sudoku
#Given the way it solves these problems, it is possible to also generate sudokus by giving a 9x9 file full of 0s (puzzle4.txt).  This forces the sudoku solver to randomly
#pick values for every single element, thus generating a unique puzzle.  To keep track, you can seed the random class to keep track of unique generations.
def main():
    #random.seed(1);
    sys.setrecursionlimit(5000)
    fileName = None;
    if len(sys.argv) != 2:
        print 'Usage: runner.py name_of_puzzle.txt';
        fileName = "puzzle4.txt";
        print 'Using default puzzle: '+fileName+'\n';
    else:
        fileName = sys.argv[1];
        
    print "Loaded Sudoku: "+fileName;
    sudoku = Sudoku(loadSudoku(fileName));
    print(sudoku)
    print 'Solving Sudoku:'

    printStackTrace = False;
    
    sudokuSolver = SudokuSolver(sudoku,printStackTrace);
    sudokuSolver.solve()
    print sudokuSolver.getSudoku()


#Sample sudoku file contents
# 027000500
# 600000903
# 900050020
# 005040070
# 000706000
# 070010800
# 010090004
# 304000001
# 002000790

#reads in a file with the above structure and creates a 2d-int array based on it for use in initializing a Sudoku object  
def loadSudoku(fileName):
    f = open(fileName, 'r')
    sudoku = []
    reading = True;
    
    while(reading):
        line = f.readline().strip();
        if line=="":
            reading = False;
            break;
        if line.startswith("#"):
            print line;
            continue;
        sudokuLine = [];
        for c in line:
            if(c.isdigit()):
                sudokuLine.append(int(c));
        sudoku.append(sudokuLine);
    return sudoku
    
if __name__ == "__main__":
    main()
