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

import pathlib
cntPath = pathlib.Path(__file__).parent.resolve()
dialogueSound = Sound(f'file:///{cntPath}/sounds/Hotel lobby music.mp3')

with open(f'./scene11.json', 'r', encoding="utf8") as file:
    scene11 = json.load(file)


#################################################
# scene 11 classes
#################################################
#################################################
# Scene 11 function
#################################################
def loadScene11(app):
    app.text = scene11["texts"]
    # appends object of unplayableSpriteClass class and rotatingSpriteClass class to the list app.unplayableSprites
    appendToUnplayable(app, scene11, "static")


def scene11Step(app):
    if app.sceneState == 0:
        loadScene11(app)
        app.sceneState += 1
    if app.sceneState == 1:
        app.unplayableSprites[0].stepSelf()
        app.sceneTicks += 1
        if app.sceneTicks == 60:
            app.sceneState = 2
            app.sceneTicks=0
    if app.sceneState == 2:
        app.unplayableSprites[0].stepSelf()
        app.unplayableSprites[1].stepSelf()
        app.sceneTicks += 1
        if app.sceneTicks == 30:
            app.sceneState = 3
            app.unplayableSprites[1].todraw=[1,0]
    elif app.sceneState >= 3:
        app.unplayableSprites[0].stepSelf()
        app.dialogueBox.stepSelf()


def scene11OnKeyPress(app, event):
    if app.sceneState >= 3 and app.sceneState < 9:
        if "enter" == event or "space" == event:
            dialogueSound.play(restart=True)
            app.sceneState += 1
    if app.sceneState == 9:
        nextScene(app)
        cleanAppVariables(app)


def scene11OnJoyPress(app, button, joystick):
    if joystick == 0:
        if app.sceneState >= 3 and app.sceneState < 9:
            if button == "1":
                dialogueSound.play(restart=True)
                app.sceneState += 1
        if app.sceneState == 9:
            nextScene(app)
            cleanAppVariables(app)


def scene11Draw(app):
    if app.sceneState==1:
        for iSprite in app.unplayableSprites[:-1]:
            iSprite.drawSelf()
    if app.sceneState>=2:
        for iSprite in app.unplayableSprites:
            iSprite.drawSelf()
    if 9 > app.sceneState > 2:
        app.dialogueBox.drawSelf(app.text[str(app.sceneState-2)])


