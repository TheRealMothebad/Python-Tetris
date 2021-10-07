from cmu_graphics import *

class xy:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class game:
    def __init__(self, boardX, boardY):
        self.gravity = 10
        self.boardSize = xy(boardX, boardY)
    
    def makeBoard(self):
        self.board = board(self.boardSize.x, self.boardSize.y)

class tile:
    def __init__(self, pos, borderWidth=1, borderColor="none"):
        self.x = pos.x
        self.y = pos.y
        self.rec = Rect(canvas.x/(game.boardSize.x*2/10)+self.x*tileSize, self.y*tileSize, tileSize, tileSize, borderWidth=borderWidth)

class board:
    def __init__(self, rows, cols):
        self.matrix = makeList(rows, cols + 4)
        for x in range(len(self.matrix)):
            for y in range(len(self.matrix)):
                self.matrix[x][y] = tile()



canvas = xy(400, 400)