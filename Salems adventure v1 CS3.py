#################################################
# TERM PROJECT
# Your name: Mohamed Waiel Shikfa
# Your andrew id: mshikfa
#################################################
# import the library
from cmu_graphics import *
import json
from random import randint
from cmu_graphics.shape_logic import loadImageFromStringReference
import os


#################################################
# global classes
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

    # updates the data of the sprite, aka goes to the next frame of the sprite
    def stepSelf(self):
        self.todraw[1] = (self.todraw[1]+1) % len(self.images[self.todraw[0]])

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
        self.animationPause = randint(60, 150)
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
                self.animationPause = randint(60, 150)
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


# global player logic
class player(unplayableSpriteClass):
    # initiate the same argument as the parent class by loading data from json file
    def __init__(self, *args, angle=0, opacity=100, collision=True):
        super().__init__(*args[:-1], angle=angle, opacity=opacity)
        self.movingSpeed = 7
        self.activeCollision = collision
        self.notAllowed = []
        if collision:
            for i in args[-1]:
                data = repr(i)
                data = data.split(";")
                self.notAllowed.append((data[1], (int(data[5]), int(data[6]), int(
                    data[5])+int(data[7]), int(data[6])+int(data[8]))))

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

    # returns if player can move and if not returns the colliding sprite
    def allowedMovement(self, offsetx, offsety):
        for i in self.notAllowed:
            if i[0] != "bg":
                j = i[1]
                if self.isPlayerColliding(self.x+offsetx, self.y+offsety, self.x+self.width+offsetx, self.y+self.height+offsety, *j):
                    return (i[0], False)
        if self.notAllowed == [] and (self.x+offsetx <= 0 or self.x+offsetx+self.width >= 1305 or self.y+offsety <= 0 or self.y+self.height+offsety >= 720):
            return ("", False)
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
    def drawSelf(self, text):
        # draw a shadow over everything
        drawRect(0, 0, 1305, 720, opacity=70)
        # draws its image
        if self.todraw[0] == 1 and text[0] == 'samer':
            if self.todraw[1] != 0:
                self.todraw[1] = 0
            self.todraw[0] = 2
        if self.todraw[0] == 2 and text[0] == 'salem':
            if self.todraw[1] != 0:
                self.todraw[1] = 0
            self.todraw[0] = 1
        super().drawSelf()
        if self.todraw[0] > 0:
            # draws text if it has finish animation
            textYPos = 445
            for i in range(6):
                # max line len == 79 characters
                drawLabel(text[1][i], 55, textYPos, size=25,
                          font="monospace", bold=True, align="left-top")
                textYPos += 35
            drawLabel("SPACE or ENTER to continue ...", 950, textYPos-10, size=15,
                      font="monospace", bold=True, align="left-top")

    # updates todraw for animation
    def stepSelf(self):
        super().stepSelf()
        if self.todraw[1] == 0:
            self.todraw[0] = 1


# button general logic
class button(unplayableSpriteClass):
    def selfMousePress(self, app, x, y):
        if self.x < x < self.x+self.width and self.y < y < self.y+self.height:
            self.answer(app)

    def answer(self, app):
        pass


#################################################
# scene 0 classes
#################################################
# buttons for scene0
class buttonScene0(button):
    def answer(self, app):
        if self.name == "1":
            app.gameState = 1
            cleanAppVariables(app)
        else:
            response = app.getTextInput(
                "Input saved game name (if game name doesn't exist, game will crash and you will have to rerun it).")
            if response in "./saved games":
                with open("./saved games/" + response, "r") as file:
                    app.gameState = int(file.read())
            else:
                print("File Not Found")
            if app.gameState == 1:
                app.previousScene = 1
            else:
                app.previousScene = app.gameState-1
            cleanAppVariables(app)
#################################################
# Scene 0 function
#################################################
def loadScene0(app):
    cleanAppVariables(app)
    # appends object of unplayableSpriteClass class and rotatingSpriteClass class to the list app.unplayableSprites
    appendToUnplayable(app, scene0, "bg")
    appendToButton(app, scene0, "buttons", buttonScene0)


