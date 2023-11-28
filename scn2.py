# import the library
from cmu_graphics import *
import json
from random import randint
from global_classes import *
from global_helper_functions import *

import pathlib
cntPath = pathlib.Path(__file__).parent.resolve()
dialogueSound = Sound(f'file:///{cntPath}/sounds/dialogue3.mp3')
succes=Sound(f'file:///{cntPath}/sounds/succes.mp3')

with open(f'./scene2.json', 'r', encoding="utf8") as file:
    scene2 = json.load(file)


#################################################
# scene 2 classes
#################################################
# class for the things player can interact with in scene2
class scene2Interactable(unplayableSpriteClass):
    # updates the self view arguments of the object depending on the game state
    def stepSelf(self, sceneState=0):
        if sceneState == 4 and self.name == "table1" or sceneState == 5 and self.name == "table2" or sceneState == 6 and self.name == "wallmap":
            self.todraw[1] = 1
            self.x = 0
            self.y = 0
            self.width = 1305
            self.height = 720
        else:
            path = scene2["interactable"][self.name]
            self.x = path["x"]
            self.y = path["y"]
            self.width = path["width"]
            self.height = path["height"]
            self.todraw[1] = 0
# player for scene2
class playerScene2(player):
    # respond to keyPress -> collision and object examination
    def selfKeyPress(self, event, app):
        if event == "x" or event=="2":
            if self.allowedMovement(0, -self.movingSpeed)[0] in ["table1", "table2", "wallmap"]:
                self.changeSceneState((0, -self.movingSpeed), app)
            elif self.allowedMovement(0, self.movingSpeed)[0] in ["table1", "table2", "wallmap"]:
                self.changeSceneState((0, self.movingSpeed), app)
            elif self.allowedMovement(-self.movingSpeed, 0)[0] in ["table1", "table2", "wallmap"]:
                self.changeSceneState((-self.movingSpeed, 0), app)
            elif self.allowedMovement(self.movingSpeed, 0)[0] in ["table1", "table2", "wallmap"]:
                self.changeSceneState((self.movingSpeed, 0), app)
            elif self.allowedMovement(self.movingSpeed, 0)[0] == "car" or self.allowedMovement(self.movingSpeed, 0)[0] == "salem":
                self.changeSceneState((self.movingSpeed, 0), app)
            elif self.allowedMovement(0, self.movingSpeed)[0] == "car":
                self.changeSceneState((0, self.movingSpeed), app)

    # changes the game state for the story flow
    def changeSceneState(self, arg, app):
        if self.allowedMovement(*arg)[0] == "table1":
            app.sceneState = 4
        elif self.allowedMovement(*arg)[0] == "table2":
            app.sceneState = 5
        elif self.allowedMovement(*arg)[0] == "wallmap":
            app.sceneState = 6
        elif (self.allowedMovement(*arg)[0] == "car" or self.allowedMovement(*arg)[0] == "salem") and app.Task[2]:
            app.sceneState = 7

    def stepSelf(self):
        super().stepSelf()
        if not (self.allowedMovement(0, -self.movingSpeed)[1] and self.allowedMovement(0, self.movingSpeed)[1] and self.allowedMovement(-self.movingSpeed, 0)[1] and self.allowedMovement(self.movingSpeed, 0)[1]):
            self.todraw[1] = 1
        else:
            self.todraw[1] = 0
#################################################
# Scene 2 function
#################################################
def loadScene2(app):
    app.Task = [False]*3
    app.text = scene2["texts"]
    # appends object of unplayableSpriteClass class and rotatingSpriteClass class to the list app.unplayableSprites
    appendToUnplayable(app, scene2, "static")
    appendToUnplayable(app, scene2, "interactable", scene2Interactable)
    appendToUnplayable(app, scene2, "rotating", rotatingSpriteClass)
    # saves the player object in app.player
    path = scene2["player"]
    app.player = playerScene2(
        "player", path["url"], path["images"], path["toDraw"], path["x"], path["y"], path["width"], path["height"], path["color"], app.unplayableSprites[1:])


def scene2Step(app):
    if app.sceneState == 0:
        loadScene2(app)
        app.sceneState += 1
    if app.sceneState == 1:
        app.sceneTicks += 1
        if app.sceneTicks == 30:
            app.sceneState = 2
    elif app.sceneState == 2:
        app.dialogueBox.stepSelf()
    elif app.sceneState == 3:
        app.dialogueBox.todraw = [0, 0]
        # calls the onStep of every object
        for iSprite in app.unplayableSprites:
            iSprite.stepSelf()
        if randint(0,30)==6:
            app.unplayableSprites[2].todraw[0]=1
        elif randint(0,30)==3:
            app.unplayableSprites[2].todraw[0]=0
            app.unplayableSprites[2].todraw[1]=0
        app.player.stepSelf()
    elif app.sceneState == 4:
        app.unplayableSprites[6].stepSelf(sceneState=app.sceneState)
        app.Task[0] = True
    elif app.sceneState == 5:
        app.unplayableSprites[7].stepSelf(sceneState=app.sceneState)
        app.Task[1] = True
    elif app.sceneState == 6:
        app.unplayableSprites[8].stepSelf(sceneState=app.sceneState)
        if app.Task[0] and app.Task[1]:
            succes.play(restart=True)
            app.Task[2] = True
    else:
        app.dialogueBox.stepSelf()
    if app.sceneState==15:
        app.digitBox.stepSelf()


