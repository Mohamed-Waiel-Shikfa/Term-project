#################################################
# TERM PROJECT
# Your name: Mohamed Waiel Shikfa
# Your andrew id: mshikfa
#################################################
# import the library
from cmu_graphics import *
import json
from random import randint
from cmu_graphics.shape_logic import loadImageFromStringReference
import os
import copy
import joystick
import sys
import arabic_reshaper
from bidi.algorithm import get_display
from global_classes import *
from global_helper_functions import *
from scn0 import *
from scn1 import *
from scn2 import *
from scn3 import *
from scn4 import *
from scn5 import *
from scn6 import *
from scn7 import *
from scn8 import *
from scn9 import *
from scn10 import *
from scn11 import *
from scn12 import *
from scn100 import *



#################################################
# MVC CS3 mode functionS
#################################################
def onAppStart(app):
    # runs at the start of the game
    app.stepsPerSeconds = 30
    app.background="black"
    app.scale=1
    app.offsetx=0
    app.offsety=0
    app.year = 2061
    app.gameState = 0
    app.crntGameIndex = [0, 0]
    app.storyFlow=game["gameState"]
    app.gameState = 0
    # saves the dialogue object in app.dialogueBox
    path = game["dialogue"]
    app.dialogueBox = dialogue("dialogue", path["url"], path["images"], path["toDraw"],
                               path["x"], path["y"], path["width"], path["height"], path["color"])
    # saves the dialogue object in app.dialogueBox
    path = game["digitBox"]
    app.digitBox = digitBox("digitBox", path["url"], path["images"], path["toDraw"],
                               path["x"], path["y"], path["width"], path["height"], path["color"])
    # shader feature to develop after mvp
    path = game["shader"]
    app.shader = unplayableSpriteClass("shader", path["url"], path["images"], path["toDraw"],
                                       path["x"], path["y"], path["width"], path["height"], path["color"], opacity=path["opacity"])
    path = game["endScreen"]
    app.endScreen = unplayableSpriteClass("endScreen", path["url"], path["images"], path["toDraw"],
                                          path["x"], path["y"], path["width"], path["height"], path["color"], opacity=path["opacity"])
    cleanAppVariables(app)
    loadScene0(app)
    print("""
#################################################
###     Running Salem's Adventure....         ###
###            Have Fun!!!                    ###
#################################################
""")


def onStep(app):
    # increase debugging ticks by 1 and reflects that in the app window
    app.debuggingTicks += 1
    # rescale everything based on window size
    rescaleAll(app)
    #step scene
    if app.gameState == 0:
        scene0Step(app)
    elif app.gameState == 1:
        scene1Step(app)
    elif app.gameState == 2:
        scene2Step(app)
    elif app.gameState == 3:
        scene3Step(app)
    elif app.gameState == 4:
        scene4Step(app)
    elif app.gameState == 5:
        scene5Step(app)
    elif app.gameState == 6:
        scene6Step(app)
    elif app.gameState == 7:
        scene7Step(app)
    elif app.gameState == 8:
        scene8Step(app)
    elif app.gameState == 9:
        scene9Step(app)
    elif app.gameState == 10:
        scene10Step(app)
    elif app.gameState == 11:
        scene11Step(app)
    elif app.gameState == 12:
        scene12Step(app)
    elif app.gameState == 100:
        scene100Step(app)
    app.shader.stepSelf()


def onKeyHold(app, events):
    if app.gameState == 2:
        scene2OnKeyHold(app, events)
    elif app.gameState == 4:
        scene4OnKeyHold(app, events)
    elif app.gameState == 7:
        scene7OnKeyHold(app, events)
    elif app.gameState == 8:
        scene8OnKeyHold(app, events)


