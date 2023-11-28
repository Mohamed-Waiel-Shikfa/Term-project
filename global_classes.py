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
                          font="DejaVu Sans Mono", bold=True, align="left-top")
                textYPos += 35
            drawLabel("SPACE or ENTER to continue for PC, A to continue for Arcade ...", 600*self.scale+self.offsetx, textYPos*self.scale+self.offsety, size=25*self.scale*2/3,
                      font="Monospace", bold=True, align="left-top")

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
        drawLabel(question, 650*self.scale+self.scale,200*self.scale+self.offsety, size=22*self.scale*2/3,font="monospace", bold=True, )
        drawLabel(question2, 650*self.scale+self.scale,230*self.scale+self.offsety, size=22*self.scale*2/3,font="monospace", bold=True)
        drawLabel(question3, 650*self.scale+self.scale,260*self.scale+self.offsety, size=22*self.scale*2/3,font="monospace", bold=True)
        for i in range(4):
            drawLabel(self.labelText[i], (430+150*i)*self.scale+self.offsetx, 375*self.scale+self.offsety, size = 256*self.scale*2/3)
        drawLabel("On pc just type the number.", 650*self.scale+self.offsetx, 480*self.scale+self.offsety, size=28*self.scale*2/3, bold=True)
        drawLabel("On arcade press B to increase current digit and A to validate it.", 650*self.scale+self.offsetx, 510*self.scale+self.offsety, size=28*self.scale*2/3, bold=True)
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

