# import the library
from cmu_graphics import *
import json
from global_classes import *
from global_helper_functions import *
from tetris import *

import pathlib
cntPath = pathlib.Path(__file__).parent.resolve()
gameover = Sound(f'file:///{cntPath}/sounds/game over.mp3')

with open(f'./scene100.json', 'r', encoding="utf8") as file:
    scene100 = json.load(file)


#################################################
# Scene 100 classes
#################################################
#################################################
# Scene 100 function
#################################################
def loadScene100(app):
    gameover.play(restart=True)
    appendToUnplayable(app, scene100, "gameOver")


def scene100Step(app):
    if app.sceneState == 0:
        loadScene100(app)
        app.sceneState += 1
    if app.sceneState == 1:
        app.sceneTicks += 1
        for iSprite in app.unplayableSprites:
            iSprite.stepSelf()


def scene100OnKeyPress(app, event):
    if event == "r":
        if app.crntGameIndex[0]==1:
            app.crntGameIndex[0]=0
            app.crntGameIndex[1]=2
        elif app.crntGameIndex[0]==2:
            app.crntGameIndex[0]=0
            app.crntGameIndex[1]=11
        app.gameState = app.storyFlow[app.crntGameIndex[0]][app.crntGameIndex[1]]
        gameover.pause()
        cleanAppVariables(app)


def scene100OnJoyPress(app, button, joystick):
    if joystick == 0:
        if button == "0":
            if app.crntGameIndex[0]==1:
                app.crntGameIndex[0]=0
                app.crntGameIndex[1]=2
            elif app.crntGameIndex[0]==2:
                app.crntGameIndex[0]=0
                app.crntGameIndex[1]=11
            app.gameState = app.storyFlow[app.crntGameIndex[0]][app.crntGameIndex[1]]
            cleanAppVariables(app)


def scene100Draw(app):
    for iSprite in app.unplayableSprites:
        iSprite.drawSelf()
    drawLabel("Press R (on pc) or B (on arcade box) to try again.", 660*app.scale+app.offsetx, 450*app.scale+app.offsety, size=37.5*app.scale*2/3, fill="orange")
