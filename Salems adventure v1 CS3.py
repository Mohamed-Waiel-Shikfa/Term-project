#################################################
# TERM PROJECT
#
# Your name: Mohamed Waiel Shikfa
# Your andrew id: mshikfa
#################################################
# import the library
from cmu_graphics import *
import json
from random import randint
from cmu_graphics.shape_logic import loadImageFromStringReference

#################################################
# classes
#################################################


# class for all unplayable sprite
class unplayableSpriteClass():
    # initiate the argument of the sprite by loading data from json file
    id = 0

    def __init__(self, *args, angle=0, opacity=100):
        unplayableSpriteClass.id += 1
        self.id = unplayableSpriteClass.id
        self.name, self.urls, self.images, self.todraw, self.x, self.y, self.width, self.height, self.color = args
        self.angle, self.opacity = angle, opacity
        # images
        self.view = []
        for i, url in enumerate(self.urls):
            temp = []
            for image in self.images[i]:
                temp.append(loadImageFromStringReference(url + image))
            self.view.append(temp)

    # used to debugg, get info for player and make the class feel more complete
    def __repr__(self):
        return f'{self};{self.urls};{self.images};{self.todraw};{self.x};{self.y};{self.width};{self.height};{self.angle};{self.opacity};{self.color}'

    def __str__(self):
        return f'{self.id};{self.name}'

    # updates the data of the sprite, aka nothing for static sprite
    def stepSelf(self):
        pass

    # draw the sprite with the argument loaded from the json and updated with the function stepSelf
    def drawSelf(self):
        drawImage(self.view[self.todraw[0]][self.todraw[1]], self.x,
                  self.y, width=self.width, height=self.height, rotateAngle=self.angle, opacity=self.opacity)


