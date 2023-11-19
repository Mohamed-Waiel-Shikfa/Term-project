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
        pass
        # to fix later
        # if self.name=='salem' and if not self.inanimation:
        #     self.todraw[0]=randint(0, 0)
        # self.todraw[1] = (self.todraw[1]+1) % len(self.images[self.todraw[0]])

    # draw the sprite with the argument loaded from the json and updated with the function stepSelf
    def drawSelf(self):
        # trying rectangle to prove cmu graphics is slow with images
        for i in range(len(self.urls)):
            for j in range(len(self.images[i])):
                self.view[i][j].visible=False
        crntView=self.view[self.todraw[0]][self.todraw[1]]
        crntView.left = self.x
        crntView.top = self.y
        crntView.width = self.width
        crntView.height = self.height
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

class interactable(unplayableSpriteClass):
    def __init__(self, *args, angle=0, opacity=100):
        super().__init__(*args, angle=angle, opacity=opacity)
    
    def stepSelf(self):
        if app.sceneState==4 and self.name=="table1" or app.sceneState==5 and self.name=="table2" or app.sceneState==6 and self.name=="wallmap":
            self.todraw[1]=1
            crntView=self.view[self.todraw[0]][self.todraw[1]]
            crntView.left = 0
            crntView.top = 0
            crntView.width = 1305
            crntView.height = 720
            crntView.visible=True
        else:
            self.todraw[1]=0

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
            self.notAllowed.append((data[1],(int(data[5]), int(data[6]), int(
                data[5])+int(data[7]), int(data[6])+int(data[8]))))
    # proximity detection to then allow for interactions

    def stepSelf(self):
        self.todraw[1] = (self.todraw[1]+1) % len(self.images[self.todraw[0]])
        if not (self.allowedMovement(0, -self.movingSpeed)[1] and self.allowedMovement(0, self.movingSpeed)[1] and self.allowedMovement(-self.movingSpeed, 0)[1] and self.allowedMovement(self.movingSpeed, 0)[1]):
            self.todraw[1] = 1
        else:
            self.todraw[1] = 0

    # respond to keyHold
    def selfKeyHold(self, events):
        if ("up" in events or "w" in events) and (not self.activeCollision or self.allowedMovement(0, -self.movingSpeed)[1]):
            self.y -= self.movingSpeed
        if ("down" in events or "s" in events) and (not self.activeCollision or self.allowedMovement(0, self.movingSpeed)[1]):
            self.y += self.movingSpeed
        if ("right" in events or "d" in events) and (not self.activeCollision or self.allowedMovement(self.movingSpeed, 0)[1]):
            self.x += self.movingSpeed
        if ("left" in events or "a" in events) and (not self.activeCollision or self.allowedMovement(-self.movingSpeed, 0)[1]):
            self.x -= self.movingSpeed
    def selfKeyPress(self, event):
        if event == "e":
            if self.allowedMovement(0, -self.movingSpeed)[0] in ["table1","table2","wallmap"]:
                self.changeGameState((0, -self.movingSpeed))
            elif self.allowedMovement(0, self.movingSpeed)[0] in ["table1","table2","wallmap"]:
                self.changeGameState((0, self.movingSpeed))
            elif self.allowedMovement(-self.movingSpeed,0)[0] in ["table1","table2","wallmap"]:
                self.changeGameState((-self.movingSpeed,0))
            elif self.allowedMovement(self.movingSpeed,0)[0] in ["table1","table2","wallmap"]:
                self.changeGameState((self.movingSpeed,0))
            else:
                print("there is nothing to examine here")

    def changeGameState(self, arg):
        if self.allowedMovement(*arg)[0] == "table1":
            app.sceneState=4
        if self.allowedMovement(*arg)[0] == "table2":
            app.sceneState=5
        if self.allowedMovement(*arg)[0] == "wallmap":
            app.sceneState=6
        
    def allowedMovement(self, offsetx, offsety):
        for i in self.notAllowed:
            j=i[1]
            if self.isPlayerColliding(self.x+offsetx, self.y+offsety, self.x+self.width+offsetx, self.y+self.height+offsety, *j):
                return (i[0],False)
        return ("",True)

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
        self.text=[]
        lineY = 445
        for i in range(7):
            # Create a label for each line, and move lineY down so the next
            # line is drawn lower
            self.text.append(Label("", 0, lineY, size=25,font="monospace", bold=True))
            lineY += 35

    def drawSelf(self,text):
        super().drawSelf()
        self.shadow.visible=True
        if self.todraw[0]==1:
            for i in range(7):
                self.text[i].left=60
                self.text[i].visible=True
                self.text[i].value=text[i+1][0]

    def stepSelf(self):
        self.todraw[1] = (self.todraw[1]+1) % len(self.images[self.todraw[0]])

        if self.todraw[1]==0:
            self.todraw[0]=1