def scene2OnKeyHold(app, events):
    # calls keyHold of the player
    # app.player.selfKeyHold(events)
    if app.sceneState == 3:
        app.player.selfKeyHold(events)


def scene2OnKeyPress(app, event):
    if app.sceneState == 3:
        app.player.selfKeyPress(event, app)
    elif app.sceneState in [4, 5, 6]:
        app.sceneState = 3
    elif app.sceneState == 2 or 15>app.sceneState > 6 or 17>app.sceneState > 15:
        if "enter" == event or "space" == event:
            dialogueSound.play(restart=True)
            app.sceneState += 1
    if app.sceneState==15 and "enter" == event or "space" == event:
        if app.digitBox.getCrntNumberLen()==4:
            if app.digitBox.getNumber()>2061:
                app.sceneState+=1
                app.year = app.digitBox.getNumber()
            for i in range(4):
                app.digitBox.labelText[i]=""
                app.digitBox.filled=0
    elif app.sceneState==15 and event.isdigit():
        if app.digitBox.getCrntNumberLen()!=4:
            app.digitBox.newDigit(event)
    if app.sceneState == 17:
        if app.year>2200:
            app.crntGameIndex[0]=1
            app.crntGameIndex[1]=-1
        nextScene(app)
        cleanAppVariables(app)


def scene2OnJoyPress(app, button, joystick):
    if joystick == 0:
        if app.sceneState == 3:
            app.player.selfKeyPress(button, app)
        elif app.sceneState in [4, 5, 6]:
            app.sceneState = 3
        elif app.sceneState == 2 or 15>app.sceneState > 6 or 17>app.sceneState > 15:
            if button=="1":
                dialogueSound.play(restart=True)
                app.sceneState += 1
        if app.sceneState==15 and button=="1":
            if app.digitBox.getCrntNumberLen()==4:
                if app.digitBox.getNumber()>2061:
                    app.sceneState+=1
                    app.year = app.digitBox.getNumber()
                for i in range(4):
                    app.digitBox.labelText[i]=""
                    app.digitBox.filled=0
                    app.digitCounter=-1
            elif app.digitBox.labelText[app.digitBox.filled]!="":
                app.digitBox.filled+=1
                app.digitCounter=-1
        elif app.sceneState==15 and button=="0":
            app.digitCounter+=1
            app.digitBox.newDigit(app.digitCounter%10, True)
        if app.sceneState == 17:
            if app.year>2200:
                app.crntGameIndex[0]=1
                app.crntGameIndex[1]=-1
            nextScene(app)
            cleanAppVariables(app)


def scene2OnDigitalJoyAxis(app, results, joystick):
    if joystick==0:
        if app.sceneState == 3:
            app.player.selfKeyHold(results)


def scene2Draw(app):
    # calls the draw of every object
    if app.sceneState in [1, 2, 3]:
        for iSprite in app.unplayableSprites:
            iSprite.drawSelf()
        app.player.drawSelf()
    elif app.sceneState == 4:
        app.unplayableSprites[6].drawSelf()
    elif app.sceneState == 5:
        app.unplayableSprites[7].drawSelf()
    elif app.sceneState == 6:
        app.unplayableSprites[8].drawSelf()
    if 7>app.sceneState >3:
        drawRect(app.offsetx,app.offsety,1305*app.scale, 720*app.scale, fill="cyan", opacity=30)
    if app.sceneState == 2:
        app.dialogueBox.drawSelf(app.text["1"])
    if app.sceneState==15:
        for iSprite in app.unplayableSprites:
            iSprite.drawSelf()
        app.player.drawSelf()
        app.dialogueBox.drawSelf(app.text[str(app.sceneState-6)])
        app.digitBox.drawSelf("To when do you think Salem and Samer should time travel?","Has to be a year in the futur", "(reminder to please read the dialogue).")
    elif app.sceneState > 15:
        for iSprite in app.unplayableSprites:
            iSprite.drawSelf()
        app.player.drawSelf()
        app.dialogueBox.drawSelf(app.text[str(app.sceneState-6)])
    elif app.sceneState > 6:
        for iSprite in app.unplayableSprites:
            iSprite.drawSelf()
        app.player.drawSelf()
        app.dialogueBox.drawSelf(app.text[str(app.sceneState-5)])

