# import the library
from cmu_graphics import *
import json
import os
from global_classes import *
from global_helper_functions import *

import pathlib
cntPath = pathlib.Path(__file__).parent.resolve()
music = Sound(f'file:///{cntPath}/sounds/main menu2.mp3')

with open(f'./scene0.json', 'r', encoding="utf8") as file:
    scene0 = json.load(file)

#################################################
# scene 0 classes
#################################################
# buttons for scene0
class buttonScene0(button):
    def selfOnJoyPress(self, app, button):
        if self.name == "1" and button == "9":
            self.answer(app)

    
    def answer(self, app):
        if self.name == "1":
            music.play()
            music.pause()
            nextScene(app)
            cleanAppVariables(app)
        else:
            response = app.getTextInput(
                "Input saved game name (if game name doesn't exist,nothing will happen).")
            if os.path.isfile("./saved games/" + response + ".txt"):
                with open("./saved games/" + response + ".txt", "r") as file:
                    data=file.read()
                app.crntGameIndex = data.split(";")
                app.crntGameIndex[0]=int(app.crntGameIndex[0])
                app.crntGameIndex[1]=int(app.crntGameIndex[1])-1
                music.play()
                music.pause()
                nextScene(app)
                cleanAppVariables(app)
            else:
                print("File Not Found")       
#################################################
# Scene 0 function
#################################################
def loadScene0(app):
    music.play(restart=True, loop=True)
    cleanAppVariables(app)
    # appends object of unplayableSpriteClass class and rotatingSpriteClass class to the list app.unplayableSprites
    appendToUnplayable(app, scene0, "bg")
    appendToButton(app, scene0, "buttons", buttonScene0)


def scene0Step(app):
    # calls the onStep of every object
    for iSprite in app.unplayableSprites:
        iSprite.stepSelf()
    for ibutton in app.buttons:
        ibutton.stepSelf()


def scene0MousePress(app, x, y):
    for ibutton in app.buttons:
        ibutton.selfMousePress(app, x, y)


def scene0OnJoyPress(app, button, joystick):
    if joystick == 0:
        for ibutton in app.buttons:
            ibutton.selfOnJoyPress(app, button)


def scene0Draw(app):
    for iSprite in app.unplayableSprites:
        iSprite.drawSelf()
    for iSprite in app.buttons:
        iSprite.drawSelf()