#################################################
# helper function
#################################################

def loadScene1():
    app.Task=[False]*3
    app.sceneTicks=0
    app.unplayableSprites = []
    app.text=scene1["texts"]
    # appends object of unplayableSpriteClass class and rotatingSpriteClass class to the list app.unplayableSprites
    for key, value in scene1["static"].items():
        app.unplayableSprites.append(unplayableSpriteClass(
            key, value["url"], value["images"], value["toDraw"], value["x"], value["y"], value["width"], value["height"], value["color"]))
    path=scene1["table1"]
    app.unplayableSprites.append(interactable("table1", path["url"], path["images"], path["toDraw"], path["x"], path["y"], path["width"], path["height"],path["color"]))
    path=scene1["table2"]
    app.unplayableSprites.append(interactable("table2", path["url"], path["images"], path["toDraw"], path["x"], path["y"], path["width"], path["height"],path["color"]))
    path=scene1["wallmap"]
    app.unplayableSprites.append(interactable("wallmap", path["url"], path["images"], path["toDraw"], path["x"], path["y"], path["width"], path["height"],path["color"]))
    for key, value in scene1["rotating"].items():
        app.unplayableSprites.append(rotatingSpriteClass(
            key, value["url"], value["images"], value["toDraw"], value["x"], value["y"], value["width"], value["height"], value["color"]))
def scene1Step():
    if app.sceneState==1:
        app.sceneTicks+=1
        drawScene1()
        if app.sceneTicks==60:
            app.sceneState=2
            app.sceneTicks=0    
    elif app.sceneState==2:
        drawScene1()
        app.dialogueBox.stepSelf()
        app.dialogueBox.drawSelf(app.text["1"])
    elif app.sceneState==3:
        app.dialogueBox.todraw=[0,0]
        # calls the onStep of every object
        for iSprite in app.unplayableSprites:
            iSprite.stepSelf()
        app.player.stepSelf()
        drawScene1()
    elif app.sceneState==4:
        app.unplayableSprites[7].stepSelf()
        app.Task[0]=True
    elif app.sceneState==5:
        app.unplayableSprites[8].stepSelf()
        app.Task[1]=True
    elif app.sceneState==6:
        app.unplayableSprites[9].stepSelf()
        if app.Task[0] and app.Task[1]:
            app.Task[2]=True
    elif app.sceneState==7:
        print(app.Task)
    # app.shader.stepSelf()

def scene1OnKeyHold(events):
    # calls keyHold of the player
    # app.player.selfKeyHold(events)
    if app.sceneState==2:
        if "enter" in events or "space" in events:
            app.sceneState=3
    if app.sceneState==3:
        app.player.selfKeyHold(events)

def scene1OnKeyPress(event):
    if app.sceneState==3:
        app.player.selfKeyPress(event)
    elif app.sceneState==4 or app.sceneState==5:
        app.sceneState=3
    elif app.sceneState==6 and app.Task[2]:
        app.sceneState=7
    elif app.sceneState==6:
        app.sceneState=3

def drawScene1():
    # calls the draw of every object
    for iSprite in app.unplayableSprites:
        iSprite.drawSelf()
    app.player.drawSelf()
    # app.shader.drawSelf()
    # increase debugging ticks by 1 and reflects that in the app window
    app.debuggingTicks += 1
    # draw the number of frame since the beginining of the game
    Label(str(app.debuggingTicks), 650, 360, fill='red', size=24)
    # shader feature to develop after mvp
    # drawImage("image/salem adventure/assets/from internet/noise shader.gif",0,0,width=app.width,height=app.height,opacity=10)

#################################################
# MVC CS2 mode functionS
#################################################

# user defined in cs2 mode, runs the first time onStep runs to mimic onAppStart of cs3 mode
def onAppStart():
    # runs at the start of the scene
    app.stepsPerSeconds = 30
    app.unplayableSprites = []
    app.debuggingTicks = 0
    app.crntScene=1
    app.sceneState=1
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
    app.group.clear()
    # disallow resizing
    if app.width != 1305 or app.height != 720:
        app.width = 1305
        app.height = 720
    # onAppStart
    if firstRun:
        onAppStart()
        firstRun = False
    if app.crntScene==1:
        scene1Step()

def onKeyHold(events):
    if app.crntScene==1:
        scene1OnKeyHold(events)

def onKeyPress(event):
    if app.crntScene==1:
        scene1OnKeyPress(event)

# load the json dictionnary in the game variable
with open('./gameGlobal.json', 'r') as file:
    game = json.load(file)

# load the json dictionnary in the game variable
with open('./scene1.json', 'r') as file:
    scene1 = json.load(file)

firstRun = True

# run app
cmu_graphics.run()