def onKeyPress(app, event):
    if app.gameState == 2:
        scene2OnKeyPress(app, event)
    elif app.gameState == 3:
        scene3OnKeyPress(app, event)
    elif app.gameState == 4:
        scene4OnKeyPress(app, event)
    elif app.gameState == 5:
        scene5OnKeyPress(app, event)
    elif app.gameState == 6:
        scene6OnKeyPress(app, event)
    elif app.gameState == 7:
        scene7OnKeyPress(app, event)
    elif app.gameState == 8:
        scene8OnKeyPress(app, event)
    elif app.gameState == 9:
        scene9OnKeyPress(app, event)
    elif app.gameState == 10:
        scene10OnKeyPress(app, event)
    elif app.gameState == 11:
        scene11OnKeyPress(app, event)
    elif app.gameState == 12:
        scene12OnKeyPress(app, event)
    elif app.gameState == 100:
        scene100OnKeyPress(app, event)
    elif app.gameState == 20 and event == "r":
        app.crntGameIndex = [0,-1]
        nextScene(app)
        cleanAppVariables(app)
        loadScene0(app)
    if event == "k" and app.gameState!=0:
        response = app.getTextInput("What would you like to name this save")
        with open("./saved games/" + response + ".txt", "w") as file:
            file.write(str(app.crntGameIndex[0])+";"+str(app.crntGameIndex[1]))


def onMousePress(app, x, y):
    if app.gameState == 0:
        scene0MousePress(app, x, y)


def redrawAll(app):
    if app.gameState == 0:
        scene0Draw(app)
    elif app.gameState == 1:
        scene1Draw(app)
    elif app.gameState == 2:
        scene2Draw(app)
    elif app.gameState == 3:
        scene3Draw(app)
    elif app.gameState == 4:
        scene4Draw(app)
    elif app.gameState == 5:
        scene5Draw(app)
    elif app.gameState == 6:
        scene6Draw(app)
    elif app.gameState == 7:
        scene7Draw(app)
    elif app.gameState == 8:
        scene8Draw(app)
    elif app.gameState == 9:
        scene9Draw(app)
    elif app.gameState == 10:
        scene10Draw(app)
    elif app.gameState == 11:
        scene11Draw(app)
    elif app.gameState == 12:
        scene12Draw(app)
    elif app.gameState == 100:
        scene100Draw(app)
    else:
        # to do : modify end screen 
        app.endScreen.drawSelf()
    # drawLine(app.width/2,0, app.width/2, app.height, fill='green')
    # drawLine(0, app.height/2, app.width,app.height/2, fill='green')

    # shader feature to develop after mvp
    app.shader.drawSelf()
    # draw the number of frame since the beginining of the game
    # drawLabel(str(app.debuggingTicks), 650, 360, fill='red', size=24)


def onJoyPress(app, button, joystick):
    if app.gameState == 0:
        scene0OnJoyPress(app, button, joystick)
    elif app.gameState == 2:
        scene2OnJoyPress(app, button, joystick)
    elif app.gameState == 3:
        scene3OnJoyPress(app, button, joystick)
    elif app.gameState == 4:
        scene4OnJoyPress(app, button, joystick)
    elif app.gameState == 5:
        scene5OnJoyPress(app, button, joystick)
    elif app.gameState == 6:
        scene6OnJoyPress(app, button, joystick)
    elif app.gameState == 7:
        scene7OnJoyPress(app, button, joystick)
    elif app.gameState == 8:
        scene8OnJoyPress(app, button, joystick)
    elif app.gameState == 9:
        scene9OnJoyPress(app, button, joystick)
    elif app.gameState == 10:
        scene10OnJoyPress(app, button, joystick)
    elif app.gameState == 11:
        scene11OnJoyPress(app, button, joystick)
    elif app.gameState == 12:
        scene12OnJoyPress(app, button, joystick)
    elif app.gameState == 100:
        scene100OnJoyPress(app, button, joystick)
    elif app.gameState == 20 and button == "0":
        app.crntGameIndex = [0,-1]
        nextScene(app)
        cleanAppVariables(app)
        loadScene0(app)
     # Make sure we can exit by pressing the "P1" button
    if button == '5':
        sys.exit(0)


def onDigitalJoyAxis(app, results, joystick):
    if app.gameState == 2:
        scene2OnDigitalJoyAxis(app, results, joystick)
    elif app.gameState == 3:
        scene3OnDigitalJoyAxis(app, results, joystick)
    elif app.gameState == 4:
        scene4OnDigitalJoyAxis(app, results, joystick)
    elif app.gameState == 7:
        scene7OnDigitalJoyAxis(app, results, joystick)
    elif app.gameState == 8:
        scene8OnDigitalJoyAxis(app, results, joystick)
    elif app.gameState == 12:
        scene12OnDigitalJoyAxis(app, results, joystick)

# load the json dictionnary in the game variable
with open('./gameGlobal.json', 'r') as file:
    game = json.load(file)


# run app
runApp(game["global"]["width"], game["global"]["height"])
