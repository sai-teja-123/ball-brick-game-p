class BallBrick:

    def __init__(self, n):
        self.size = n
        self.gameMatrix = []
        self.createWallsAndGround()
        self.ballCount = 0
        self.ballPosition = [n - 1, n // 2]
        self.brickCount = 0
        self.extendedBaseOnRight = False
        self.pointToExtendOnRight = self.ballPosition[1] + 1
        self.pointToExtendOnLeft = self.ballPosition[1] - 1
    
    def createWallsAndGround(self):
        self.gameMatrix = [[' ' for j in range(self.size)] for i in range(self.size)]
        for row in range(self.size):
            self.gameMatrix[row][0] = 'W'
            self.gameMatrix[row][self.size - 1] = 'W'
        for col in range(self.size):
            self.gameMatrix[0][col] = 'W'
            if col > 0 and col < self.size - 1:
                self.gameMatrix[self.size - 1][col] = 'G'
        self.gameMatrix[self.size - 1][self.size // 2] = '_'
    
    def addBricks(self, row, col, type):
        self.gameMatrix[row][col] = type
        self.brickCount += 1
    
    def setballCount(self, count):
        self.ballCount = count
    
    def shootBall(self, direction):
        if direction == 'ST':
            self.travelStraight()
        elif direction == 'LD':
            self.travelLeftDiagonally()
        else:
            self.travelRightDiagonally()
    
    def isBrick(self, row, col):
        if self.gameMatrix[row][col] == 'B':
            self.powerBrickHit(row, col)
        elif self.gameMatrix[row][col] == 'DE':
            self.rowDestroyerBrickHit(row, col)
        elif self.gameMatrix[row][col] == 'DS':
            self.surroundingDestroyerBrickHit(row, col)
        else:
            self.numericBrickHit(row, col)
        self.ballPosition[1] = col
    
    def numericBrickHit(self, row, col):
        brickNum = int(self.gameMatrix[row][col])
        brickNum -= 1
        if brickNum == 0:
            self.gameMatrix[row][col] = ' '
            self.brickCount -= 1
        else:
            self.gameMatrix[row][col] = str(brickNum)
    
    def surroundingDestroyerBrickHit(self, row, col):
        mat = self.gameMatrix
        mat[row][col] = ' '
        self.brickCount -= 1
        for currCol in range(col - 1, col + 2):
            if mat[row - 1][currCol] != 'W' and mat[row - 1][currCol] != ' ':
                if mat[row - 1][currCol].isdigit():
                    mat[row - 1][currCol] = ' '
                    self.brickCount -= 1
                else:
                    self.isBrick(row - 1, currCol)
            if mat[row][currCol] != 'W' and mat[row][currCol] != ' ':
                if mat[row][currCol].isdigit():
                    mat[row][currCol] = ' '
                    self.brickCount -= 1
                else:
                    self.isBrick(row, currCol)
            if mat[row + 1][currCol] != 'W' and mat[row + 1][currCol] != ' ':
                if mat[row + 1][currCol].isdigit():
                    mat[row + 1][currCol] = ' '
                    self.brickCount -= 1
                else:
                    self.isBrick(row + 1, currCol)
    
    def rowDestroyerBrickHit(self, row, col):
        mat = self.gameMatrix
        mat[row][col] = ' '
        self.brickCount -= 1
        for currCol in range(1, self.size - 1):
            if mat[row][currCol] != ' ':
                if mat[row][currCol].isdigit():
                    mat[row][currCol] = ' '
                    self.brickCount -= 1
                else:
                    self.isBrick(row, currCol)
    
    def powerBrickHit(self, row, col):
        self.gameMatrix[row][col] = ' '
        self.brickCount -= 1
        if self.extendedBaseOnRight:
            if self.pointToExtendOnLeft > 0:
                self.gameMatrix[self.size - 1][self.pointToExtendOnLeft] = '_'
                self.pointToExtendOnLeft -= 1
                self.extendedBaseOnRight = False
        else:
            if self.pointToExtendOnRight < self.size - 1:
                self.gameMatrix[self.size - 1][self.pointToExtendOnRight] = '_'
                self.pointToExtendOnRight += 1
                self.extendedBaseOnRight = True
   
    def travelStraight(self):
        currCol = self.ballPosition[1]
        for row in range(self.size - 2, -1, -1):
            if self.gameMatrix[row][currCol] != ' ':
                if self.gameMatrix[row][currCol] != 'W':
                    self.isBrick(row, currCol)
                break
    
    def travelLeftDiagonally(self):
        currRow = self.ballPosition[0] - 1
        currCol = self.ballPosition[1] - 1
        mat = self.gameMatrix
        while currRow > -1 and currCol > -1:
            if mat[currRow][currCol] != ' ':
                if mat[currRow][currCol] == 'W':
                    self.travelRightHorizontally(currRow)
                else:
                    self.isBrick(currRow, currCol)
                break
            currRow -= 1
            currCol -= 1
    
    def travelRightDiagonally(self):
        currRow = self.ballPosition[0] - 1
        currCol = self.ballPosition[1] + 1
        mat = self.gameMatrix
        while currRow > -1 and currCol < self.size:
            if mat[currRow][currCol] != ' ':
                if mat[currRow][currCol] == 'W':
                    self.travelLeftHorizontally(currRow)
                else:
                    self.isBrick(currRow, currCol)
                break
            currRow -= 1
            currCol += 1
    
    def travelRightHorizontally(self, row):
        for col in range(1, self.size):
            if self.gameMatrix[row][col] != ' ':
                if self.gameMatrix[row][col] == 'W':
                    self.ballCount -= 1
                else:
                    self.isBrick(row, col)
                break
    
    def travelLeftHorizontally(self, row):
        for col in range(self.size - 2, -1, -1):
            if self.gameMatrix[row][col] != ' ':
                if self.gameMatrix[row][col] == 'W':
                    self.ballCount -= 1
                else:
                    self.isBrick(row, col)
                break
    
    def checkBallStatus(self):
        if self.ballPosition[1] != self.size // 2:
            if self.gameMatrix[self.size - 1][self.ballPosition[1]] != '_':
                self.ballCount -= 1
        self.ballPosition[1] = self.size // 2
    
    def displayGame(self):
        for row in range(self.size):
            for col in range(self.size):
                if row == self.ballPosition[0] and col == self.ballPosition[1]:
                    print('o', end = ' ')
                else:
                    print(self.gameMatrix[row][col], end = ' ')
            print('')
        self.checkBallStatus()
        if self.ballCount == 0 or self.brickCount == 0:
            if self.brickCount == 0:
                print('You win HURRAY..!!')
            else:
                print('You lose GAME OVER..!!')
            self.ballCount = 0
        else:
            print('Ball count is {}.'.format(self.ballCount))

def main():
    n = input('Enter size of the NxN matrix : ')
    while True:
        try:
            s = int(n)
            break
        except:
            n = input('Please enter an integer as the NxN matrix size : ')
            continue
    n = int(n)
    while n < 3:
        n = int(input('Please enter a valid NxN matrix size : '))
    game = BallBrick(n)
    print('')
    wishToConinue = 'y'
    while wishToConinue.lower() == 'y':
        row, col, brickType = list(input("Enter the brick's position and the brick type : ").split())
        while True:
            try:
                r = int(row)
                c = int(col)
                if (r > 0 and r < n - 1) and (c > 0 and c < n - 1):
                    if brickType in {'B', 'DS', 'DE'}:
                        break
                    else:
                        try:
                            b = int(brickType)
                            break
                        except:
                            row, col, brickType = list(input("Please enter the brick's position and a valid brick type : ").split())
                            continue
                else:
                    row, col, brickType = list(input("Please enter brick's position that is valid (within range) and the brick type : ").split())
                    continue
            except:
                row, col, brickType = list(input("Please enter brick's position that is valid (integer) and the brick type : ").split())
                continue
        row = int(row)
        col = int(col)
        game.addBricks(row, col, brickType)
        wishToConinue = input('Do you want to continue(Y or N)?')
    ballCount = 0
    currBallCount = input('Enter ball Count : ')
    while True:
        try:
            ball = int(currBallCount)
            break
        except:
            currBallCount = input('Please enter an integer for ball count : ')
            continue
    ballCount = int(currBallCount)
    game.setballCount(ballCount)
    game.displayGame()
    while game.ballCount > 0:
        direction = input('Enter the direction in which the ball need to traverse : ').upper()
        while direction not in {'ST', 'RD', 'LD'}:
            direction = input('Please enter a valid direction in which the ball need to traverse : ').upper()
        game.shootBall(direction)
        game.displayGame()
main()