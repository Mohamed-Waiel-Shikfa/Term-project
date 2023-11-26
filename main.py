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
import copy
import joystick
import sys
# install: pip install --upgrade arabic-reshaper
import arabic_reshaper
# install: pip install python-bidi
from bidi.algorithm import get_display


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
        self.scale, self. offsetx, self.offsety = 1, 0, 0
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
        drawImage(self.view[self.todraw[0]][self.todraw[1]], self.x*self.scale+self.offsetx, self.y*self.scale+self.offsety, width=self.width*self.scale, height=self.height*self.scale, rotateAngle=self.angle, opacity=self.opacity)


# class for all rotating sprite as rotating in pixel software is really hard
class rotatingSpriteClass(unplayableSpriteClass):
    # initiate the same argument as the parent class plus some more by loading data from json file
    def __init__(self, *args, angle=0, opacity=100):
        super().__init__(*args, angle=angle, opacity=opacity)
        self.animationDuration = randint(5, 20)
        self.animationPause = randint(60, 150)
        self.inAnimation = False
        self.ticks = 0
        self.rotateToAngle = randint(-30, 30)
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
                self.rotateToAngle = randint(15, 30)
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
        if ("up" in events or "w" in events or (1,-1) in events) and (not self.activeCollision or self.allowedMovement(0, -self.movingSpeed)[1]):
            self.y -= self.movingSpeed
        if ("down" in events or "s" in events or (1,1) in events) and (not self.activeCollision or self.allowedMovement(0, self.movingSpeed)[1]):
            self.y += self.movingSpeed
        if ("right" in events or "d" in events or (0,1) in events) and (not self.activeCollision or self.allowedMovement(self.movingSpeed, 0)[1]):
            self.x += self.movingSpeed
        if ("left" in events or "a" in events or (0,-1) in events) and (not self.activeCollision or self.allowedMovement(-self.movingSpeed, 0)[1]):
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
        drawRect(self.offsetx, self.offsety, 1305*self.scale, 720*self.scale, opacity=70)
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
            textYPos = 440
            for i in range(6):
                # max line len == 79 characters
                drawLabel(get_display(arabic_reshaper.reshape(text[1][i])), 55*self.scale+self.offsetx, textYPos*self.scale+self.offsety, size=37.5*self.scale*2/3,
                          font="monospace", bold=True, align="left-top")
                textYPos += 35
            drawLabel("SPACE or ENTER to continue ...", 900*self.scale+self.offsetx, (textYPos-10)*self.scale+self.offsety, size=25*self.scale*2/3,
                      font="monospace", bold=True, align="left-top")

    # updates todraw for animation
    def stepSelf(self):
        super().stepSelf()
        if self.todraw[1] == 0:
            self.todraw[0] = 1


# button general logic
class button(unplayableSpriteClass):
    def selfMousePress(self, app, x, y):
        if self.x*self.scale +self.offsetx< x < (self.x+self.width)*self.scale+self.offsetx and self.y*self.scale + self.offsety< y < (self.y+self.height)*self.scale+self.offsety:
            self.answer(app)
    

    def answer(self, app):
        pass


# digit box
class digitBox(unplayableSpriteClass):
    def __init__(self, *args, angle=0, opacity=100):
        super().__init__(*args, angle=angle, opacity=opacity)
        self.labelText=[""]*4
        self.filled=0
    def drawSelf(self, question, question2, question3):
        super().drawSelf()
        drawLabel(question, 655*self.scale+self.scale,200*self.scale+self.offsety, size=32*self.scale*2/3)
        drawLabel(question2, 655*self.scale+self.scale,230*self.scale+self.offsety, size=32*self.scale*2/3)
        drawLabel(question3, 655*self.scale+self.scale,260*self.scale+self.offsety, size=32*self.scale*2/3)
        for i in range(4):
            drawRect((375+150*i)*self.scale+self.offsetx, 300*self.scale+self.offsety, 110*self.scale, 150*self.scale, fill=None, border="black")
            drawLabel(self.labelText[i], (430+150*i)*self.scale+self.offsetx, 375*self.scale+self.offsety, size = 256*self.scale*2/3)
        drawLabel("On pc just type the number.", 655*self.scale+self.offsetx, 500*self.scale+self.offsety, size=32*self.scale*2/3)
        drawLabel("On arcade press b to increase current digit and a to validate it.", 655*self.scale+self.offsetx, 530*self.scale+self.offsety, size=32*self.scale*2/3)
    def getCrntNumberLen(self):
        nblen=0
        for i in self.labelText:
            if i !="":
                nblen+=1
        return nblen
    def getNumber(self):
        nb=0
        for i in range(4):
            nb+=int(self.labelText[i])*10**(3-i)
        return nb
    def newDigit(self, digit, arcade=False):
        self.labelText[self.filled]=digit
        if not arcade:
            self.filled+=1


