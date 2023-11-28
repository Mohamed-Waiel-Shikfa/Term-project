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
dialogueSound = Sound(f'file:///{cntPath}/sounds/dialogue3.mp3')
portalSound = Sound(f'file:///{cntPath}/sounds/portal.mp3')

with open(f'./scene6.json', 'r', encoding="utf8") as file:
    scene6 = json.load(file)


#################################################
# scene 6 classes
#################################################

#################################################
# Scene 6 function
#################################################


def loadScene6(app):
    app.text = scene6["texts"]
    # appends object of unplayableSpriteClass class and rotatingSpriteClass class to the list app.unplayableSprites
    appendToUnplayable(app, scene6, "static")


def scene6Step(app):
    if app.sceneState == 0:
        loadScene6(app)
        app.sceneState += 1
    if app.sceneState == 1:
        for isprite in app.unplayableSprites[:-1]:
            isprite.stepSelf()
        app.sceneTicks += 1
        if app.sceneTicks == 30:
            portalSound.play()
            app.sceneState = 2
            app.sceneTicks=0
    if app.sceneState == 2:
        for isprite in app.unplayableSprites:
            isprite.stepSelf()
        app.sceneTicks += 1
        if app.sceneTicks == 30:
            portalSound.pause()
            app.sceneState = 3
            app.unplayableSprites[1].todraw=[1,0]
    if app.sceneState >= 3:
        for isprite in app.unplayableSprites:
            isprite.stepSelf()
        app.dialogueBox.stepSelf()


def scene6OnKeyPress(app, event):
    if app.sceneState > 2 and app.sceneState < 10:
        if "enter" == event or "space" == event:
            dialogueSound.play(restart=True)
            app.sceneState += 1
    if app.sceneState == 10:
        nextScene(app)
        cleanAppVariables(app)


def scene6OnJoyPress(app, button, joystick):
    if joystick == 0:
        if app.sceneState > 2 and app.sceneState < 10:
            if button == "1":
                dialogueSound.play(restart=True)
                app.sceneState += 1
        if app.sceneState == 10:
            nextScene(app)
            cleanAppVariables(app)


def scene6Draw(app):
    if app.sceneState==1:
        for iSprite in app.unplayableSprites[:-1]:
            iSprite.drawSelf()
    if app.sceneState==2:
        for iSprite in app.unplayableSprites:
            iSprite.drawSelf()
    if 11 > app.sceneState > 2:
        for iSprite in app.unplayableSprites:
            iSprite.drawSelf()
        app.dialogueBox.drawSelf(app.text[str(app.sceneState-2)])

