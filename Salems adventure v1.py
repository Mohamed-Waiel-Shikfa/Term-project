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
    def drawSelf(self, app):
        # trying rectangle to prove cmu graphics is slow with images
        drawRect(self.x, self.y,
                 self.width, self.height, rotateAngle=self.angle, fill=self.color, opacity=self.opacity)

        # drawImage(self.urls[self.todraw[0]]+self.images[self.todraw[0]][self.todraw[1]], self.x,
        #           self.y, width=self.width, height=self.height, rotateAngle=self.angle, opacity=self.opacity)

        # print("drawed", self)


# class for all rotating sprite as rotating in pixel software is really hard
class rotatingSpriteClass(unplayableSpriteClass):
    # initiate the same argument as the parent class plus some more by loading data from json file
    def __init__(self, *args, angle=0, opacity=100):
        super().__init__(*args, angle=angle, opacity=opacity)
        self.animationDuration = randint(5, 10)
        self.animationPause = randint(15, 60)
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
                self.animationDuration = randint(5, 10)
                self.animationPause = randint(15, 60)
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
        self.notAllowed=[]
        for i in args[-1]:
            data=repr(i)
            data=data.split(";")
            self.notAllowed.append((int(data[5]),int(data[6]),int(data[5])+int(data[7]),int(data[6])+int(data[8])))
        print(self.notAllowed)

    # respond to keyHold
    def selfKeyHold(self, events):
        if ("up" in events or "w" in events) and self.allowedMovementUp():
            self.y -= 10
        if ("down" in events or "s" in events) and self.allowedMovementDown():
            self.y += 10
        if ("right" in events or "d" in events) and self.allowedMovementRight():
            self.x += 10
        if ("left" in events or "a" in events) and self.allowedMovementLeft():
            self.x -= 10

    def allowedMovementUp(self):
        if 230 <= self.x <= 430 and self.y-10 < 190:
            return False
        if 670 <= self.x <= 870 and self.y-10 < 190:
            return False
        return True

    def allowedMovementDown(self):
        if 0 <= self.x <= 270 and self.y+10 > 40:
            return False
        if 500 <= self.x <= 770 and self.y+10 > 440:
            return False
        if 950 <= self.x <= 1270 and self.y+10 > 300:
            return False
        return True

    def allowedMovementRight(self):
        if 0 <= self.y <= 190 and self.x+10 > 230 and self.x < 430:
            return False
        # if 500<=self.y<=770 and self.x+10>440:
        #     return False
        # if 950<=self.y<=1270 and self.x+10>300:
        #     return False
        # if 950<=self.y<=1270 and self.x+10>300:
        #     return False
        return True

    def allowedMovementLeft(self):
        return True


def onAppStart(app):
    # runs at the start of the scene
    # app.debuggingTicks = 0
    app.stepsPerSeconds = 30
    app.unplayableSprites = []
    path1 = game["scene1"]["unplayable"]
    # appends object of unplayableSpriteClass class and rotatingSpriteClass class to the list app.unplayableSprites
    for key, value in path1["static"].items():
        app.unplayableSprites.append(unplayableSpriteClass(
            key, value["url"], value["images"], value["toDraw"], value["x"], value["y"], value["width"], value["height"], value["color"]))
    for key, value in path1["rotating"].items():
        app.unplayableSprites.append(rotatingSpriteClass(
            key, value["url"], value["images"], value["toDraw"], value["x"], value["y"], value["width"], value["height"], value["color"]))
    # saves the player object in app.player
    path2 = game["scene1"]["player"]
    app.player = player(
        "player", path2["url"], path2["images"], path2["toDraw"], path2["x"], path2["y"], path2["width"], path2["height"], path2["color"], app.unplayableSprites)
    # shader feature to develop after mvp
    # for key, value in path1["bonus"].items():
    #     app.unplayableSprites.append(unplayableSpriteClass(
    #         key, value["url"], value["images"], value["toDraw"], value["x"], value["y"], value["width"], value["height"],opacity=value["opacity"]))
    # print to confirm initiation
    for iSprite in app.unplayableSprites:
        print(iSprite)
        print(repr(iSprite))
    print(app.player)
    print(repr(app.player))


def onStep(app):
    # increase debugging ticks by 1
    # app.debuggingTicks += 1
    # disallow resizing
    if app.width != 1305 or app.height != 720:
        app.width = 1305
        app.height = 720
    # calls the onStep of every object
    for iSprite in app.unplayableSprites:
        iSprite.stepSelf()


def redrawAll(app):
    # calls the draw of every object
    for iSprite in app.unplayableSprites:
        iSprite.drawSelf(app)
    app.player.drawSelf(app)
    # draw the number of frame since the beginining of the game
    # drawLabel(str(app.debuggingTicks), 650, 360, fill='red', size=24)
    # shader feature to develop after mvp
    # drawImage("image/salem adventure/assets/from internet/noise shader.gif",0,0,width=app.width,height=app.height,opacity=10)


def onKeyHold(app, events):
    # calls keyHold of the player
    app.player.selfKeyHold(events)


# load the json dictionnary in the game variable
with open('./game.json', 'r') as file:
    game = json.load(file)

# run app
runApp(game["global"]["width"], game["global"]["height"])
