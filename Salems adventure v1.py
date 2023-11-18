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

# class for all unplayable sprite
class unplayableSpriteClass():
    # initiate the argument of the sprite by loading data from json file
    id = 0

    def __init__(self, *args, angle=0, opacity=100):
        unplayableSpriteClass.id += 1
        self.id = unplayableSpriteClass.id
        self.name, self.urls, self.images, self.todraw, self.x, self.y, self.width, self.height, self.color = args
        self.angle, self.opacity = angle, opacity
        # uncomment below for rectangle
        # self.view=[]
        # for i,url in enumerate(self.urls):
        #     temp=[]
        #     for image in self.images[i]:
        #         temp.append(Rect(self.x, self.y,
        #          self.width, self.height, rotateAngle=self.angle, fill=self.color, opacity=self.opacity,visible=False))
        #     self.view.append(temp)
        # uncomment below for images
        self.view=[]
        for i,url in enumerate(self.urls):
            temp=[]
            for image in self.images[i]:
                temp.append(Image(url + image, self.x,
                          self.y, width=self.width, height=self.height, rotateAngle=self.angle, opacity=self.opacity,visible=False))
            self.view.append(temp)

    # used to debugg, get info for player and make the class feel more complete
    def __repr__(self):
        return f'{self};{self.urls};{self.images};{self.todraw};{self.x};{self.y};{self.width};{self.height};{self.angle};{self.opacity};{self.color}'

    def __str__(self):
        return f'{self.id};{self.name}'

    # updates the data of the sprite, mainly if it is animated it goes to the next frame
    def stepSelf(self):
        # to fix later
        # if self.name=='salem' and if not self.inanimation:
        #     self.todraw[0]=randint(0, 0)
        self.todraw[1] = (self.todraw[1]+1) % len(self.images[self.todraw[0]])

    # draw the sprite with the argument loaded from the json and updated with the function stepSelf
    def drawSelf(self):
        # trying rectangle to prove cmu graphics is slow with images
        for i in range(len(self.urls)):
            for j in range(len(self.images[i])):
                self.view[i][j].visible=False
        crntView=self.view[self.todraw[0]][self.todraw[1]]
        crntView.left = self.x
        crntView.top = self.y
        crntView.right = self.x+self.width
        crntView.bottom = self.y+self.height
        crntView.rotateAngle = self.angle
        crntView.opacity = self.opacity
        crntView.visible=True
        # comment fill for image or transparency won't be visible
        # crntView.fill = self.color


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
            self.notAllowed.append((int(data[5]), int(data[6]), int(
                data[5])+int(data[7]), int(data[6])+int(data[8])))
    # proximity detection to then allow for interactions

    def stepSelf(self):
        self.todraw[1] = (self.todraw[1]+1) % len(self.images[self.todraw[0]])
        if not (self.allowedMovement(0, -self.movingSpeed) and self.allowedMovement(0, self.movingSpeed) and self.allowedMovement(-self.movingSpeed, 0) and self.allowedMovement(self.movingSpeed, 0)):
            self.color = 'purple'
        else:
            self.color = 'blue'

    # respond to keyHold
    def selfKeyHold(self, events):
        if ("up" in events or "w" in events) and (not self.activeCollision or self.allowedMovement(0, -self.movingSpeed)):
            self.y -= self.movingSpeed
        if ("down" in events or "s" in events) and (not self.activeCollision or self.allowedMovement(0, self.movingSpeed)):
            self.y += self.movingSpeed
        if ("right" in events or "d" in events) and (not self.activeCollision or self.allowedMovement(self.movingSpeed, 0)):
            self.x += self.movingSpeed
        if ("left" in events or "a" in events) and (not self.activeCollision or self.allowedMovement(-self.movingSpeed, 0)):
            self.x -= self.movingSpeed

    def allowedMovement(self, offsetx, offsety):
        for i in self.notAllowed:
            if self.isPlayerColliding(self.x+offsetx, self.y+offsety, self.x+self.width+offsetx, self.y+self.height+offsety, *i):
                return False
        return True

    def isPlayerColliding(self, left1, top1, right1, bottom1,
                          left2, top2, right2, bottom2):
        if left1 <= 0 or right1 >= 1305 or top1 <= 0 or bottom1 >= 720:
            return True
        if bottom1 >= top2 and bottom2 >= top1 and\
                right1 >= left2 and right2 >= left1:
            return True
        else:
            return False