def scene0Step(app):
    # calls the onStep of every object
    for iSprite in app.unplayableSprites:
        iSprite.stepSelf()
    for ibutton in app.buttons:
        ibutton.stepSelf()


def scene0MousePress(app, x, y):
    for ibutton in app.buttons:
        ibutton.selfMousePress(app, x, y)


def scene0Draw(app):
    for iSprite in app.unplayableSprites:
        iSprite.drawSelf()
    for iSprite in app.buttons:
        iSprite.drawSelf()
    drawLabel("Press k at any time to save.", 660, 650, size=25, fill="blue")


#################################################
# Scene 1 classes
#################################################
#################################################
# Scene 1 function
#################################################
def loadScene1(app):
    appendToUnplayable(app, scene1, "loading", unplayableSpriteClass)


def scene1Step(app):
    if app.sceneState == 0:
        loadScene1(app)
        app.sceneState += 1
    if app.sceneState == 1:
        app.sceneTicks += 1
        for iSprite in app.unplayableSprites:
            iSprite.stepSelf()
        if app.sceneTicks == 60:
            app.gameState = app.previousScene + 1
            cleanAppVariables(app)
            print(app.gameState)


def scene1Draw(app):
    drawRect(0, 0, 1305, 720)
    for iSprite in app.unplayableSprites:
        iSprite.drawSelf()


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
        if event == "e":
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
    print(app.text)
    # appends object of unplayableSpriteClass class and rotatingSpriteClass class to the list app.unplayableSprites
    appendToUnplayable(app, scene2, "static")
    appendToUnplayable(app, scene2, "interactable", toClass=scene2Interactable)
    appendToUnplayable(app, scene2, "rotating", toClass=rotatingSpriteClass)
    # saves the player object in app.player
    path = scene2["player"]
    app.player = playerScene2(
        "player", path["url"], path["images"], path["toDraw"], path["x"], path["y"], path["width"], path["height"], path["color"], app.unplayableSprites[1:])
    for iSprite in app.unplayableSprites:
        print(iSprite)
        print(repr(iSprite))


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
    elif app.sceneState == 2 or (app.sceneState > 6 and app.sceneState < 15):
        if "enter" == event or "space" == event:
            app.sceneState += 1
    elif app.sceneState > 6:
        app.gameState = 1
        app.previousScene = 3
        cleanAppVariables(app)


def scene2Draw(app):
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
        self.speed = 1

    def stepSelf(self):
        super().stepSelf()
        if self.speed > 0:
            self.speed = randint(1, 3)
        self.y += self.speed
        self.x += randint(-50, 50)/5
        if self.x > 700:
            self.x = 700
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
    print(app.text)
    # appends object of unplayableSpriteClass class and rotatingSpriteClass class to the list app.unplayableSprites
    appendToUnplayable(app, scene4, "static")
    for i in range(randint(2, 7)):
        appendToUnplayable(app, scene4, "ennemie", toClass=ennemie)
        app.unplayableSprites[-1].x = randint(100, 1200)
    # saves the player object in app.player
    path = scene4["player"]
    app.player = playerScene4(
        "player", path["url"], path["images"], path["toDraw"], path["x"], path["y"], path["width"], path["height"], path["color"], app.unplayableSprites[1:])
    for iSprite in app.unplayableSprites:
        print(iSprite)
        print(repr(iSprite))
    print(app.player)
    print(repr(app.player))


def scene4Step(app):
    if app.sceneState == 0:
        loadScene4(app)
        app.sceneState += 1
    if app.sceneState == 1:
        app.sceneTicks += 1
        if app.sceneTicks == 30:
            app.sceneState = 2
    elif 7 > app.sceneState > 1:
        app.dialogueBox.stepSelf()
    elif app.sceneState == 7:
        print(app.unplayableSprites)
        app.dialogueBox.todraw = [0, 0]
        app.player.stepSelf(app.unplayableSprites)
        for i in range(len(app.unplayableSprites)):
            if app.player.removeEnnemie(i):
                app.unplayableSprites[i].speed = -10
                app.unplayableSprites[i].angle = 180
        if len(app.unplayableSprites) < 7 and app.ennemie > 0:
            for i in range(randint(2, 15)):
                appendToUnplayable(app, scene4, "ennemie", toClass=ennemie)
                app.unplayableSprites[-1].x = randint(100, 1200)
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
        app.dialogueBox.stepSelf()