#################################################
# scene 0 classes
#################################################
# buttons for scene0
class buttonScene0(button):
    def selfOnJoyPress(self, app, button):
        if self.name == "1" and button == "9":
            self.answer(app)

    
    def answer(self, app):
        if self.name == "1":
            nextScene(app)
            cleanAppVariables(app)
        else:
            response = app.getTextInput(
                "Input saved game name (if game name doesn't exist,nothing will happen).")
            if os.path.isfile("./saved games/" + response + ".txt"):
                with open("./saved games/" + response + ".txt", "r") as file:
                    data=file.read()
                app.crntGameIndex = data.split(";")
                app.crntGameIndex[0]=int(app.crntGameIndex[0])
                app.crntGameIndex[1]=int(app.crntGameIndex[1])-1
                nextScene(app)
                cleanAppVariables(app)
            else:
                print("File Not Found")       
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


def scene0OnJoyPress(app, button, joystick):
    if joystick == 0:
        for ibutton in app.buttons:
            ibutton.selfOnJoyPress(app, button)


def scene0Draw(app):
    for iSprite in app.unplayableSprites:
        iSprite.drawSelf()
    for iSprite in app.buttons:
        iSprite.drawSelf()
    drawLabel("Press k at any time to save. (not supported on arcade machine)", 660*app.scale+app.offsetx, 650*app.scale+app.offsety, size=25*app.scale*2/3, fill="blue")


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
            app.sceneState += 1
    if app.sceneState==15 and "enter" == event or "space" == event:
        if app.digitBox.getCrntNumberLen()==4:
            if app.digitBox.getNumber()>2061:
                app.sceneState+=1
                app.year = app.digitBox.getNumber()
            for i in range(4):
                app.digitBox.labelText[i]=""
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
        app.unplayableSprites[7].drawSelf()
    elif app.sceneState == 5:
        app.unplayableSprites[8].drawSelf()
    elif app.sceneState == 6:
        app.unplayableSprites[9].drawSelf()
    if app.sceneState == 2:
        app.dialogueBox.drawSelf(app.text["1"])
    if app.sceneState==15:
        for iSprite in app.unplayableSprites:
            iSprite.drawSelf()
        app.player.drawSelf()
        app.dialogueBox.drawSelf(app.text[str(app.sceneState-6)])
        app.digitBox.drawSelf("To when do you think Salem and Samer should time travel?","Has to be a year in the futur", "(duh I just said that, pls read the dialogue).")
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


#################################################
# scene 3 classes
#################################################
#################################################
# Scene 3 function
#################################################
def gameDimensions(app):
    # These values are set to the writeup defaults
    rows = 17
    cols = 10
    cellSize = 10*app.scale
    margin = 12*app.scale
    offsetx=590*app.scale+app.offsetx
    offsety=161*app.scale+app.offsety
    return (rows, cols, cellSize, margin, offsetx, offsety)


def loadScene3(app):
    appendToUnplayable(app, scene3,"static")
    loadTetris(app)


def loadTetris(app):
    # initiate the game by creating and assigning all necessary variables

    # Seven "standard" pieces (tetrominoes)
    iPiece = [
        [True, True, True, True]
    ]

    jPiece = [
        [True, False, False],
        [True, True, True]
    ]

    lPiece = [
        [False, False, True],
        [True, True, True]
    ]

    oPiece = [
        [True, True],
        [True, True]
    ]

    sPiece = [
        [False, True, True],
        [True, True, False]
    ]

    tPiece = [
        [False, True, False],
        [True, True, True]
    ]

    zPiece = [
        [True, True, False],
        [False, True, True]
    ]
    app.tetrisPieces = [iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece]
    # colors
    app.tetrisPieceColors = ["red", "yellow",
                             "magenta", "pink", "cyan", "green", "orange"]
    app.emptyColor = 'blue'
    app.color = 'orange'
    # dimension and board
    app.rows, app.cols, app.cellSize, app.margin, app.tetrisOffsetx, app.tetrisOffsety = gameDimensions(app)
    app.board = [[app.emptyColor for _ in range(app.cols)] for _ in
                 range(app.rows)]
    # game states variable
    app.runningBonus = False
    app.isPaused = False
    app.isGameOver = False
    app.score = 0
    # first falling piece of the game needs to be created here
    newFallingPiece(app)


def scene3OnKeyPress(app, event):
    # handles key press events according to game state and game design
    # specification
    if not app.isGameOver:
        if event == 'p':
            app.isPaused = not app.isPaused
        elif not app.isPaused:
            if event == 'space':
                hardDropFallingPiece(app)
            elif event == 'up':
                rotateFallingPiece(app)
            elif event == 'down':
                moveFallingPiece(app, 1, 0)
            elif event == 'right':
                moveFallingPiece(app, 0, 1)
            elif event == 'left':
                moveFallingPiece(app, 0, -1)
            # bonus! :)
            elif event == 'b':
                app.runningBonus = not app.runningBonus
                if app.runningBonus:
                    print(
                        'There are two features that are running in bonus '
                        'mode.')
                    print('These are: ')
                    print(
                        '1 - You can now pause (yes it was recommended to do '
                        'that '
                        'in the instructions but never required, so I count '
                        'it as '
                        'a feature :).')
                    print(
                        "2 - For more challenge, the pieces don't have a fixed "
                        "color anymore, in other word the new falling piece "
                        "will "
                        "have a random color between the 7 defined for tetris "
                        "pieces (see line 52 for code of this feature)")
                    print('(also press b again to exit bonus mode.)')
    # restarts game
    elif event == 'r':
        loadTetris(app)
    if event == "c" and  20-app.sceneTicks//30<=0:
        nextScene(app)
        cleanAppVariables(app)


