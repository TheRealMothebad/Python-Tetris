from cmu_graphics import *
#-- INITIALIZE VARIABLES --
#pos class needs to go here cuz it is used very soon
class posXY:
    def __init__(self, x, y):
        self.x = x
        self.y = y
#board dimensions
canvas = posXY(400, 400)
boardRow = 20
boardCol = 10
tileSize = canvas.x/boardRow
boardMatrix = makeList(boardCol, boardRow)
#make grid lines by drawing them manually

#key handler vars
keysPressed = []
keyLabel = Label('', 200, 200, size = 50)
buttons = []

#tickspeed
app.stepsPerSecond = 20
gravityStrength = 10
gravityTimer = 0

#misc vars
active = None
pieces = ["I", "J", "L", "O", "S", "T", "Z"]
gameStopped = True

#-- DEBUGGING PRINT STATEMENT FUNCTION --
#yall's IDE is laggy when printing so I need to be selective about when I print, hence this class.
class p():
    def __init__(self, sepString=" ", label=False):
        self.groups = {}
        self.sepString = sepString
        self.label = label
    
    def check_group(self, group):
        if not group in self.groups:
            self.groups[group] = True
    
    def s(self, group, *values):
        self.check_group(group)
        if self.groups[group]:
            output = ""
            for i in values:
                output += str(i)
                output += str(self.sepString)
            print((("[" + group + "] ") if self.label else "") + output[0:len(output)-len(self.sepString)])
    
    def enable(self, *group):
        for i in group:
            self.check_group(i)
            self.groups[i] = True
    
    def disable(self, *group):
        if len(group) == 0:
            print(type(self.groups.keys()))
            for i in self.groups.keys():
                self.groups[i] = False
        else:
            for i in group:
                self.check_group(i)
                self.groups[i] = False

p = p(label=True)
#p.disable()
p.disable("inherit", "render", "place", "collision")

#-- KEYBINDS CLASS --
class keybind_class:
    def __init__(self):
        self.settingKeybinds = None
        self.moveL = "left"
        self.moveR = "right"
        self.dropSoft = "down"
        self.dropHard = "up"
        self.spinL = "z"
        self.spinR = "x"
        self.hold = "space"
        #self.spin180 = "c" kinda stupid, might not incude
    
    def rebind_key(key):
        self.settingKeybinds = key
        
        
        
keybinds = keybind_class()

#-- BUTTON CLASS --
class button():
    def __init__(self, text, center, width, height, onPress, color="lightGray", textSize=12, textColor="Black", border="gray"):
        global buttons
        buttons.append(self)
        self.rect = Rect(center.x-(width/2), center.y-(height/2), width, height, fill=color, border=border)
        self.label = Label(text, center.x, center.y, size=textSize, fill=textColor)
        self.onPress = onPress
        
    def pressed(self):
        self.onPress()
    
    def show(self):
        self.rect.visible = True
        self.label.visible = True
    
    def hide(self):
        self.rect.visible = False
        self.label.visible = False
    
    @staticmethod
    def all_show():
        global buttons
        for i in buttons:
            i.show()
    
    @staticmethod
    def all_hide():
        global buttons
        for i in buttons:
            i.hide()