def scene4OnKeyHold(app, events):
    # calls keyHold of the player
    # app.player.selfKeyHold(events)
    if app.sceneState == 7:
        app.player.selfKeyHold(events)


def scene4OnKeyPress(app, event):
    if 7 > app.sceneState > 1 or 10 > app.sceneState > 7:
        if "enter" == event or "space" == event:
            app.sceneState += 1
    if app.sceneState == 10:
        app.gameState = 1
        app.previousScene = 4
        cleanAppVariables(app)


def scene4Draw(app):
    # calls the draw of every object
    if app.sceneState > 0:
        for iSprite in app.unplayableSprites:
            iSprite.drawSelf()
        app.player.drawSelf()
    if 7 > app.sceneState > 1 or 10 > app.sceneState > 7:
        app.dialogueBox.drawSelf(app.text[str(app.sceneState-1)])


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
    print(app.text)
    # appends object of unplayableSpriteClass class and rotatingSpriteClass class to the list app.unplayableSprites
    appendToUnplayable(app, scene5, "static")
    appendToUnplayable(app, scene5, "interactable", toClass=scene2Interactable)
    appendToUnplayable(app, scene5, "rotating", toClass=rotatingSpriteClass)
    # saves the player object in app.player
    path = scene5["player"]
    app.player = playerScene5(
        "player", path["url"], path["images"], path["toDraw"], path["x"], path["y"], path["width"], path["height"], path["color"], app.unplayableSprites[1:])
    for iSprite in app.unplayableSprites:
        print(iSprite)
        print(repr(iSprite))


def scene5Step(app):
    if app.sceneState == 0:
        loadScene5(app)
        app.sceneState += 1
    else:
        app.dialogueBox.stepSelf()


def scene5OnKeyPress(app, event):
    if app.sceneState > 0 and app.sceneState < 10:
        if "enter" == event or "space" == event:
            app.sceneState += 1
    elif app.sceneState == 10:
        app.gameState = 1
        app.previousScene = 5
        cleanAppVariables(app)


def scene5Draw(app):
    # calls the draw of every object
    if 11 > app.sceneState > 0:
        for iSprite in app.unplayableSprites:
            iSprite.drawSelf()
        app.player.drawSelf()
        app.dialogueBox.drawSelf(app.text[str(app.sceneState)])


#################################################
# Scene 100 classes
#################################################
#################################################
# Scene 100 function
#################################################
def loadScene100(app):
    appendToUnplayable(app, scene100, "gameOver", unplayableSpriteClass)


def scene100Step(app):
    if app.sceneState == 0:
        loadScene100(app)
        app.sceneState += 1
    if app.sceneState == 1:
        app.sceneTicks += 1
        for iSprite in app.unplayableSprites:
            iSprite.stepSelf()


def scene100OnKeyPress(app, event):
    if event == "r":
        app.gameState = app.previousScene + 1
        cleanAppVariables(app)
        print(app.gameState)


def scene100Draw(app):
    drawRect(0, 0, 1305, 720)
    for iSprite in app.unplayableSprites:
        iSprite.drawSelf()
    drawLabel("Press r to try again.", 660, 450, size=25, fill="orange")


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
    app.debuggingTicks = 0