def scene3OnJoyPress(app, button, joystick):
    if joystick == 0:
        if not app.isGameOver:
            if button == '2':
                hardDropFallingPiece(app)
            elif button == '3':
                rotateFallingPiece(app)
        # restarts game
        elif button == '0':
            loadTetris(app)
        if button == "1" and  20-app.sceneTicks//30<=0:
            nextScene(app)
            cleanAppVariables(app)


def scene3OnDigitalJoyAxis(app, results, joystick):
    if joystick==0:
        if (1,1) in results:
            moveFallingPiece(app, 1, 0)
        elif (0,1) in results:
            moveFallingPiece(app, 0, 1)
        elif (0,-1) in results:
            moveFallingPiece(app, 0, -1)


def scene3Step(app):
    # code executed at every frame

    # if the game is running and the falling piece can't fall anymore calls
    # placeFallingPiece to place it on the board the makes a new piece
    if app.sceneState==0:
        loadScene3(app)
        app.sceneState=1
    else:
        app.sceneTicks+=1
        for isprite in app.unplayableSprites:
            isprite.stepSelf()
        stepTetris(app)


def stepTetris(app):
    if app.sceneTicks%10==0:
        app.rows, app.cols, app.cellSize, app.margin, app.tetrisOffsetx, app.tetrisOffsety = gameDimensions(app)
        if not app.isGameOver and not app.isPaused and not moveFallingPiece(app,
                                                                            1, 0):
            placeFallingPiece(app)
            newFallingPiece(app)
            # ends the game if right after making a new falling piece, it is in
            # an illegal state
            if not fallingPieceIsLegal(app):
                app.isGameOver = True


def scene3Draw(app):
    if app.sceneState!=0:
        for isprite in app.unplayableSprites:
            isprite.drawSelf()
        if app.offsety>0:
            drawRect(0, 0, 1305*app.scale,app.offsety, fill="black")
        drawTetris(app)
        if 20-app.sceneTicks//30>=10:
            drawLabel(f"00:{20-app.sceneTicks//30} seconds left", 650*app.scale+app.offsetx, 100*app.scale+app.offsety, fill='red', size=24*app.scale*2/3)
        elif 20-app.sceneTicks//30>=0:
            drawLabel(f"00:0{20-app.sceneTicks//30} seconds left", 650*app.scale+app.offsetx, 100*app.scale+app.offsety, fill='red', size=24*app.scale*2/3)
        else:
            drawLabel(f"00:00 seconds left", 650*app.scale+app.offsetx, 100*app.scale+app.offsety, fill='red', size=24*app.scale*2/3)


def drawTetris(app):
        drawRect(app.tetrisOffsetx, app.tetrisOffsety, 2*app.margin+app.cols*app.cellSize,2*app.margin+app.rows*app.cellSize, fill='orange')
        # draws the game window

        # draw the different element of the board, which are the board the
        # falling piece and the score
        drawBoard(app)
        drawFallingPiece(app)
        drawScore(app)
        # if the player is dead draws a Game over message
        if app.isGameOver:
            drawRect(app.margin + app.tetrisOffsetx, app.margin + app.cellSize + app.tetrisOffsety,
                    app.cols * app.cellSize, app.cellSize * 2)
            drawLabel("Game Over!", app.cols // 2 * app.cellSize + app.margin + app.tetrisOffsetx,
                    2 * app.cellSize + app.margin + app.tetrisOffsety, fill='yellow', align='center',
                    size=app.cellSize, bold=True)


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
        app.sceneTicks += 1
        if app.sceneTicks == 30:
            app.sceneState = 2
    elif 7 > app.sceneState > 1:
        app.dialogueBox.stepSelf()
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
        nextScene(app)
        cleanAppVariables(app)


def scene4OnJoyPress(app, button, joystick):
    if joystick == 0:
        if 7 > app.sceneState > 1 or 10 > app.sceneState > 7:
            if button=="1":
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
    # appends object of unplayableSpriteClass class and rotatingSpriteClass class to the list app.unplayableSprites
    appendToUnplayable(app, scene5, "static")
    appendToUnplayable(app, scene5, "interactable", scene2Interactable)
    appendToUnplayable(app, scene5, "rotating", rotatingSpriteClass)
    # saves the player object in app.player
    path = scene5["player"]
    app.player = playerScene5(
        "player", path["url"], path["images"], path["toDraw"], path["x"], path["y"], path["width"], path["height"], path["color"], app.unplayableSprites[1:])


