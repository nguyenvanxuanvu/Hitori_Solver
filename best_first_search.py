
# x: colored black
from asyncio import constants
from inspect import stack
from timeit import default_timer
import os
import psutil

f = open('testcase5x5.txt', 'r')
inputData = f.read().split('\n')

# get level
inputLevel = 0

# get problem
inputMatrix = []
# stack of the cells
stacks = []
for i in range(0, len(inputData)):
    temp = []
    temp = inputData[i].split(',')
    inputLevel = len(temp)
    inputRow = []
    
    for j in range(inputLevel):
        inputRow.append(temp[j])
    inputMatrix.append(inputRow)
    
########

class HitoriSolver:
    def __init__(self, _matrix: list, _level: int):
        self.beginMatrix = _matrix
        self.matrix = _matrix
        self.level = _level
        self.log = []
        self.latest = _matrix
        
    # print a matrix
    def printMatrix(self, matrix, step=-1):
        if step == 0:
            print('-----Initial-----')
        elif step == -1:
            if matrix:
                print('------Result-----')
            else:
                print('=====Can\'t Solve=====')
                return
        else:
            print('-----Step '+str(step)+'-----')
        for row in matrix:
            for ele in row:
                print(ele,end='  ')
            print()
    
    # print all status of matrix from start to finish
    def printLog(self):
        for i,v in enumerate(self.log[::-1]):
            self.printMatrix(v, i)
        self.printMatrix(self.matrix)

    # deep copy a matrix
    def copyMatrix(self, matrix):
        res = []
        for row in matrix:
            resRow = row.copy()
            res.append(resRow)
        return res

    # solve problem
    def solve(self):
        self.matrix = self.searchAndFill(self.matrix)

    # Best-first Search
    def searchAndFill(self, matrix, r=0, c=0, step=0):
        if matrix != self.latest:
            self.printMatrix(matrix, step)
            self.latest = matrix

        if r==self.level:
            self.log.append(matrix)
            return matrix

        # copy matrix for searching
        t_matrix = self.copyMatrix(matrix)
        
        # if a cell is not good for 'x' but it can be drawn 'x', push it to stack 
        # row index, column index and step
        if t_matrix[r][c] != 'x' and self.isNotGood(t_matrix,r,c) and self.inValid(t_matrix, r, c, t_matrix[r][c], True):
            stacks.append((r,c,step))
        
        # cell have not filled yet
        # try 'x' value

        if t_matrix[r][c] != 'x' and not self.isNotGood(t_matrix,r,c) and self.inValid(t_matrix, r, c, t_matrix[r][c], True):
            
            t_matrix[r][c] = 'x'
            
            res = self.searchAndFill(t_matrix, (r if c < self.level-1 else r+1), (c+1 if c < self.level-1 else 0), step+1)
            if res:
                self.log.append(matrix)
                return res
        
        # Keep the original value for cell
        if  self.inValid(t_matrix, r, c, self.beginMatrix[r][c], False):
            t_matrix[r][c] = self.beginMatrix[r][c]
            res = self.searchAndFill(t_matrix, (r if c < self.level-1 else r+1), (c+1 if c < self.level-1 else 0), step)
            if res:
                self.log.append(matrix)
                return res
            elif len(stacks)>0:
                temp = stacks.pop()
                newStep = step
                if self.inValid(t_matrix, r, c, t_matrix[r][c], True):
                    t_matrix[temp[0]][temp[1]]='x'
                else:
                    t_matrix[temp[0]][temp[1]]='x'
                    r = temp[0]
                    c = temp[1]
                    newStep = temp[2]
                    for i in range (inputLevel):
                        for j in range (inputLevel):
                            if (i > temp[0]):
                                t_matrix[i][j]=self.beginMatrix[i][j]
                            if i == temp[0] and j > temp[1]:
                                t_matrix[i][j] = self.beginMatrix[i][j]
                
                res = self.searchAndFill(t_matrix, (r if c < self.level-1 else r+1), (c+1 if c < self.level-1 else 0), newStep+1)
                if res:
                    self.log.append(matrix)
                    return res
    
        
        return None
    # Return mark of a cell 
    # The number of cell which have same value in same row or column with current cell
    def getMark(self, matrix, r, c):
        m = 0
        for i in range (inputLevel):
            if matrix[r][i] == matrix[r][c] and i != c:
                m = m + 1
            if matrix[i][c] == matrix[r][c] and i != r:
                m = m + 1
        return m
    # return true if current cell is not better than another cell (same column or same row))
    def isNotGood(self, matrix, r, c):
        listOfOp = []
        countBefore = 0
        for i in range (inputLevel):
            if i<r and matrix[i][c] == matrix[r][c]:
                countBefore = countBefore+1
            if i<c and matrix[r][i] == matrix[r][c]:
                countBefore = countBefore+1
        if countBefore > 0:
            return False
        countLast = 0
        for i in range (inputLevel):
            if i>r and matrix[i][c] == matrix[r][c]:
                countLast = countLast+1
            if i>c and matrix[r][i] == matrix[r][c]:
                countLast = countLast+1
        if countLast == 0:
            return False
        listOfOp = []
        for i in range (inputLevel):
            if c != i and matrix[r][c] == matrix[r][i]:
                listOfOp.append(self.getMark(matrix,r,i))
            if r != i and matrix[r][c] == matrix[i][c]:
                listOfOp.append(self.getMark(matrix,i,c))
        
        if len(listOfOp)==0 or self.getMark(matrix,r,c) < min(listOfOp):
            return True
        return False

    def inValid(self, matrix, r, c, op, type):
        # check if a cell have another cell with same value
        def checkRowColumn(lst: list):
            return True if lst.count(op) > 1 else False
        
        # check adjacent is x
        # False if exist
        # True if not exist
        def checkAdjacent():
            if (r>0 and r<self.level-1 and (matrix[r-1][c]=='x' or matrix[r+1][c]=='x')):
                return False
            elif (c>0 and c<self.level-1 and (matrix[r][c-1]=='x' or matrix[r][c+1]=='x')):
                return False
            elif (r==c==0 and (matrix[0][1]=='x' or matrix[1][0]=='x')):
                return False
            elif (r==c==self.level-1 and (matrix[r][c-1]=='x' or matrix[r-1][c]=='x')):
                return False
            elif (r==0 and c==self.level-1 and (matrix[r][c-1]=='x' or matrix[1][c]=='x')):
                return False
            elif (r==self.level-1 and c==0 and (matrix[r-1][c]=='x' or matrix[r][c+1]=='x')):
                return False
            elif (r==self.level-1 and c>0 and c<self.level-1 and (matrix[r-1][c]=='x')):
                return False
            elif (c==self.level-1 and r>0 and r<self.level-1 and (matrix[r][c-1]=='x')):
                return False
            elif (r==0 and c>0 and c<self.level-1 and (matrix[r+1][c]=='x')):
                return False
            elif (c==0 and r>0 and r<self.level-1 and (matrix[r][c+1]=='x')):
                return False
            
            return True

        def NonShape(i: int, j: int):
            
            temp = matrix
            temp[r][c] = 'x'
            if (i==j==0 and temp[0][1]=='x' and temp[1][0]=='x'):
                return True
            elif (i==0 and j==self.level-1 and temp[0][j-1]=='x' and temp[1][j]=='x'):
                return True
            elif (i==self.level-1 and j==0 and temp[i][1]=='x' and temp[i-1][0]=='x'):
                return True
            elif (i==j==self.level-1 and temp[i-1][j]=='x' and temp[i][j-1]=='x'):
                return True
            elif (j==self.level-1 and i>0 and i<self.level-1 and temp[i-1][j]=='x' and temp[i+1][j]=='x' and temp[i][j-1]=='x'):
                return True
            elif (i==self.level-1 and j>0 and j<self.level-1 and temp[i-1][j]=='x' and temp[i][j-1]=='x' and temp[i][j+1]=='x'):
                return True
            elif (i==0 and j>0 and j<self.level-1 and temp[i][j-1]=='x' and temp[i][j+1]=='x' and temp[i+1][j]=='x'):
                return True
            elif (j==0 and i>0 and i<self.level-1 and temp[i-1][j]=='x' and temp[i+1][j]=='x' and temp[i][j+1]=='x'):
                return True
            elif (i>0 and i<self.level-1 and j>0 and j<self.level-1 and temp[i-1][j]=='x' and temp[i+1][j]=='x' and temp[i][j+1]=='x'and temp[i][j-1]=='x'):
                return True
            
            return False
        # check if exist a cell is not connected in a single group by vertical or horizontal motion
        def checkNonShaded():
            for i in range(self.level):
                for j in range(self.level):
                    if(matrix[i][j] != 'x' and NonShape(i,j)):
                        return False
            
            
            return True
        
        if type==True:

            if ((checkRowColumn(matrix[r]) or checkRowColumn([matrix[i][c] for i in range(self.level)])) and checkAdjacent() and checkNonShaded()):
                return True
        if type == False:
            
            for i in range (c):
                if(matrix[r][i]==op):
                    return False
            for i in range (r):
                if(matrix[i][c]==op):
                    return False
            return True
def process_memory():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss

start = default_timer()
memBefore = process_memory()
solver = HitoriSolver(inputMatrix, inputLevel)

solver.solve()
memAfter = process_memory()
print('Usage Memory:', memAfter - memBefore, 'bytes')
stop = default_timer()
print('Time To Run: ', stop - start)
