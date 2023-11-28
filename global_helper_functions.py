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


#################################################
# helper function
#################################################
def appendToUnplayable(app, scene, key, toClass=unplayableSpriteClass):
    for key, value in scene[key].items():
        app.unplayableSprites.append(toClass(
            key, value["url"], value["images"], value["toDraw"], value["x"], value["y"], value["width"], value["height"], value["color"]))


def appendToButton(app, scene, key, toClass=button):
    for key, value in scene[key].items():
        app.buttons.append(toClass(
            key, value["url"], value["images"], value["toDraw"], value["x"], value["y"], value["width"], value["height"], value["color"]))


def cleanAppVariables(app):
    app.unplayableSprites = []
    app.buttons = []
    app.sceneState = 0
    app.sceneTicks = 0
    app.Task = []
    app.text = []
    app.player = None
    app.dialogueBox.todraw=[0,0]
    app.debuggingTicks = 0
    app.stepsPerSecond=30
    app.digitCounter=-1


def rescaleAll(app):
    app.scale=min(app.width/1305, app.height/720)
    if app.scale == app.height/720:
        app.offsetx=(app.width/1305-app.height/720)*app.width/2
        app.offsety=0
    else:
        app.offsety=(app.height/720-app.width/1305)*app.height/2
        app.offsetx=0
    for isprite in app.unplayableSprites:
        isprite.scale=app.scale
        isprite.offsetx=app.offsetx
        isprite.offsety=app.offsety
    for isprite in app.buttons:
        isprite.scale=app.scale 
        isprite.offsetx=app.offsetx
        isprite.offsety=app.offsety
    if app.player:
        app.player.scale=app.scale 
        app.player.offsetx=app.offsetx
        app.player.offsety=app.offsety
    app.dialogueBox.scale=app.scale 
    app.dialogueBox.offsetx=app.offsetx
    app.dialogueBox.offsety=app.offsety
    app.digitBox.scale=app.scale 
    app.digitBox.offsetx=app.offsetx
    app.digitBox.offsety=app.offsety
    app.endScreen.scale=app.scale 
    app.endScreen.offsetx=app.offsetx
    app.endScreen.offsety=app.offsety
    app.shader.scale=app.scale 
    app.shader.offsetx=app.offsetx
    app.shader.offsety=app.offsety


def nextScene(app):
    app.crntGameIndex[1] +=1
    app.gameState=app.storyFlow[app.crntGameIndex[0]][app.crntGameIndex[1]]