def scene5Step(app):
    if app.sceneState == 0:
        loadScene5(app)
        app.sceneState += 1
    if app.sceneState == 1:
        app.sceneTicks += 1
        if app.sceneTicks == 30:
            app.sceneState = 2
    elif app.sceneState >= 2:
        app.dialogueBox.stepSelf()


def scene5OnKeyPress(app, event):
    if app.sceneState > 0 and app.sceneState < 12:
        if "enter" == event or "space" == event:
            app.sceneState += 1
    if app.sceneState == 12:
        nextScene(app)
        cleanAppVariables(app)


def scene5OnJoyPress(app, button, joystick):
    if joystick == 0:
        if app.sceneState > 0 and app.sceneState < 12:
            if button=="1":
                app.sceneState += 1
        if app.sceneState == 12:
            nextScene(app)
            cleanAppVariables(app)


def scene5Draw(app):
    # calls the draw of every object
    if 13 > app.sceneState > 1:
        for iSprite in app.unplayableSprites:
            iSprite.drawSelf()
        app.player.drawSelf()
        app.dialogueBox.drawSelf(app.text[str(app.sceneState-1)])


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
        app.sceneTicks += 1
        if app.sceneTicks == 30:
            app.sceneState = 2
            app.sceneTicks=0
    if app.sceneState == 2:
        app.sceneTicks += 1
        if app.sceneTicks == 30:
            app.sceneState = 3
    if app.sceneState >= 3:
        app.dialogueBox.stepSelf()


def scene6OnKeyPress(app, event):
    if app.sceneState > 2 and app.sceneState < 10:
        if "enter" == event or "space" == event:
            app.sceneState += 1
    if app.sceneState == 10:
        nextScene(app)
        cleanAppVariables(app)


def scene6OnJoyPress(app, button, joystick):
    if joystick == 0:
        if app.sceneState > 2 and app.sceneState < 10:
            if button == "1":
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


#################################################
# scene 7 classes
#################################################
class playerScene7(player):
    def stepSelf(self):
        super().stepSelf()
        if not (self.allowedMovement(0, -self.movingSpeed)[1] and self.allowedMovement(0, self.movingSpeed)[1] and self.allowedMovement(-self.movingSpeed, 0)[1] and self.allowedMovement(self.movingSpeed, 0)[1]):
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
        app.sceneTicks += 1
        if app.sceneTicks == 30:
            app.sceneState = 3
    if app.sceneState >= 3:
        app.dialogueBox.stepSelf()
    if app.sceneState == 7:
        if app.player.stepSelf():
            app.sceneState=8


def scene7OnKeyPress(app, event):
    if 7 > app.sceneState > 2 or 15 > app.sceneState > 8:
        if "enter" == event or "space" == event:
            app.sceneState += 1
    if app.sceneState==8 and "enter" == event or "space" == event:
        if app.digitBox.getCrntNumberLen()==4:
            if app.digitBox.getNumber()==1729:
                app.sceneState+=1
            else:
                for i in range(4):
                    app.digitBox.labelText[i]=""
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
        elif app.sceneState==15 and button=="0":
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
        app.digitBox.drawSelf("What is the smallest number that can be written", "as the sum of two cubes in two different way", "")
    if 7 > app.sceneState > 2:
        app.dialogueBox.drawSelf(app.text[str(app.sceneState-2)])
    if app.sceneState == 9:
        app.dialogueBox.drawSelf(app.text["5"])


#################################################
# scene 8 classes
#################################################
class playerScene8(player):
    def stepSelf(self):
        super().stepSelf()
        if not (self.allowedMovement(0, -self.movingSpeed)[1] and self.allowedMovement(0, self.movingSpeed)[1] and self.allowedMovement(-self.movingSpeed, 0)[1] and self.allowedMovement(self.movingSpeed, 0)[1]):
            return True
        return False
#################################################
# Scene 8 function
#################################################
def loadScene8(app):
    app.text = scene8["texts"]
    # appends object of unplayableSpriteClass class and rotatingSpriteClass class to the list app.unplayableSprites
    appendToUnplayable(app, scene8, "static")
    path = scene8["player"]
    app.player = playerScene8(
        "player", path["url"], path["images"], path["toDraw"], path["x"], path["y"], path["width"], path["height"], path["color"], app.unplayableSprites[1:])


def scene8Step(app):
    if app.sceneState == 0:
        loadScene8(app)
        app.sceneState += 1
    if app.sceneState == 1:
        app.sceneTicks += 1
        if app.sceneTicks == 30:
            app.sceneState = 2
            app.sceneTicks=0
    if app.sceneState == 2:
        app.sceneTicks += 1
        if app.sceneTicks == 30:
            app.sceneState = 3
    if 5 > app.sceneState > 2 or 7 > app.sceneState > 5:
        app.dialogueBox.stepSelf()
    if app.sceneState == 5:
        if app.player.x>1200:
            app.sceneState+=1
        if app.player.stepSelf():
            app.gameState = 100
            cleanAppVariables(app)


def scene8OnKeyHold(app, events):
    # calls keyHold of the player
    # app.player.selfKeyHold(events)
    if app.sceneState == 5:
        app.player.selfKeyHold(events)