# class for all rotating sprite as rotating in pixel software is really hard
class rotatingSpriteClass(unplayableSpriteClass):
    # initiate the same argument as the parent class plus some more by loading data from json file
    def __init__(self, *args, angle=0, opacity=100):
        super().__init__(*args, angle=angle, opacity=opacity)
        self.animationDuration = randint(5, 20)
        self.animationPause = randint(60, 300)
        self.inAnimation = False
        self.ticks = 0
        self.rotateToAngle = randint(-15, 15)
        self.deltaRotation = 2*self.rotateToAngle/self.animationDuration

    # rotate the sprite randomly by acting on the sprite argument self.angle
    def stepSelf(self):
        self.ticks += 1
        if not self.inAnimation:
            if self.ticks % self.animationPause == 0:
                self.ticks = 0
                self.inAnimation = True
        else:
            if self.ticks % (self.animationDuration+1) == 0:
                self.angle = 0
                self.ticks = 0
                self.animationDuration = randint(5, 20)
                self.animationPause = randint(60, 300)
                self.inAnimation = False
                self.rotateToAngle = randint(7, 15)
                if randint(0, 1) == 1:
                    self.rotateToAngle = -self.rotateToAngle
                self.deltaRotation = 2*self.rotateToAngle/self.animationDuration
            elif self.ticks % (self.animationDuration//2+1) == 0:
                self.deltaRotation = -self.deltaRotation
                self.angle += self.deltaRotation
            else:
                self.angle += self.deltaRotation


# class for the things player can interact with
class interactable(unplayableSpriteClass):
    # initiate the same argument as the parent class
    def __init__(self, *args, angle=0, opacity=100):
        super().__init__(*args, angle=angle, opacity=opacity)

    # updates the self view arguments of the object depending on the game state
    def stepSelf(self, sceneState=0):
        if sceneState == 4 and self.name == "table1" or sceneState == 5 and self.name == "table2" or sceneState == 6 and self.name == "wallmap":
            self.todraw[1] = 1
            self.x = 0
            self.y = 0
            self.width = 1305
            self.height = 720
        else:
            path = scene1["interactable"][self.name]
            self.x = path["x"]
            self.y = path["y"]
            self.width = path["width"]
            self.height = path["height"]
            self.todraw[1] = 0


# player logic
class player(unplayableSpriteClass):
    # initiate the same argument as the parent class by loading data from json file
    def __init__(self, *args, angle=0, opacity=100, collision=True):
        super().__init__(*args[:-1], angle=angle, opacity=opacity)
        self.movingSpeed = 7
        self.activeCollision = collision
        self.notAllowed = []
        for i in args[-1]:
            data = repr(i)
            data = data.split(";")
            self.notAllowed.append((data[1], (int(data[5]), int(data[6]), int(
                data[5])+int(data[7]), int(data[6])+int(data[8]))))

    # proximity detection to then allow for interactions
    def stepSelf(self):
        self.todraw[1] = (self.todraw[1]+1) % len(self.images[self.todraw[0]])
        if not (self.allowedMovement(0, -self.movingSpeed)[1] and self.allowedMovement(0, self.movingSpeed)[1] and self.allowedMovement(-self.movingSpeed, 0)[1] and self.allowedMovement(self.movingSpeed, 0)[1]):
            self.todraw[1] = 1
        else:
            self.todraw[1] = 0

    # respond to keyHold -> movement
    def selfKeyHold(self, events):
        if ("up" in events or "w" in events) and (not self.activeCollision or self.allowedMovement(0, -self.movingSpeed)[1]):
            self.y -= self.movingSpeed
        if ("down" in events or "s" in events) and (not self.activeCollision or self.allowedMovement(0, self.movingSpeed)[1]):
            self.y += self.movingSpeed
        if ("right" in events or "d" in events) and (not self.activeCollision or self.allowedMovement(self.movingSpeed, 0)[1]):
            self.x += self.movingSpeed
        if ("left" in events or "a" in events) and (not self.activeCollision or self.allowedMovement(-self.movingSpeed, 0)[1]):
            self.x -= self.movingSpeed

    # respond to keyPress -> collision and object examination
    def selfKeyPress(self, event, app):
        if event == "e":
            if self.allowedMovement(0, -self.movingSpeed)[0] in ["table1", "table2", "wallmap"]:
                self.changeGameState((0, -self.movingSpeed), app)
            elif self.allowedMovement(0, self.movingSpeed)[0] in ["table1", "table2", "wallmap"]:
                self.changeGameState((0, self.movingSpeed), app)
            elif self.allowedMovement(-self.movingSpeed, 0)[0] in ["table1", "table2", "wallmap"]:
                self.changeGameState((-self.movingSpeed, 0), app)
            elif self.allowedMovement(self.movingSpeed, 0)[0] in ["table1", "table2", "wallmap"]:
                self.changeGameState((self.movingSpeed, 0), app)
            elif self.allowedMovement(self.movingSpeed, 0)[0] == "car" or self.allowedMovement(self.movingSpeed, 0)[0] == "salem":
                self.changeGameState((self.movingSpeed, 0), app)
            elif self.allowedMovement(0, self.movingSpeed)[0] == "car":
                self.changeGameState((0, self.movingSpeed), app)

    # changes the game state for the story flow
    def changeGameState(self, arg, app):
        if self.allowedMovement(*arg)[0] == "table1":
            app.sceneState = 4
        elif self.allowedMovement(*arg)[0] == "table2":
            app.sceneState = 5
        elif self.allowedMovement(*arg)[0] == "wallmap":
            app.sceneState = 6
        elif (self.allowedMovement(*arg)[0] == "car" or self.allowedMovement(*arg)[0] == "salem") and app.Task[2]:
            app.sceneState = 7

    # returns if player can move and if not returns the colliding sprite
    def allowedMovement(self, offsetx, offsety):
        for i in self.notAllowed:
            j = i[1]
            if self.isPlayerColliding(self.x+offsetx, self.y+offsety, self.x+self.width+offsetx, self.y+self.height+offsety, *j):
                return (i[0], False)
        return ("", True)

    # rectangle to rectangle collision
    def isPlayerColliding(self, left1, top1, right1, bottom1,
                          left2, top2, right2, bottom2):
        if left1 <= 0 or right1 >= 1305 or top1 <= 0 or bottom1 >= 720:
            return True
        if bottom1 >= top2 and bottom2 >= top1 and\
                right1 >= left2 and right2 >= left1:
            return True
        else:
            return False


# dialogue logic
class dialogue(unplayableSpriteClass):
    # initiate the same argument as the parent class
    def __init__(self, *args, angle=0, opacity=100):
        super().__init__(*args, angle=angle, opacity=opacity)

    def drawSelf(self, text):
        # draw a shadow over everything
        drawRect(0, 0, 1305, 720, opacity=70)
        # draws its image
        super().drawSelf()
        if self.todraw[0] == 1:
            if text[0]=='samer':
                self.todraw[1]=2
            # draws text if it has finish animation
            textYPos = 445
            for i in range(7):
                # max line len == 79 characters
                drawLabel(text[1][i], 55, textYPos, size=25,
                          font="monospace", bold=True, align="left-top")
                textYPos += 35

    # updates todraw for animation
    def stepSelf(self):
        self.todraw[1] = (self.todraw[1]+1) % len(self.images[self.todraw[0]])
        if self.todraw[1] == 0:
            self.todraw[0] = 1
#################################################
# helper function
#################################################

#################################################
# Scene function
#################################################

#################################################
# Scene 1
#################################################


def loadScene1(app):
    app.Task = [False]*3
    app.sceneTicks = 0
    app.unplayableSprites = []
    app.text = scene1["texts"]
    print(app.text)
    # appends object of unplayableSpriteClass class and rotatingSpriteClass class to the list app.unplayableSprites
    for key, value in scene1["static"].items():
        app.unplayableSprites.append(unplayableSpriteClass(
            key, value["url"], value["images"], value["toDraw"], value["x"], value["y"], value["width"], value["height"], value["color"]))
    for key, value in scene1["interactable"].items():
        app.unplayableSprites.append(interactable(
            key, value["url"], value["images"], value["toDraw"], value["x"], value["y"], value["width"], value["height"], value["color"]))
    for key, value in scene1["rotating"].items():
        app.unplayableSprites.append(rotatingSpriteClass(
            key, value["url"], value["images"], value["toDraw"], value["x"], value["y"], value["width"], value["height"], value["color"]))


def scene1Step(app):
    # increase debugging ticks by 1 and reflects that in the app window
    app.debuggingTicks += 1
    if app.sceneState == 1:
        app.sceneTicks += 1
        if app.sceneTicks == 60:
            app.sceneState = 2
            app.sceneTicks = 0
    elif app.sceneState == 2:
        app.dialogueBox.stepSelf()
    elif app.sceneState == 3:
        app.dialogueBox.todraw = [0, 0]
        # calls the onStep of every object
        for iSprite in app.unplayableSprites:
            iSprite.stepSelf()
        app.player.stepSelf()
    elif app.sceneState == 4:
        app.unplayableSprites[7].stepSelf(sceneState=app.sceneState)
        app.Task[0] = True
    elif app.sceneState == 5:
        app.unplayableSprites[8].stepSelf(sceneState=app.sceneState)
        app.Task[1] = True
    elif app.sceneState == 6:
        app.unplayableSprites[9].stepSelf(sceneState=app.sceneState)
        if app.Task[0] and app.Task[1]:
            app.Task[2] = True
    else:
        app.dialogueBox.stepSelf()
    # app.shader.stepSelf()


def scene1OnKeyHold(app, events):
    # calls keyHold of the player
    # app.player.selfKeyHold(events)
    if app.sceneState == 3:
        app.player.selfKeyHold(events)


def scene1OnKeyPress(app, event):
    if app.sceneState == 3:
        app.player.selfKeyPress(event, app)
    elif app.sceneState in [4, 5, 6]:
        app.sceneState = 3
    elif app.sceneState == 2 or (app.sceneState > 6 and app.sceneState < 15):
        print(app.sceneState)
        if "enter" == event or "space" == event:
            app.sceneState += 1
    else:
        app.crntScene=1

def scene1Draw(app):
    # calls the draw of every object
    if app.sceneState in [1, 2, 3]:
        for iSprite in app.unplayableSprites:
            iSprite.drawSelf()
        app.player.drawSelf()
    elif app.sceneState == 4:
        app.unplayableSprites[7].drawSelf()
    elif app.sceneState == 5:
        app.unplayableSprites[8].drawSelf()
    elif app.sceneState == 6:
        app.unplayableSprites[9].drawSelf()
    if app.sceneState == 2:
        app.dialogueBox.drawSelf(app.text["1"])
    if app.sceneState > 6:
        for iSprite in app.unplayableSprites:
            iSprite.drawSelf()
        app.player.drawSelf()
        app.dialogueBox.drawSelf(app.text[str(app.sceneState-5)])
    # app.shader.drawSelf()
    # draw the number of frame since the beginining of the game
    drawLabel(str(app.debuggingTicks), 650, 360, fill='red', size=24)
    # shader feature to develop after mvp
    # drawImage("image/salem adventure/assets/from internet/noise shader.gif",0,0,width=app.width,height=app.height,opacity=10)

#################################################
# MVC CS2 mode functionS
#################################################

# user defined in cs2 mode, runs the first time onStep runs to mimic onAppStart of cs3 mode


def onAppStart(app):
    # runs at the start of the scene
    app.stepsPerSeconds = 30
    app.unplayableSprites = []
    app.debuggingTicks = 0
    app.crntScene = 2
    app.sceneState = 1
    loadScene1(app)
    # saves the player object in app.player
    path = game["player"]
    app.player = player(
        "player", path["url"], path["images"], path["toDraw"], path["x"], path["y"], path["width"], path["height"], path["color"], app.unplayableSprites[1:])
    # saves the dialogue object in app.dialogueBox
    path = game["dialogue"]
    app.dialogueBox = dialogue("dialogue", path["url"], path["images"], path["toDraw"],
                               path["x"], path["y"], path["width"], path["height"], path["color"])
    # shader feature to develop after mvp
    path = game["shader"]
    app.shader = unplayableSpriteClass("shader", path["url"], path["images"], path["toDraw"],
                                       path["x"], path["y"], path["width"], path["height"], path["color"], opacity=path["opacity"])
    # print to confirm initiation
    # if everything runned properly this print all the loaded data of the scene
    for iSprite in app.unplayableSprites:
        print(iSprite)
        print(repr(iSprite))
    print(app.player)
    print(repr(app.player))
    print(app.dialogueBox)
    print(repr(app.dialogueBox))
    print(app.shader)
    print(repr(app.shader))


def onStep(app):
    # disallow resizing
    if app.width != 1305 or app.height != 720:
        app.width = 1305
        app.height = 720
    if app.crntScene == 2:
        scene1Step(app)


def onKeyHold(app, events):
    if app.crntScene == 2:
        scene1OnKeyHold(app, events)


def onKeyPress(app, event):
    if app.crntScene == 2:
        scene1OnKeyPress(app, event)


def redrawAll(app):
    if app.crntScene == 2:
        scene1Draw(app)


# load the json dictionnary in the game variable
with open('./gameGlobal.json', 'r') as file:
    game = json.load(file)

# load the json dictionnary in the game variable
with open('./scene1.json', 'r') as file:
    scene1 = json.load(file)
# run app
runApp()