#################################################
# MVC CS3 mode functionS
#################################################
def onAppStart(app):
    # runs at the start of the game
    app.stepsPerSeconds = 30
    app.gameState = 0
    app.previousScene = 1
    cleanAppVariables(app)
    loadScene0(app)
    # saves the dialogue object in app.dialogueBox
    path = game["dialogue"]
    app.dialogueBox = dialogue("dialogue", path["url"], path["images"], path["toDraw"],
                               path["x"], path["y"], path["width"], path["height"], path["color"])
    # shader feature to develop after mvp
    path = game["shader"]
    app.shader = unplayableSpriteClass("shader", path["url"], path["images"], path["toDraw"],
                                       path["x"], path["y"], path["width"], path["height"], path["color"], opacity=path["opacity"])
    path = game["endScreen"]
    app.endScreen = unplayableSpriteClass("endScreen", path["url"], path["images"], path["toDraw"],
                                          path["x"], path["y"], path["width"], path["height"], path["color"], opacity=path["opacity"])
    # print to confirm initiation
    # if everything runned properly this print all the loaded data of the scene
    print(app.dialogueBox)
    print(repr(app.dialogueBox))
    print(app.shader)
    print(repr(app.shader))


def onStep(app):
    # increase debugging ticks by 1 and reflects that in the app window
    app.debuggingTicks += 1
    # disallow resizing
    if app.width != 1305 or app.height != 720:
        app.width = 1305
        app.height = 720
    if app.gameState == 0:
        scene0Step(app)
    elif app.gameState == 1:
        scene1Step(app)
    elif app.gameState == 2:
        scene2Step(app)
    elif app.gameState == 4:
        scene4Step(app)
    elif app.gameState == 5:
        scene5Step(app)
    elif app.gameState == 100:
        scene100Step(app)
    # app.shader.stepSelf()


def onKeyHold(app, events):
    if app.gameState == 2:
        scene2OnKeyHold(app, events)
    elif app.gameState == 4:
        scene4OnKeyHold(app, events)


def onKeyPress(app, event):
    if app.gameState == 2:
        scene2OnKeyPress(app, event)
    elif app.gameState == 4:
        scene4OnKeyPress(app, event)
    elif app.gameState == 5:
        scene5OnKeyPress(app, event)
    elif app.gameState == 100:
        scene100OnKeyPress(app, event)
    elif event == "r":
        app.gameState = 0
        app.previousScene = 1
        cleanAppVariables(app)
        loadScene0(app)
    if event == "k":
        response = app.getTextInput("What would you like to name this save")
        with open("./saved games/" + response + ".txt", "w") as file:
            file.write(str(app.gameState))


def onMousePress(app, x, y):
    if app.gameState == 0:
        scene0MousePress(app, x, y)


def redrawAll(app):
    if app.gameState == 0:
        scene0Draw(app)
    elif app.gameState == 1:
        scene1Draw(app)
    elif app.gameState == 2:
        scene2Draw(app)
    elif app.gameState == 4:
        scene4Draw(app)
    elif app.gameState == 5:
        scene5Draw(app)
    elif app.gameState == 100:
        scene100Draw(app)
    else:
        app.endScreen.drawSelf()


    # app.shader.drawSelf()
    # draw the number of frame since the beginining of the game
    # drawLabel(str(app.debuggingTicks), 650, 360, fill='red', size=24)
    # shader feature to develop after mvp
    # drawImage("image/salem adventure/assets/from internet/noise shader.gif",0,0,width=app.width,height=app.height,opacity=10)


# load the json dictionnary in the game variable
with open('./gameGlobal.json', 'r') as file:
    game = json.load(file)
# load the json dictionnary for scene0
with open('./scene0.json', 'r') as file:
    scene0 = json.load(file)
# load the json dictionnary for scene1
with open('./scene1.json', 'r') as file:
    scene1 = json.load(file)
# load the json dictionnary for scene2
with open('./scene2.json', 'r') as file:
    scene2 = json.load(file)
# load the json dictionnary for scene2
with open('./scene3.json', 'r') as file:
    scene3 = json.load(file)
# load the json dictionnary for scene2
with open('./scene4.json', 'r') as file:
    scene4 = json.load(file)
# load the json dictionnary for scene2
with open('./scene5.json', 'r') as file:
    scene5 = json.load(file)
# load the json dictionnary for scene2
with open('./scene100.json', 'r') as file:
    scene100 = json.load(file)


# run app
runApp(game["global"]["width"], game["global"]["height"])