def scene8OnKeyPress(app, event):
    if  5> app.sceneState > 2 or 7 > app.sceneState > 5:
        if "enter" == event or "space" == event:
            app.sceneState += 1
    if app.sceneState == 7:
        nextScene(app)
        cleanAppVariables(app)


def scene8OnJoyPress(app, button, joystick):
    if joystick == 0:
        if  5> app.sceneState > 2 or 7 > app.sceneState > 5:
            if button == "1":
                app.sceneState += 1
        if app.sceneState == 7:
            nextScene(app)
            cleanAppVariables(app)


def scene8OnDigitalJoyAxis(app, results, joystick):
    if joystick==0:
        if app.sceneState == 5:
            app.player.selfKeyHold(results)


def scene8Draw(app):
    if app.sceneState>=1:
        for iSprite in app.unplayableSprites:
            iSprite.drawSelf()
    if app.sceneState>=2:
        app.player.drawSelf()
    if 5 > app.sceneState > 2:
        app.dialogueBox.drawSelf(app.text[str(app.sceneState-2)])
    if 7 > app.sceneState > 5:
        app.dialogueBox.drawSelf(app.text[str(app.sceneState-3)])


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
    elif app.sceneState==5 and event.isdigit():
        if app.digitBox.getCrntNumberLen()!=4:
            app.digitBox.newDigit(event)


def scene9OnJoyPress(app, button, joystick):
    if joystick == 0:
        if 5> app.sceneState > 2 or app.sceneState > 5:
            if button=="1":
                app.sceneState += 1
        if app.sceneState == 7:
            if app.year<1850:
                app.crntGameIndex[0]=2
                app.crntGameIndex[1]=-1
            nextScene(app)
            cleanAppVariables(app)
        if app.sceneState==5 and button=="1":
            if app.digitBox.getCrntNumberLen()==4:
                if app.digitBox.getNumber()==1950:
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


#################################################
# scene 10 classes
#################################################
#################################################
# Scene 10 function
#################################################
def loadScene10(app):
    app.text = scene10["texts"]
    # appends object of unplayableSpriteClass class and rotatingSpriteClass class to the list app.unplayableSprites
    appendToUnplayable(app, scene10, "static")


def scene10Step(app):
    if app.sceneState == 0:
        loadScene10(app)
        app.sceneState += 1
    if app.sceneState == 1:
        app.sceneTicks += 1
        if app.sceneTicks == 30:
            app.sceneState = 2
            app.sceneTicks=0
    if app.sceneState == 2:
        app.sceneTicks += 1
        if app.sceneTicks == 30:
            app.sceneState = 3
    elif app.sceneState >= 3:
        app.dialogueBox.stepSelf()


def scene10OnKeyPress(app, event):
    if app.sceneState >= 3 and app.sceneState < 9:
        if "enter" == event or "space" == event:
            app.sceneState += 1
    if app.sceneState == 9:
        nextScene(app)
        cleanAppVariables(app)


def scene10OnJoyPress(app, button, joystick):
    if joystick == 0:
        if app.sceneState >= 3 and app.sceneState < 9:
            if button == "1":
                app.sceneState += 1
        if app.sceneState == 9:
            nextScene(app)
            cleanAppVariables(app)


def scene10Draw(app):
    if app.sceneState==1:
        for iSprite in app.unplayableSprites[:-1]:
            iSprite.drawSelf()
    if app.sceneState>=2:
        for iSprite in app.unplayableSprites:
            iSprite.drawSelf()
    if 9 > app.sceneState > 2:
        app.dialogueBox.drawSelf(app.text[str(app.sceneState-2)])


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
        app.sceneTicks += 1
        if app.sceneTicks == 30:
            app.sceneState = 2
            app.sceneTicks=0
    if app.sceneState == 2:
        app.sceneTicks += 1
        if app.sceneTicks == 30:
            app.sceneState = 3
    elif app.sceneState >= 3:
        app.dialogueBox.stepSelf()


def scene11OnKeyPress(app, event):
    if app.sceneState >= 3 and app.sceneState < 9:
        if "enter" == event or "space" == event:
            app.sceneState += 1
    if app.sceneState == 9:
        nextScene(app)
        cleanAppVariables(app)


def scene11OnJoyPress(app, button, joystick):
    if joystick == 0:
        if app.sceneState >= 3 and app.sceneState < 9:
            if button == "1":
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


#################################################
# Scene 100 classes
#################################################
#################################################
# Scene 100 function
#################################################
def loadScene100(app):
    appendToUnplayable(app, scene100, "gameOver")


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
        if app.crntGameIndex[0]==1:
            app.crntGameIndex[0]=0
            app.crntGameIndex[1]=2
        elif app.crntGameIndex[0]==2:
            app.crntGameIndex[0]=0
            app.crntGameIndex[1]=11
        app.gameState = app.storyFlow[app.crntGameIndex[0]][app.crntGameIndex[1]]
        cleanAppVariables(app)