#-- TILE CLASS --
class tile:
    #instance variables are declared in constructor
    def __init__(self, pos, borderWidth=1, borderColor="none", side=False):
        self.x = pos.x
        self.y = pos.y
        if side:
            self.recShape = Rect(canvas.x/(boardRow*2/10)+self.x*tileSize, self.y*tileSize, tileSize, tileSize, borderWidth=borderWidth)
        else:
            self.recShape = Rect(canvas.x/(boardRow*2/10)+self.x*tileSize, self.y*tileSize, tileSize, tileSize, borderWidth=borderWidth)
        self.active = False
    
    def inherit(self, prevTile, wipe):
        p.s("inherit", self.x , ",", self.y, "is inheriting", prevTile.x, ",", prevTile.y)
        self.render(prevTile.get_color())
        self.active = prevTile.active

        if wipe:
            p.s("inherit", prevTile.x, ",", prevTile.y, "wiped")
            prevTile.wipe()
    
    def wipe(self):
        self.recShape.fill = "black"
        self.active = False
        p.s("inherit", self.recShape.fill)
    
    def render(self, color):
            self.recShape.fill = color
        
    def get_color(self):
        return self.recShape.fill
    
    def check_collision(self, dir):
        x = self.x+dir.x
        y = self.y+dir.y
        #check if it's within x bounds (turn off for fun)
        if self.x+dir.x <= boardCol - 1 and self.x+dir.x >= 0:
            #check if it's within y bounds
            if self.y+dir.y <= boardRow - 1:
                if boardMatrix[int(x)][int(y)].get_color() == "black" or boardMatrix[int(x)][int(y)].active == True:
                    return "clear"
                else:
                    return "block"
            else:
                return "floor"
        else:
            return "wall"
        p.s("error", "ERROR: check_collision edge case")
        return -1

#-- TETRIOMINOS --
class tetromino:
    
    def __init__(self):
        self.origin = posXY(5, 2)
        self.rot = 1
        self.shape = []
        self.color = "white"
    
    def rotate(self, direction):
        normalizedDir = self.rot + direction
        if normalizedDir > 4:
            normalizedDir -= 4
        elif normalizedDir < 1:
            normalizedDir += 4
        else:
            normalizedDir = self.rot + direction
        collision = self.check_dir_col(normalizedDir)
        if "block" in collision or "floor" in collision or "wall" in collision or "Out of Bounds" in collision:
            self.kick()
        else:
            for i in self.get_shape():
                boardMatrix[int(i.x)][int(i.y)].wipe()
            self.rot = normalizedDir
        self.shape_render()
    
    def move(self, dir):
        collision = self.check_shape_col(dir)
        if ("block" in collision and dir.y == 1) or ("floor" in collision):
            self.place()
        elif "block" in collision or "wall" in collision:
            pass
        elif "clear" in collision:
            self.shift_origin(dir.x, dir.y)
            self.shape_inherit(posXY(dir.x, dir.y), True)
            self.shape_render()
        else:
            p.s("error", "ERROR: bad collision")

    def shift_origin(self, x, y):
        self.origin.x += x
        self.origin.y += y
        p.s("shift", "origin shifted to: (", self.origin.x, ",", self.origin.y, ")")
    
    def get_shape(self):
        if self.rot == 1:
            self.shape = [posXY(self.origin.x-1.5, self.origin.y-1), posXY(self.origin.x-0.5, self.origin.y-1), posXY(self.origin.x+0.5, self.origin.y-1), posXY(self.origin.x+1.5, self.origin.y-1)]
        elif self.rot == 2:
            self.shape = [posXY(self.origin.x, self.origin.y-2), posXY(self.origin.x, self.origin.y-1), posXY(self.origin.x, self.origin.y), posXY(self.origin.x, self.origin.y+1)]
        elif  self.rot == 3:
            self.shape = [posXY(self.origin.x-1.5, self.origin.y), posXY(self.origin.x-0.5, self.origin.y), posXY(self.origin.x+0.5, self.origin.y), posXY(self.origin.x+1.5, self.origin.y)]
        elif self.rot == 4:
            self.shape = [posXY(self.origin.x, self.origin.y-2), posXY(self.origin.x, self.origin.y-1), posXY(self.origin.x, self.origin.y+1), posXY(self.origin.x, self.origin.y+2)]
        return self.shape

    def shape_render(self):
        p.s("render", "in render function for: ")
        for i in self.get_shape():
            p.s("render", i.x, ":", i.y)
            boardMatrix[int(i.x)][int(i.y)].render(self.color)
            boardMatrix[int(i.x)][int(i.y)].active = True

    def shape_inherit(self, dir, wipe):
        for i in self.get_shape():
            boardMatrix[int(i.x)][int(i.y)].inherit(boardMatrix[int(i.x-dir.x)][int(i.y-dir.y)], wipe)

    def drop(self):
        while not (("block" in self.check_shape_col(posXY(0, 1))) or ("floor" in self.check_shape_col(posXY(0, 1)))):
            self.move(posXY(0, 1))
        self.move(posXY(0, 1))
                    
    def check_shape_col(self, dir):
        result = []
        for i in self.get_shape():
            #print("x: " + str(i.x) + " y: " + str(i.y))
            if i.x < 0 or i.x >= len(boardMatrix) or i.y < 0 or i.y >= len(boardMatrix[0]):
                result.append("Out of Bounds")
            else:
                result.append(boardMatrix[int(i.x)][int(i.y)].check_collision(dir))
        p.s("collision", result)
        return result
    
    def check_dir_col(self, rot):
        default = self.rot
        self.rot = rot
        collision = self.check_shape_col(posXY(0, 0))
        self.rot = default
        return collision
    
    def kick(self):
        pass
        
    def place(self):
        for i in self.get_shape():
            boardMatrix[int(i.x)][int(i.y)].active = False
            p.s("place", i.x, ",", i.y, "is", boardMatrix[int(i.x)][int(i.y)].active)
        next_piece()
        
