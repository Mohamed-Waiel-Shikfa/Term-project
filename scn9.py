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

with open(f'./scene9.json', 'r', encoding="utf8") as file:
    scene9 = json.load(file)


#################################################
# scene 9 classes
#################################################
class playerScene9(player):
    pass
#################################################
# Scene 9 function
#################################################
def loadScene9(app):
    app.text = scene9["texts"]
    # appends object of unplayableSpriteClass class and rotatingSpriteClass class to the list app.unplayableSprites
    appendToUnplayable(app, scene9, "static")
    path = scene9["player"]
    app.player = playerScene9(
        "player", path["url"], path["images"], path["toDraw"], path["x"], path["y"], path["width"], path["height"], path["color"], app.unplayableSprites[1:])


def scene9Step(app):
    if app.sceneState == 0:
        loadScene9(app)
        app.sceneState += 1
    if app.sceneState == 1:
        app.sceneTicks += 1
        if app.sceneTicks == 30:
            app.sceneState = 2
            app.sceneTicks=0
    if app.sceneState == 2:
        app.player.x+=6
        app.sceneTicks += 1
        if app.sceneTicks == 30:
            app.sceneState = 3
    if app.sceneState >= 3:
        app.dialogueBox.stepSelf()
    if app.sceneState==5:
        app.digitBox.stepSelf()


def scene9OnKeyPress(app, event):
    if 5> app.sceneState > 2 or app.sceneState > 5:
        if "enter" == event or "space" == event:
            dialogueSound.play(restart=True)
            app.sceneState += 1
    if app.sceneState == 7:
        if app.year<1850:
            app.crntGameIndex[0]=2
            app.crntGameIndex[1]=-1
        nextScene(app)
        cleanAppVariables(app)
    if app.sceneState==5 and "enter" == event or "space" == event:
        if app.digitBox.getCrntNumberLen()==4:
            if app.digitBox.getNumber()<1950:
                app.sceneState+=1
                app.year = app.digitBox.getNumber()
            for i in range(4):
                app.digitBox.labelText[i]=""
                app.digitBox.filled=0
    elif app.sceneState==5 and event.isdigit():
        if app.digitBox.getCrntNumberLen()!=4:
            app.digitBox.newDigit(event)


def scene9OnJoyPress(app, button, joystick):
    if joystick == 0:
        if 5> app.sceneState > 2 or app.sceneState > 5:
            if button=="1":
                dialogueSound.play(restart=True)
                app.sceneState += 1
        if app.sceneState == 7:
            if app.year<1850:
                app.crntGameIndex[0]=2
                app.crntGameIndex[1]=-1
            nextScene(app)
            cleanAppVariables(app)
        if app.sceneState==5 and button=="1":
            if app.digitBox.getCrntNumberLen()==4:
                if app.digitBox.getNumber()<1950:
                    app.sceneState+=1
                    app.year = app.digitBox.getNumber()
                for i in range(4):
                    app.digitBox.labelText[i]=""
                    app.digitBox.filled=0
                    app.digitCounter=-1
            elif app.digitBox.labelText[app.digitBox.filled]!="":
                app.digitBox.filled+=1
                app.digitCounter=-1
        elif app.sceneState==5 and button=="0":
            app.digitCounter+=1
            app.digitBox.newDigit(app.digitCounter%10, True)


def scene9Draw(app):
    if app.sceneState>=1:
        for iSprite in app.unplayableSprites:
            iSprite.drawSelf()
    if app.sceneState>=2:
        app.player.drawSelf()
    if 7 > app.sceneState > 2:
        app.dialogueBox.drawSelf(app.text[str(app.sceneState-2)])
    if app.sceneState==5:
        app.digitBox.drawSelf("To when do you think Salem and Samer should time travel?","Has to be a year before 1950", "(remeinder to read the dialogue please)")