def scene100OnJoyPress(app, button, joystick):
    if joystick == 0:
        if button == "1":
            if app.crntGameIndex[0]==1:
                app.crntGameIndex[0]=0
                app.crntGameIndex[1]=2
            elif app.crntGameIndex[0]==2:
                app.crntGameIndex[0]=0
                app.crntGameIndex[1]=11
            app.gameState = app.storyFlow[app.crntGameIndex[0]][app.crntGameIndex[1]]
            cleanAppVariables(app)


def scene100Draw(app):
    for iSprite in app.unplayableSprites:
        iSprite.drawSelf()
    drawLabel("Press r to try again.", 660*app.scale+app.offsetx, 450*app.scale+app.offsety, size=37.5*app.scale*2/3, fill="orange")


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


#################################################
# Tetris tutorial's functions in order
#################################################
def drawBoard(app):
    # draw the board by going through every row and every cell in that row
    # and drawing that cell

    for irow in range(app.rows):
        for jcol in range(app.cols):
            drawCell(app, irow, jcol)


def drawCell(app, row, col, color=None):
    # draws cells which are squares on the game window

    # if it is a board cell, the position arguments are the final coordinates
    finalcol = col * app.cellSize + app.margin + app.tetrisOffsetx
    finalrow = row * app.cellSize + app.margin + app.tetrisOffsety
    if color is None:
        color = app.board[row][col]
    # if it is not a board cell then we need to add the relative position of
    # the piece to the final coordinates
    else:
        finalcol += app.fallingPieceCol * app.cellSize
        finalrow += app.fallingPieceRow * app.cellSize
    drawRect(finalcol, finalrow, app.cellSize,
             app.cellSize, fill=color, border='black')


def newFallingPiece(app):
    # generate a new falling piece

    # selects a random piece and store calculated useful attribute of this
    # piece in the app (module)
    import random
    randomIndex = random.randint(0, len(app.tetrisPieces) - 1)
    app.fallingPiece = copy.deepcopy(app.tetrisPieces[randomIndex])
    # if in bonus mode the color of the piece will be a randomised color from
    # tetrisPieceColors, which make the game more challenging
    if app.runningBonus:
        randomIndex = random.randint(0, len(app.tetrisPieces) - 1)
    app.fallingPieceColor = app.tetrisPieceColors[randomIndex]
    app.numFallingPieceCols = len(app.fallingPiece[0])
    app.numFallingPieceRows = len(app.fallingPiece)
    app.fallingPieceRow = 0
    app.fallingPieceCol = app.cols // 2 - app.numFallingPieceCols // 2


def drawFallingPiece(app):
    # draws falling piece in the same way the board is drawn

    for irow in range(app.numFallingPieceRows):
        for jcol in range(app.numFallingPieceCols):
            if app.fallingPiece[irow][jcol]:
                drawCell(app, irow, jcol, app.fallingPieceColor)


def moveFallingPiece(app, drow, dcol):
    # move the falling piece only if the move is legal in 3 steps

    # move the falling piece by changing its coordinate
    app.fallingPieceCol += dcol
    app.fallingPieceRow += drow
    # check if the new coordinate result in a legal state
    if not fallingPieceIsLegal(app):
        # if not undo the change to the coordinates
        app.fallingPieceCol -= dcol
        app.fallingPieceRow -= drow
        return False
    return True


def fallingPieceIsLegal(app):
    # checks if the falling piece is in a legal state

    # To return true and validate the piece state, it confirms that:
    # (1) the cell is in fact on the board
    # (2) the color at that location on the board is the emptyColor
    # Otherwise it immediately returns False
    for cellRow in range(len(app.fallingPiece)):
        pieceRow = app.fallingPiece[cellRow]
        for cellCol in range(len(pieceRow)):
            cell = pieceRow[cellCol]
            if cell:
                if app.fallingPieceCol < 0 or app.fallingPieceCol + \
                        app.numFallingPieceCols > app.cols or \
                        app.fallingPieceRow + app.numFallingPieceRows > \
                        app.rows or app.fallingPieceRow < 0:
                    return False
                for boardCol in range(app.cols):
                    for boardRow in range(app.rows):
                        if app.board[boardRow][
                            boardCol] != app.emptyColor and boardCol == \
                                app.fallingPieceCol + cellCol and boardRow == \
                                app.fallingPieceRow + cellRow:
                            return False
    return True