class I(tetromino):
    def __init__(self):
        super().__init__()
        self.origin = posXY(5, 1)
        self.color = "cyan"
    
    def get_shape(self):
        if self.rot == 1:
            self.shape = [posXY(self.origin.x-1.5, self.origin.y-1), posXY(self.origin.x-0.5, self.origin.y-1), posXY(self.origin.x+0.5, self.origin.y-1), posXY(self.origin.x+1.5, self.origin.y-1)]
        elif self.rot == 2:
            self.shape = [posXY(self.origin.x, self.origin.y-2), posXY(self.origin.x, self.origin.y-1), posXY(self.origin.x, self.origin.y), posXY(self.origin.x, self.origin.y+1)]
        elif  self.rot == 3:
            self.shape = [posXY(self.origin.x-1.5, self.origin.y), posXY(self.origin.x-0.5, self.origin.y), posXY(self.origin.x+0.5, self.origin.y), posXY(self.origin.x+1.5, self.origin.y)]
        elif self.rot == 4:
            self.shape = [posXY(self.origin.x-1, self.origin.y-2), posXY(self.origin.x-1, self.origin.y-1), posXY(self.origin.x-1, self.origin.y), posXY(self.origin.x-1, self.origin.y+1)]
        return self.shape

class J(tetromino):
    def __init__(self):
        super().__init__()
        self.origin = posXY(4.5, 2)
        self.color = "blue"
    
    def get_shape(self):
        if self.rot == 1:
            self.shape = [posXY(self.origin.x-1.5, self.origin.y-1.5), posXY(self.origin.x-1.5, self.origin.y-0.5), posXY(self.origin.x-0.5, self.origin.y-0.5), posXY(self.origin.x+0.5, self.origin.y-0.5)]
        elif self.rot == 2:
            self.shape = [posXY(self.origin.x-0.5, self.origin.y-1.5), posXY(self.origin.x+0.5, self.origin.y-1.5), posXY(self.origin.x-0.5, self.origin.y-0.5), posXY(self.origin.x-0.5, self.origin.y+0.5)]
        elif  self.rot == 3:
            self.shape = [posXY(self.origin.x-1.5, self.origin.y-0.5), posXY(self.origin.x-0.5, self.origin.y-0.5), posXY(self.origin.x+0.5, self.origin.y-0.5), posXY(self.origin.x+0.5, self.origin.y+0.5)]
        elif self.rot == 4:
            self.shape = [posXY(self.origin.x-0.5, self.origin.y-1.5), posXY(self.origin.x-0.5, self.origin.y-0.5), posXY(self.origin.x-1.5, self.origin.y+0.5), posXY(self.origin.x-0.5, self.origin.y+0.5)]
        return self.shape
        
