
from cmu_graphics import *
# x y pos class
class xy:
    def __init__(self, x, y):
        self.x = x
        self.y = y

#CMU handler class
class cmu:
    def __init__(self):
        self.canvas = xy(400, 400)

cmu = cmu()
app.stepsPerSecond = 100

class keybind_class:
    def __init__(self):
        self.settingKeybinds = None
        self.step = "space"
        self.playPause = "p"
    def rebind_key(self, key):
        self.settingKeybinds = key
keybinds = keybind_class()

def onKeyPress(key):
    if key == keybinds.step:
        game.step()
    if key == keybinds.playPause:
        game.tick = not game.tick

#general game class
class game:
    
    def __init__(self, tileSize, alive, reproduce, border=False, borderSize=1):
        game.tick = False
        self.alive = alive
        self.reproduce = reproduce
        self.tileSize = tileSize
        self.group = Group()
        self.makeBoard(self.tileSize)
        self.setBorder(border, borderSize)

    
    def bulk(self, func):
        for x in range(len(self.board)):
            for y in range(len(self.board[x])):
                func(x, y)
    
    def IcreateTile(self, x, y):
        self.board[x][y] = tile(xy(x, y), self.tileSize)
    
    def Iborder(self, x, y):
        self.board[x][y].rec.borderWidth = self.borderSize
        self.board[x][y].rec.border = ("grey" if self.border else None)
    
    def makeBoard(self, tileSize):
        self.board = makeList(int(cmu.canvas.x/tileSize.x), int(cmu.canvas.y/tileSize.y))
        self.bulk(self.IcreateTile)
        self.bulk(self.makeGroup)
    
    def makeGroup(self, x, y):
        self.group.add(self.board[x][y].rec)
    
    def Icalc(self, x, y):
        self.board[x][y].calcNextState()
    
    def Istep(self, x, y):
        self.board[x][y].step()
    
    def step(self):
        self.bulk(self.Icalc)
        self.bulk(self.Istep)
    
    def setBorder(self, state, size):
        self.border = state
        self.borderSize = size
        self.bulk(self.Iborder)

#tile class
class tile:
    def __init__(self, pos, shape, state=False, border=False):
        self.pos = pos
        self.rec = Rect(self.pos.x * shape.x, self.pos.y * shape.y, shape.x, shape.y, fill=("black" if not state else "white"), border=("grey" if border else None))
        self.nextState = "black"
    
    def setState(self, state):
        self.rec.fill = "black" if not state else "white"
    
    def calcNextState(self):
        alive = 0
        dead = 0
        for x in range(self.pos.x -1, self.pos.x + 2):
            for y in range(self.pos.y - 1, self.pos.y + 2):
                if not (x == self.pos.x and y == self.pos.y):
                    try:
                        assert game.board[x][y].rec.fill == "black" or game.board[x][y].rec.fill == "white"
                        if game.board[x][y].rec.fill == "black":
                            dead += 1
                        elif game.board[x][y].rec.fill == "white":
                            alive += 1
                        else:
                            print("ERROR, color exception not caught")
                    except:
                        dead += 1
        if alive in game.alive:
            if self.rec.fill == "black" and alive in game.reproduce:
                self.nextState = "white"
            else:
                self.nextState = self.rec.fill
        else:
            self.nextState = "black"
    
    def step(self):
        self.rec.fill = self.nextState
        

#tick handler
def onStep():
    if game.tick:
        game.step()


#click handler
startState = -1

def onMouseDrag(x, y):
    global startState
    if startState == -1:
        print(game.group.hitTest(x, y))
        startState = ("white" if game.group.hitTest(x, y).fill == "black" else "black")
    if startState == 1:
        print(game.group.hitTest(x, y))
        startState = game.group.hitTest(x, y).fill
    game.group.hitTest(x, y).fill = startState

def onMousePress(x, y):
    global startState
    startState = 1
    game.group.hitTest(x, y).fill = ("white" if game.group.hitTest(x, y).fill == "black" else "black")

def onMouseRelease(x, y):
    global startState
    startState = -1 
    


game = game(xy(20, 20), [2, 3], [3], border=True, borderSize = 0.6)











