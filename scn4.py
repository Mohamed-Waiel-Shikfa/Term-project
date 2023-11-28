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

with open(f'./scene4.json', 'r', encoding="utf8") as file:
    scene4 = json.load(file)


#################################################
# scene 4 classes
#################################################
class playerScene4(player):
    def stepSelf(self, ennemies):
        self.notAllowed = []
        for i in ennemies:
            data = repr(i)
            data = data.split(";")
            self.notAllowed.append((data[1], (float(data[5]), float(data[6]), float(
                data[5])+float(data[7]), float(data[6])+float(data[8]))))
    def removeEnnemie(self, i):
        if self.notAllowed[i][0] == "ennemie":
            j = self.notAllowed[i][1]
            if self.isPlayerColliding(self.x, self.y, self.x+self.width, self.y+self.height, *j):
                return True
class ennemie(unplayableSpriteClass):
    def __init__(self, *args, angle=0, opacity=100):
        super().__init__(*args, angle=angle, opacity=opacity)
        self.speed = 0.5

    def stepSelf(self):
        super().stepSelf()
        if self.speed > 0:
            self.speed = randint(5, 20)/10
        self.y += self.speed
        self.x += randint(-50, 50)/5
        if self.x > 1290:
            self.x = 1290
        if self.x < 0:
            self.x = 0
        if self.y > 720:
            return 0
        elif self.y < 0:
            return 1
#################################################
# Scene 4 function
#################################################
def loadScene4(app):
    app.ennemie = 60
    app.text = scene4["texts"]
    # appends object of unplayableSpriteClass class and rotatingSpriteClass class to the list app.unplayableSprites
    appendToUnplayable(app, scene4, "static")
    for i in range(randint(2, 7)):
        appendToUnplayable(app, scene4, "ennemie", ennemie)
        app.unplayableSprites[-1].x = randint(100, 1200)
    # saves the player object in app.player
    path = scene4["player"]
    app.player = playerScene4(
        "player", path["url"], path["images"], path["toDraw"], path["x"], path["y"], path["width"], path["height"], path["color"], app.unplayableSprites[1:])


def scene4Step(app):
    if app.sceneState == 0:
        loadScene4(app)
        app.sceneState += 1
    if app.sceneState == 1:
        app.unplayableSprites[0].stepSelf()
        app.sceneTicks += 1
        if app.sceneTicks == 30:
            app.sceneState = 2
    elif 7 > app.sceneState > 1:
        app.dialogueBox.stepSelf()
        app.unplayableSprites[0].stepSelf()
    elif app.sceneState == 7:
        app.dialogueBox.todraw = [0, 0]
        app.player.stepSelf(app.unplayableSprites)
        for i in range(len(app.unplayableSprites)):
            if app.player.removeEnnemie(i):
                app.unplayableSprites[i].speed = -10
                app.unplayableSprites[i].angle = 180
        if len(app.unplayableSprites) < 7 and app.ennemie > 0:
            for i in range(randint(2, 15)):
                appendToUnplayable(app, scene4, "ennemie", ennemie)
                app.unplayableSprites[-1].x = randint(50,1255)
        elif len(app.unplayableSprites) == 1 and app.ennemie <= 0:
            app.sceneState += 1
        # calls the onStep of every object
        unplayableSpritesCopy = app.unplayableSprites[:]
        for iSprite in unplayableSpritesCopy:
            response = iSprite.stepSelf()
            if response == 0:
                app.gameState = 100
                cleanAppVariables(app)
            elif response == 1:
                app.unplayableSprites.remove(iSprite)
                app.ennemie -= 1
    else:
        app.unplayableSprites[0].stepSelf()
        app.dialogueBox.stepSelf()


def scene4OnKeyHold(app, events):
    # calls keyHold of the player
    # app.player.selfKeyHold(events)
    if app.sceneState == 7:
        app.player.selfKeyHold(events)


def scene4OnKeyPress(app, event):
    if 7 > app.sceneState > 1 or 10 > app.sceneState > 7:
        if "enter" == event or "space" == event:
            dialogueSound.play(restart=True)
            app.sceneState += 1
    if app.sceneState == 10:
        nextScene(app)
        cleanAppVariables(app)


def scene4OnJoyPress(app, button, joystick):
    if joystick == 0:
        if 7 > app.sceneState > 1 or 10 > app.sceneState > 7:
            if button=="1":
                dialogueSound.play(restart=True)
                app.sceneState += 1
        if app.sceneState == 10:
            nextScene(app)
            cleanAppVariables(app)


def scene4OnDigitalJoyAxis(app, results, joystick):
    if joystick==0:
        if app.sceneState == 7:
            app.player.selfKeyHold(results)


def scene4Draw(app):
    # calls the draw of every object
    if app.sceneState > 0:
        for iSprite in app.unplayableSprites:
            iSprite.drawSelf()
        app.player.drawSelf()
    if 7 > app.sceneState > 1 or 10 > app.sceneState > 7:
        app.dialogueBox.drawSelf(app.text[str(app.sceneState-1)])

