import time

spaces = []
s = 0.25

def choice(text, choices):
    time.sleep(s)
    print("What do you do next?")
    time.sleep(s)
    result = input(text)
    try: result = int(result)
    except: print("Input must be a number\n")
    while result not in choices:
        print(result + " is not a valid option.")
        result = input(text)
        try: result = int(result)
        except: print("Input must be a number\n")
    print("")
    return result

class space:
    def __init__(self, name, flavorText, choiceText, choices):
        global spaces
        self.name = name
        self.flav = flavorText
        self.cho = choiceText
        self.choices = choices
        spaces.append(self)
        self.first = True

    @staticmethod
    def go(name):
        for i in spaces:
            if i.name == name:
                c = i
        if c.first:
            print(c.flav + "\n")
        c.first = False
        time.sleep(1)
        print("-={ you have entered the " + c.name + " }=-\n")
        time.sleep(1)
        inp = choice(c.cho, c.choices)
        for i in c.choices:
            if i == inp:
                space.go(c.choices.get(inp))


print('''▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
█▄▄ ▄▄█▀▄▄▀█ ▄▄▀█ ▄▀███ ▄▄▀█ ▄▀█▀███▀█ ▄▄█ ▄▄▀█▄ ▄█ ██ █ ▄▄▀█ ▄▄█
███ ███ ██ █ ▀▀ █ █ ███ ▀▀ █ █ ██ ▀ ██ ▄▄█ ██ ██ ██ ██ █ ▀▀▄█ ▄▄█
███ ████▄▄██▄██▄█▄▄████ ██ █▄▄████▄███▄▄▄█▄██▄██▄███▄▄▄█▄█▄▄█▄▄▄█
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀''')
print('''              _         _
  __   ___.--'_`.     .'_`--.___   __
 ( _`.'. -   'o` )   ( 'o`   - .`.'_ )
 _\.'_'      _.-'     `-._      `_`./_
( \`. )    //\`         '/\\\    ( .'/ )
 \_`-'`---'\\\__,       ,__//`---'`-'_/
  \`        `-\         /-'        '/
   `                               '   ''')

hallText = "    The weather is starting to turn, so you all gather beneath the hill. Among the sea of toads bustling around the floor of the opening (all in exquisite dress, thoroughly respectable folk), you see that the kind toads have presented you all with a selection of sturdy old teacups, and a basket of fresh seedcakes. The procession of toads carrying these to you set down their baskets, step out from under them, and give a polite little bob before bloomphing on away."
mainHall = space("Main Hall", hallText, "[1 : Head for the door]  [2 : Thank the toads for their troubles] (type a number):", {1 : "Entrance", 2 : "Kitchen"})

entranceText = "    The opening is well lit against the grey by two little candles, and with your back to the Toad Home, you watch as the rain slowly covers the road forward as it arcs away into the trees. You are safe from the weather here for now."
entrance = space("Entrance", entranceText, "[1 : Return to the warmth of the festivities] [2 : Venture into the percipitate]: ", {1 : "Main Hall", 2 : "Cottage Path"})

kitchenText = "    The toads recipricate your gratitude. It is not their custom to let weary travelers go hungry."
kitchen = space("Kitchen", kitchenText, "[1 : Return to the Main Hall]: ", {1 : "Main Hall"})

cottagePathText = "    You slip into the coming nightfall unseen. "
cottagePath = space("Cottage Path", cottagePathText, "[1 : Turn back] [2 : Venture onward]: ", {1 : "Entrance", 2 : "Onward"})

onwardText = "I didn't think you would get this far......."
onward = space("Onward", onwardText, "[1 : Retrace your steps]: ", {1 : "Cottage Path"})

space.go("Main Hall")