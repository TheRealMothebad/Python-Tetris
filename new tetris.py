from cmu_graphics import *
##CLASSES:
# -- Structure Classes --
#CMU class to handle all of the jank ;)
class cmu:
    canvas = xy(400, 400)
    def __init__(self):
        pass

    #setter functions
    def tickspeed(self, speed):
        app.stepsPerSecond = speed
    
    #getter functions
    def tickspeed(self):
        return app.stepsPerSecond
    
    #mutator functions
    
#xy class - positional implementation of a tuple
class xy:
    def __init__(self, x, y):
        self.x = x
        self.y = y

#-- Game Mechanics Classes --
#game class - controls general game functions
class game:
    def __init__(self, boardX, boardY):
        self.gravity = 10
        #adds 4 for spawning space above board
        self.boardSize = xy(boardX, boardY)
        self.tileSize = cmu.canvas.x/game.boardSize.x
    
    def makeBoard(self):
        self.board = board(self.boardSize.x, self.boardSize.y, False)

#board class - defines board instance
class board:
    def __init__(self, rows, cols, visible):
        self.matrix = makeList(rows, cols + 4)
        for x in range(len(self.matrix)):
            for y in range(len(self.matrix)):
                self.matrix[x][y] = tile(xy(x, y), visible=visible)

#tile class - defines tile instance
class tile:
    def __init__(self, pos, borderWidth=1, borderColor="none", visible=True):
        self.x = pos.x
        self.y = pos.y
        #x-pos, y-pos, width, height, boarder
        self.rec = Rect(cmu.canvas.x/(game.boardSize.x*2/10)+self.x*game.tileSize, self.y*game.tileSize, game.tileSize, game.tileSize, borderWidth=borderWidth)

class tetromino():
    def __init__(self):
        pass