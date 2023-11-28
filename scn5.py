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


with open(f'./scene5.json', 'r', encoding="utf8") as file:
    scene5 = json.load(file)


#################################################
# scene 5 classes
#################################################
# player for scene5
class playerScene5(player):
    pass
#################################################
# Scene 5 function
#################################################
def loadScene5(app):
    app.text = scene5["texts"]
    # appends object of unplayableSpriteClass class and rotatingSpriteClass class to the list app.unplayableSprites
    appendToUnplayable(app, scene5, "static")
    appendToUnplayable(app, scene5, "interactable")
    appendToUnplayable(app, scene5, "rotating", rotatingSpriteClass)
    # saves the player object in app.player
    path = scene5["player"]
    app.player = playerScene5(
        "player", path["url"], path["images"], path["toDraw"], path["x"], path["y"], path["width"], path["height"], path["color"], app.unplayableSprites[1:])


def scene5Step(app):
    if app.sceneState == 0:
        loadScene5(app)
        app.sceneState += 1
    if app.sceneState == 1:
        app.sceneTicks += 1
        if app.sceneTicks == 30:
            app.sceneState = 2
    elif app.sceneState >= 2:
        app.dialogueBox.stepSelf()


def scene5OnKeyPress(app, event):
    if app.sceneState > 0 and app.sceneState < 12:
        if "enter" == event or "space" == event:
            app.sceneState += 1
    if app.sceneState == 12:
        nextScene(app)
        cleanAppVariables(app)


def scene5OnJoyPress(app, button, joystick):
    if joystick == 0:
        if app.sceneState > 0 and app.sceneState < 12:
            if button=="1":
                app.sceneState += 1
        if app.sceneState == 12:
            nextScene(app)
            cleanAppVariables(app)


def scene5Draw(app):
    # calls the draw of every object
    if 13 > app.sceneState > 1:
        for iSprite in app.unplayableSprites:
            iSprite.drawSelf()
        app.player.drawSelf()
        app.dialogueBox.drawSelf(app.text[str(app.sceneState-1)])