class L(tetromino):
    def __init__(self):
        super().__init__()
        self.origin = posXY(4.5, 2)
        self.color = "orange"
    
    def get_shape(self):
        if self.rot == 1:
            self.shape = [posXY(self.origin.x+0.5, self.origin.y-1.5), posXY(self.origin.x-1.5, self.origin.y-0.5), posXY(self.origin.x-0.5, self.origin.y-0.5), posXY(self.origin.x+0.5, self.origin.y-0.5)]
        elif self.rot == 2:
            self.shape = [posXY(self.origin.x-0.5, self.origin.y-1.5), posXY(self.origin.x-0.5, self.origin.y-0.5), posXY(self.origin.x-0.5, self.origin.y+0.5), posXY(self.origin.x+0.5, self.origin.y+0.5)]
        elif  self.rot == 3:
            self.shape = [posXY(self.origin.x-1.5, self.origin.y-0.5), posXY(self.origin.x-0.5, self.origin.y-0.5), posXY(self.origin.x+0.5, self.origin.y-0.5), posXY(self.origin.x-1.5, self.origin.y+0.5)]
        elif self.rot == 4:
            self.shape = [posXY(self.origin.x-1.5, self.origin.y-1.5), posXY(self.origin.x-0.5, self.origin.y-1.5), posXY(self.origin.x-0.5, self.origin.y-0.5), posXY(self.origin.x-0.5, self.origin.y+0.5)]
        return self.shape
        
class O(tetromino):
    def __init__(self):
        super().__init__()
        self.origin = posXY(5, 1)
        self.color = "yellow"
    
    def get_shape(self):
        if self.rot == 1:
            return [posXY(self.origin.x-1, self.origin.y-1), posXY(self.origin.x, self.origin.y-1), posXY(self.origin.x-1, self.origin.y), posXY(self.origin.x, self.origin.y)]
    
    def rotate(self, direction):
        pass

class S(tetromino):
    def __init__(self):
        super().__init__()
        self.origin = posXY(4.5, 2)
        self.color = "limegreen"
    
    def get_shape(self):
        if self.rot == 1:            
            self.shape = [posXY(self.origin.x-0.5, self.origin.y-1.5), posXY(self.origin.x+0.5, self.origin.y-1.5), posXY(self.origin.x-1.5, self.origin.y-0.5), posXY(self.origin.x-0.5, self.origin.y-0.5)]
        elif self.rot == 2:
            self.shape = [posXY(self.origin.x-0.5, self.origin.y-1.5), posXY(self.origin.x-0.5, self.origin.y-0.5), posXY(self.origin.x+0.5, self.origin.y-0.5), posXY(self.origin.x+0.5, self.origin.y+0.5)]
        elif  self.rot == 3:
            self.shape = [posXY(self.origin.x-0.5, self.origin.y-0.5), posXY(self.origin.x+0.5, self.origin.y-0.5), posXY(self.origin.x-1.5, self.origin.y+0.5), posXY(self.origin.x-0.5, self.origin.y+0.5)]
        elif self.rot == 4:
            self.shape = [posXY(self.origin.x-1.5, self.origin.y-1.5), posXY(self.origin.x-1.5, self.origin.y-0.5), posXY(self.origin.x-0.5, self.origin.y-0.5), posXY(self.origin.x-0.5, self.origin.y+0.5)]
        return self.shape

class T(tetromino):
    def __init__(self):
        super().__init__()
        self.origin = posXY(4.5, 2)
        self.color = "magenta"
    
    def get_shape(self):
        if self.rot == 1:            
            self.shape = [posXY(self.origin.x-0.5, self.origin.y-1.5), posXY(self.origin.x-1.5, self.origin.y-0.5), posXY(self.origin.x-0.5, self.origin.y-0.5), posXY(self.origin.x+0.5, self.origin.y-0.5)]
        elif self.rot == 2:
            self.shape = [posXY(self.origin.x-0.5, self.origin.y-1.5), posXY(self.origin.x-0.5, self.origin.y-0.5), posXY(self.origin.x+0.5, self.origin.y-0.5), posXY(self.origin.x-0.5, self.origin.y+0.5)]
        elif  self.rot == 3:
            self.shape = [posXY(self.origin.x-1.5, self.origin.y-0.5), posXY(self.origin.x-0.5, self.origin.y-0.5), posXY(self.origin.x+0.5, self.origin.y-0.5), posXY(self.origin.x-0.5, self.origin.y+0.5)]
        elif self.rot == 4:
            self.shape = [posXY(self.origin.x-0.5, self.origin.y-1.5), posXY(self.origin.x-1.5, self.origin.y-0.5), posXY(self.origin.x-0.5, self.origin.y-0.5), posXY(self.origin.x-0.5, self.origin.y+0.5)]
        return self.shape