class dialogue(unplayableSpriteClass):
    def __init__(self, *args, angle=0, opacity=100):
        self.shadow=Rect(0,0,1305,720,opacity=70)
        super().__init__(*args, angle=angle, opacity=opacity)
        self.inDialogue=True

    def drawSelf(self):
        if self.inDialogue:
            super().drawSelf()
            self.shadow.visible=True
    
    def stepSelf(self):
        super().stepSelf()
        if self.todraw[1]==0:
            self.todraw[0]=1
            app.stepsPerSecond=30
        else:
            app.stepsPerSecond=10

def loadScene1():
    app.unplayableSprites = []
    # appends object of unplayableSpriteClass class and rotatingSpriteClass class to the list app.unplayableSprites
    for key, value in scene1["static"].items():
        app.unplayableSprites.append(unplayableSpriteClass(
            key, value["url"], value["images"], value["toDraw"], value["x"], value["y"], value["width"], value["height"], value["color"]))
    for key, value in scene1["rotating"].items():
        app.unplayableSprites.append(rotatingSpriteClass(
            key, value["url"], value["images"], value["toDraw"], value["x"], value["y"], value["width"], value["height"], value["color"]))


# Taken and modified from the code of a cmu_graphics sample 
# A helper function for drawing text centered on the screen
def drawText(linesList):
    lineHeight = 35
    # lineY starts out at the center (200) minus half the height of our
    # whole block of text
    lineY = 200 - ((len(linesList) * lineHeight) // 2)
    for line in linesList:
        # Create a label for each line, and move lineY down so the next
        # line is drawn lower
        Label(line, 200, lineY, align='center', size=25)
        lineY += lineHeight


# user defined in cs2 mode, runs the first time onStep runs to mimic onAppStart of cs3 mode
def onAppStart():
    # runs at the start of the scene
    app.stepsPerSeconds = 30
    app.unplayableSprites = []
    app.debuggingTicks = 0
    app.crntScene=1
    loadScene1()
    # saves the player object in app.player
    path = game["player"]
    app.player = player(
        "player", path["url"], path["images"], path["toDraw"], path["x"], path["y"], path["width"], path["height"], path["color"], app.unplayableSprites[1:])
    path2 = game["dialogue"]
    app.dialogueBox=dialogue("dialogue",path2["url"], path2["images"], path2["toDraw"], path2["x"], path2["y"], path2["width"], path2["height"], path2["color"])
    # shader feature to develop after mvp
    path3 = game["shader"]
    app.shader = unplayableSpriteClass("shader", path3["url"], path3["images"], path3["toDraw"], path3["x"], path3["y"], path3["width"], path3["height"],path3["color"],opacity=path3["opacity"])
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

def onStep():
    global firstRun
    # disallow resizing
    if app.width != 1305 or app.height != 720:
        app.width = 1305
        app.height = 720
    # onAppStart
    if firstRun:
        onAppStart()
        firstRun = False
    if app.dialogueBox.inDialogue:
        app.dialogueBox.stepSelf()
    else:
        # calls the onStep of every object
        for iSprite in app.unplayableSprites:
            iSprite.stepSelf()
        app.player.stepSelf()
    app.shader.stepSelf()
    redrawAllCs2()


def redrawAllCs2():
    app.group.clear()
    # calls the draw of every object
    for iSprite in app.unplayableSprites:
        iSprite.drawSelf()
    app.player.drawSelf()
    app.dialogueBox.drawSelf()
    # app.shader.drawSelf()
    # increase debugging ticks by 1 and reflects that in the app window
    app.debuggingTicks += 1
    # draw the number of frame since the beginining of the game
    Label(str(app.debuggingTicks), 650, 360, fill='red', size=24)
    # shader feature to develop after mvp
    # drawImage("image/salem adventure/assets/from internet/noise shader.gif",0,0,width=app.width,height=app.height,opacity=10)


def onKeyHold(events):
    if not app.dialogueBox.inDialogue:
        # calls keyHold of the player
        app.player.selfKeyHold(events)


# load the json dictionnary in the game variable
with open('./gameGlobal.json', 'r') as file:
    game = json.load(file)

# load the json dictionnary in the game variable
with open('./scene1.json', 'r') as file:
    scene1 = json.load(file)

firstRun = True

# run app
cmu_graphics.run()