def rotateFallingPiece(app):
    # rotate the falling piece only if the move is legal in 5 steps

    # 1. Store the relevant values associated with the old piece
    tempNumFallingPieceCols = app.numFallingPieceCols
    tempNumFallingPieceRows = app.numFallingPieceRows
    tempfallingPieceCol = app.fallingPieceCol
    tempFallingPieceRow = app.fallingPieceRow
    tempFallingPiece = copy.deepcopy(app.fallingPiece)
    # 2. Compute the relevant values according to the old dimensions.
    app.numFallingPieceCols = tempNumFallingPieceRows
    app.numFallingPieceRows = tempNumFallingPieceCols
    app.fallingPieceCol = tempfallingPieceCol + tempNumFallingPieceCols // 2 \
                          - app.numFallingPieceCols // 2
    app.fallingPieceRow = tempFallingPieceRow + tempNumFallingPieceRows // 2 \
                          - app.numFallingPieceRows // 2
    # 3. Assigns fallingPiece to a 2D list, based on the new dimensions, filled
    # with None values.
    app.fallingPiece = [[None for _ in range(app.numFallingPieceCols)] for _ in
                        range(app.numFallingPieceRows)]
    # 4. Iterate through each of the cells in the original piece, and move
    # each value to its new location in the new piece.

    for cellRow in range(len(tempFallingPiece)):
        pieceRow = tempFallingPiece[cellRow]
        for cellCol in range(len(pieceRow)):
            cell = pieceRow[cellCol]
            app.fallingPiece[app.numFallingPieceRows - cellCol - 1][cellRow] \
                = cell
    # 5. Check whether the new piece is legal. If it isn't, restore the all
    # of the values based on the temporary variables created in Step 1.
    if not fallingPieceIsLegal(app):
        app.fallingPiece = copy.deepcopy(tempFallingPiece)
        app.numFallingPieceCols = tempNumFallingPieceCols
        app.numFallingPieceRows = tempNumFallingPieceRows
        app.fallingPieceRow = tempFallingPieceRow
        app.fallingPieceCol = tempfallingPieceCol


def placeFallingPiece(app):
    # places the falling piece on the bard

    # iterates through each cell of the piece
    for irow in range(app.numFallingPieceRows):
        for jcol in range(app.numFallingPieceCols):
            # if the cell is a colored one, change the color of the board at
            # the coordinates of that cell to the color of the piece
            if app.fallingPiece[irow][jcol]:
                finalrow = irow + app.fallingPieceRow
                finalcol = jcol + app.fallingPieceCol
                app.board[finalrow][finalcol] = app.fallingPieceColor
    # after the piece has been placed, it is necessary to remove any full rows
    removeFullRows(app)


def removeFullRows(app):
    # removes full rows from the board

    # we first count how many full row there is as it is needed later
    fullRows = 0
    for irow in range(app.rows):
        if not app.emptyColor in app.board[irow]:
            fullRows += 1
    # we make a new board by replacing full rows by an empty list
    noFullRowBoard = [[color for color in copy.copy(app.board[irow])
                       if app.emptyColor in app.board[irow]] for irow in
                      range(app.rows)]
    # remove all the empty lists from our new board effectively deleting the
    # full rows
    i = 0
    while i < len(noFullRowBoard):
        if noFullRowBoard[i] == []:
            noFullRowBoard.pop(i)
        else:
            i += 1
    # replace the previous board with full rows number of empty rows (so at
    # the top of our new board), and below that, the rest of the board that was
    # not empty
    app.board = [[app.emptyColor for _ in range(
        app.cols)] for _ in range(fullRows)] + copy.deepcopy(noFullRowBoard)
    # updates the score by adding the square of the number of rows removed
    app.score += fullRows ** 2