class Z(tetromino):
    def __init__(self):
        super().__init__()
        self.origin = posXY(4.5, 2)
        self.color = "red"
    
    def get_shape(self):
        if self.rot == 1:            
            self.shape = [posXY(self.origin.x-1.5, self.origin.y-1.5), posXY(self.origin.x-0.5, self.origin.y-1.5), posXY(self.origin.x-0.5, self.origin.y-0.5), posXY(self.origin.x+0.5, self.origin.y-0.5)]
        elif self.rot == 2:
            self.shape = [posXY(self.origin.x+0.5, self.origin.y-1.5), posXY(self.origin.x-0.5, self.origin.y-0.5), posXY(self.origin.x+0.5, self.origin.y-0.5), posXY(self.origin.x-0.5, self.origin.y+0.5)]
        elif  self.rot == 3:
            self.shape = [posXY(self.origin.x-1.5, self.origin.y-0.5), posXY(self.origin.x-0.5, self.origin.y-0.5), posXY(self.origin.x-0.5, self.origin.y+0.5), posXY(self.origin.x+0.5, self.origin.y+0.5)]
        elif self.rot == 4:
            self.shape = [posXY(self.origin.x-0.5, self.origin.y-1.5), posXY(self.origin.x-1.5, self.origin.y-0.5), posXY(self.origin.x-0.5, self.origin.y-0.5), posXY(self.origin.x-1.5, self.origin.y+0.5)]
        return self.shape

class nextBoard:
    def __init__():
        self.x = 4
        self.y = 16
        self.board = makeList(self.x, self.y)
        for x in self.board:
            for y in self.board[0]:
                self.board[x][y] = tile(posXY(x, y))
    
    def update():
        pass
        

#-- KEY HANDLER --
def onKeyPress(key):
    if keybinds.settingKeybinds != None:
        keybinds.rebind_key(key)
    elif gameStopped:
        pass
    elif key == keybinds.moveL:
        active.move(posXY(-1, 0))
        
    elif key == keybinds.moveR:
        active.move(posXY(1, 0))
        
    elif key == keybinds.dropSoft:
        active.move(posXY(0, 1))
    
    elif key == keybinds.spinL:
        active.rotate(-1)
        
    elif key == keybinds.spinR:
        active.rotate(1)
        
    elif key == keybinds.dropHard:
        active.drop()
    
    elif key == keybinds.hold:
        hold()
    
    #elif key == keybinds.
    
    elif key == "b":
        bulk_debug_render()
    else:
        print(key + " is not bound to anything")

def onMousePress(mouseX, mouseY):
    if gameStopped:
        down = posXY(mouseX, mouseY)
        for i in buttons:
            if i.rect.hits(down.x, down.y):
                i.pressed()

#deprecated way to handle keys
'''
#I know that there is already an inbuilt way to do this, but this is the easiest way I could think of to convert from async data to sync for the onStep function
def onKeyPress(key):
    if not key in keysPressed:
        keysPressed.append(key)

def onKeyRelease(key):
    if key in keysPressed:
        keysPressed.pop(keysPressed.index(key))


def handle_keys():
    if keybinds.moveL in keysPressed:
        moveL()
    if keybinds.moveR in keysPressed:
'''

#-- GAME FUNCTIONS --
def check_lose():
    for x in range(3, 7):
        if boardMatrix[x][0].get_color() != "black" or boardMatrix[x][1].get_color() != "black":
            print("u lose" + str(x))
            return True

