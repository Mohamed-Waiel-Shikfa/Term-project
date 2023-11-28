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

with open(f'./scene7.json', 'r', encoding="utf8") as file:
    scene7 = json.load(file)

#################################################
# scene 7 classes
#################################################
class playerScene7(player):
    def stepSelf(self):
        super().stepSelf()
        if self.allowedMovement(self.movingSpeed, 0)[0]=="door" and not self.allowedMovement(self.movingSpeed, 0)[1]:
            return True
        return False
#################################################
# Scene 7 function
#################################################
def loadScene7(app):
    app.text = scene7["texts"]
    # appends object of unplayableSpriteClass class and rotatingSpriteClass class to the list app.unplayableSprites
    appendToUnplayable(app, scene7, "static")
    path = scene7["player"]
    app.player = playerScene7(
        "player", path["url"], path["images"], path["toDraw"], path["x"], path["y"], path["width"], path["height"], path["color"], app.unplayableSprites[1:])


def scene7Step(app):
    if app.sceneState == 0:
        loadScene7(app)
        app.sceneState += 1
    if app.sceneState == 1:
        app.sceneTicks += 1
        if app.sceneTicks == 30:
            app.sceneState = 2
            app.sceneTicks=0
    if app.sceneState == 2:
        app.player.stepSelf()
        app.sceneTicks += 1
        if app.sceneTicks == 30:
            app.sceneState = 3
            app.player.width=80
            app.player.height=80
            app.player.x+=15
            app.player.y+=10
            app.player.todraw=[1,0]
    if app.sceneState >= 3:
        app.dialogueBox.stepSelf()
    if app.sceneState == 7:
        if app.player.stepSelf():
            app.sceneState=8


def scene7OnKeyPress(app, event):
    if 7 > app.sceneState > 2 or 15 > app.sceneState > 8:
        if "enter" == event or "space" == event:
            dialogueSound.play(restart=True)
            app.sceneState += 1
    if app.sceneState==8 and "enter" == event or "space" == event:
        if app.digitBox.getCrntNumberLen()==4:
            if app.digitBox.getNumber()==1729:
                app.sceneState+=1
            for i in range(4):
                app.digitBox.labelText[i]=""
                app.digitBox.filled=0
    elif app.sceneState==8 and event.isdigit():
        if app.digitBox.getCrntNumberLen()!=4:
            app.digitBox.newDigit(event)
    if app.sceneState == 10:
        nextScene(app)
        cleanAppVariables(app)


def scene7OnJoyPress(app, button, joystick):
    if joystick == 0:
        if 7 > app.sceneState > 2 or 15 > app.sceneState > 8:
            if button == "1":
                dialogueSound.play(restart=True)
                app.sceneState += 1
        if app.sceneState==8 and button=="1":
            if app.digitBox.getCrntNumberLen()==4:
                if app.digitBox.getNumber()==1729:
                    app.sceneState+=1
                for i in range(4):
                    app.digitBox.labelText[i]=""
                    app.digitBox.filled=0
                    app.digitCounter=-1
            elif app.digitBox.labelText[app.digitBox.filled]!="":
                app.digitBox.filled+=1
                app.digitCounter=-1
        elif app.sceneState==8 and button=="0":
            app.digitCounter+=1
            app.digitBox.newDigit(app.digitCounter%10, True)
        if app.sceneState == 10:
            nextScene(app)
            cleanAppVariables(app)


def scene7OnKeyHold(app, events):
    # calls keyHold of the player
    # app.player.selfKeyHold(events)
    if app.sceneState == 7:
        app.player.selfKeyHold(events)


def scene7OnDigitalJoyAxis(app, results, joystick):
    if joystick==0:
        if app.sceneState == 7:
            app.player.selfKeyHold(results)


def scene7Draw(app):
    if app.sceneState>=1:
        for iSprite in app.unplayableSprites:
            iSprite.drawSelf()
    if app.sceneState>=2:
        app.player.drawSelf()
    if app.sceneState==8:
        app.digitBox.drawSelf("What is the smallest number that can be written as the sum of", "two cubes in two different way; in other term what is the number", "n=x**3+y**3=a**3+b**3, where a,b,x,y are positive integers")
    if 7 > app.sceneState > 2:
        app.dialogueBox.drawSelf(app.text[str(app.sceneState-2)])
    if app.sceneState == 9:
        app.dialogueBox.drawSelf(app.text["5"])