def drawScore(app):
    # displays the score on the top of the game window

    drawLabel("Score: " + str(app.score),
              app.cols // 2 * app.cellSize + app.margin + app.tetrisOffsetx,
              app.margin // 2 + app.tetrisOffsety, fill='blue', align='center',
              size=app.cellSize // 1.2, bold=True)


def hardDropFallingPiece(app):
    # hard drops the piece by moving it down until it can't be moved any further

    while moveFallingPiece(app, 1, 0):
        moveFallingPiece(app, 1, 0)


#################################################
# MVC CS3 mode functionS
#################################################
def onAppStart(app):
    # runs at the start of the game
    app.stepsPerSeconds = 30
    app.background="black"
    app.scale=1
    app.offsetx=0
    app.offsety=0
    app.year = 2061
    app.gameState = 0
    app.crntGameIndex = [0, 0]
    app.storyFlow=game["gameState"]
    app.gameState = 0
    # saves the dialogue object in app.dialogueBox
    path = game["dialogue"]
    app.dialogueBox = dialogue("dialogue", path["url"], path["images"], path["toDraw"],
                               path["x"], path["y"], path["width"], path["height"], path["color"])
    # saves the dialogue object in app.dialogueBox
    path = game["digitBox"]
    app.digitBox = digitBox("digitBox", path["url"], path["images"], path["toDraw"],
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
    cleanAppVariables(app)
    loadScene0(app)


def onStep(app):
    # increase debugging ticks by 1 and reflects that in the app window
    app.debuggingTicks += 1
    # rescale everything based on window size
    rescaleAll(app)
    #step scene
    if app.gameState == 0:
        scene0Step(app)
    elif app.gameState == 1:
        scene1Step(app)
    elif app.gameState == 2:
        scene2Step(app)
    elif app.gameState == 3:
        scene3Step(app)
    elif app.gameState == 4:
        scene4Step(app)
    elif app.gameState == 5:
        scene5Step(app)
    elif app.gameState == 6:
        scene6Step(app)
    elif app.gameState == 7:
        scene7Step(app)
    elif app.gameState == 8:
        scene8Step(app)
    elif app.gameState == 9:
        scene9Step(app)
    elif app.gameState == 10:
        scene10Step(app)
    elif app.gameState == 11:
        scene11Step(app)
    elif app.gameState == 100:
        scene100Step(app)
    app.shader.stepSelf()


def onKeyHold(app, events):
    if app.gameState == 2:
        scene2OnKeyHold(app, events)
    elif app.gameState == 4:
        scene4OnKeyHold(app, events)
    elif app.gameState == 7:
        scene7OnKeyHold(app, events)
    elif app.gameState == 8:
        scene8OnKeyHold(app, events)


def onKeyPress(app, event):
    if app.gameState == 2:
        scene2OnKeyPress(app, event)
    elif app.gameState == 3:
        scene3OnKeyPress(app, event)
    elif app.gameState == 4:
        scene4OnKeyPress(app, event)
    elif app.gameState == 5:
        scene5OnKeyPress(app, event)
    elif app.gameState == 6:
        scene6OnKeyPress(app, event)
    elif app.gameState == 7:
        scene7OnKeyPress(app, event)
    elif app.gameState == 8:
        scene8OnKeyPress(app, event)
    elif app.gameState == 9:
        scene9OnKeyPress(app, event)
    elif app.gameState == 10:
        scene10OnKeyPress(app, event)
    elif app.gameState == 11:
        scene11OnKeyPress(app, event)
    elif app.gameState == 100:
        scene100OnKeyPress(app, event)
    elif event == "r":
        app.crntGameIndex = [0,-1]
        nextScene(app)
        cleanAppVariables(app)
        loadScene0(app)
    if event == "k" and app.gameState!=0:
        response = app.getTextInput("What would you like to name this save")
        with open("./saved games/" + response + ".txt", "w") as file:
            file.write(str(app.crntGameIndex[0])+";"+str(app.crntGameIndex[1]))


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
    elif app.gameState == 3:
        scene3Draw(app)
    elif app.gameState == 4:
        scene4Draw(app)
    elif app.gameState == 5:
        scene5Draw(app)
    elif app.gameState == 6:
        scene6Draw(app)
    elif app.gameState == 7:
        scene7Draw(app)
    elif app.gameState == 8:
        scene8Draw(app)
    elif app.gameState == 9:
        scene9Draw(app)
    elif app.gameState == 10:
        scene10Draw(app)
    elif app.gameState == 11:
        scene11Draw(app)
    elif app.gameState == 100:
        scene100Draw(app)
    else:
        app.endScreen.drawSelf()
    # drawLine(app.width/2,0, app.width/2, app.height, fill='green')
    # drawLine(0, app.height/2, app.width,app.height/2, fill='green')

    # shader feature to develop after mvp
    app.shader.drawSelf()
    # draw the number of frame since the beginining of the game
    # drawLabel(str(app.debuggingTicks), 650, 360, fill='red', size=24)


def onJoyPress(app, button, joystick):
    if app.gameState == 0:
        scene0OnJoyPress(app, button, joystick)
    elif app.gameState == 2:
        scene2OnJoyPress(app, button, joystick)
    elif app.gameState == 3:
        scene3OnJoyPress(app, button, joystick)
    elif app.gameState == 4:
        scene4OnJoyPress(app, button, joystick)
    elif app.gameState == 5:
        scene5OnJoyPress(app, button, joystick)
    elif app.gameState == 6:
        scene6OnJoyPress(app, button, joystick)
    elif app.gameState == 7:
        scene7OnJoyPress(app, button, joystick)
    elif app.gameState == 8:
        scene8OnJoyPress(app, button, joystick)
    elif app.gameState == 9:
        scene9OnJoyPress(app, button, joystick)
    elif app.gameState == 10:
        scene10OnJoyPress(app, button, joystick)
    elif app.gameState == 11:
        scene11OnJoyPress(app, button, joystick)
    elif app.gameState == 100:
        scene100OnJoyPress(app, button, joystick)
     # Make sure we can exit by pressing the "P1" button
    if button == '5':
        sys.exit(0)


def onDigitalJoyAxis(app, results, joystick):
    if app.gameState == 2:
        scene2OnDigitalJoyAxis(app, results, joystick)
    elif app.gameState == 3:
        scene3OnDigitalJoyAxis(app, results, joystick)
    elif app.gameState == 4:
        scene4OnDigitalJoyAxis(app, results, joystick)
    elif app.gameState == 7:
        scene7OnDigitalJoyAxis(app, results, joystick)
    elif app.gameState == 8:
        scene8OnDigitalJoyAxis(app, results, joystick)


# load the json dictionnary in the game variable
with open('./gameGlobal.json', 'r') as file:
    game = json.load(file)
allData=[]
for i in range(12):
    with open(f'./scene{i}.json', 'r', encoding="utf8") as file:
        allData.append(json.load(file))
scene0, scene1, scene2, scene3, scene4, scene5, scene6, scene7, scene8, scene9, scene10, scene11= allData 
with open('./scene100.json', 'r') as file:
    scene100 = json.load(file)


# run app
runApp(game["global"]["width"], game["global"]["height"])