def u_lose():
    global gameStopped
    gameStopped = True

queue = []

def hold():
    pass

def next_piece():
    global active
    if check_lose():
        u_lose()
        
    else:
        p.s("piece", "new piece")
        while len(queue) < 6:
            new = pieces[randrange(len(pieces))]
            queue.append(new)
        next = queue[0]
        queue.pop(0)
        if next == "I":
            active = I()
        elif next == "J":
            active = J()
        elif next == "L":
            active = L()
        elif next == "S":
            active = S()
        elif next == "O":
            active = O()
        elif next == "T":
            active = T()
        elif next == "Z":
            active = Z()
        else:
            p.s("error", "ERROR: tetromino \"" + next + "\" is not defined")
        p.s("piece", "New", next, "piece is spawning")
        active.shape_render()
        check_clear()
    
def gravity():
    global active
    global gravityTimer
    if gravityStrength == 0:
        return
    if gravityTimer >= app.stepsPerSecond - gravityStrength:
        gravityTimer = 1
        active.move(posXY(0, 1))
    else:
        gravityTimer += 1

def check_clear():
    for y in range(len(boardMatrix[0])):
        full = True
        for x in range(len(boardMatrix)):
            if boardMatrix[x][y].get_color() == "black":
                full = False
        if full:
            clear_line(y)

def clear_line(line):
    print("clearing line " + str(line))
    
    for y in range(line, 1, -1):
        p.s("line", y, "is inheriting line", y-1)
        for x in range(len(boardMatrix)):
            if not boardMatrix[x][y-1].active:
                boardMatrix[x][y].inherit(boardMatrix[x][y-1], False)
            else:
                boardMatrix[x][y].wipe()
    '''
    for y in range(line, 1, -1):
        for x in range(len(boardMatrix)):
            if not boardMatrix[x][y-1].active:
                boardMatrix[x][y].inherit(boardMatrix[x][y-1], False)
            else:
                boardMatrix[x][y].wipe()
    '''
        
def shader():
    for x in range(len(boardMatrix)):
        for y in range(len(boardMatrix[x])):
            if boardMatrix[x][y].get_color() == "black":
                boardMatrix[x][y].recShape.border = rgb(100, 100, 100)
            else:
                boardMatrix[x][y].recShape.border = boardMatrix[x][y].get_color()

def bulk_debug_render():
    for x in range(len(boardMatrix)):
        for y in range(len(boardMatrix[x])):
            if boardMatrix[x][y].active:
                boardMatrix[x][y].recShape.border = active.color
            elif x in range(3, 7) and y <= 1:
                boardMatrix[x][y].recShape.border = "red"
            else:
                boardMatrix[x][y].recShape.border = rgb(100, 100, 100)

def hide_board():
    for x in range(len(boardMatrix)):
        for y in range(len(boardMatrix[0])):
            boardMatrix[x][y].recShape.visible = False

def show_board():
    for x in range(len(boardMatrix)):
        for y in range(len(boardMatrix[0])):
            boardMatrix[x][y].recShape.visible = True

#-- ON START FUNCTIONS --
def board_constructor():
    for x in range(len(boardMatrix)):
        for y in range(len(boardMatrix[x])):
            boardMatrix[x][y] = tile(posXY(x, y))

board_constructor()

def start_game():
    global gameStopped
    show_board()
    button.all_hide()
    next_piece()
    gameStopped = False

def main_menu():
    hide_board()
    start_button = button("Start Game", posXY(200, 180), 160, 70, start_game, textSize=20)
    settings_button = button("Settings", posXY(200, 280), 160, 70, settings, textSize=20)
    
def settings():
    pass
    

#-- SETUP FUNCTIONS --
main_menu()

def onStep():
    if not gameStopped:
        keyLabel.value = keysPressed
        #update active piece position
        gravity()
        #check to see if lines are clearable
        #render
        bulk_debug_render()
        #shader()