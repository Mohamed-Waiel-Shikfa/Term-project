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

with open(f'./scene1.json', 'r', encoding="utf8") as file:
    scene1 = json.load(file)

#################################################
# Scene 1 classes
#################################################
#################################################
# Scene 1 function
#################################################


def loadScene1(app):
    appendToUnplayable(app, scene1, "loading")


def scene1Step(app):
    if app.sceneState == 0:
        loadScene1(app)
        app.sceneState += 1
    if app.sceneState == 1:
        app.sceneTicks += 1
        for iSprite in app.unplayableSprites:
            iSprite.stepSelf()
        if app.sceneTicks == 60:
            nextScene(app)
            cleanAppVariables(app)


def scene1Draw(app):
    drawRect(0, 0, 1305, 720)
    for iSprite in app.unplayableSprites:
        iSprite.drawSelf()

