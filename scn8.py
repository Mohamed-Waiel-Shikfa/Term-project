# import the library
from cmu_graphics import *
import json
from global_classes import *
from global_helper_functions import *

# import sounds
import pathlib
cntPath = pathlib.Path(__file__).parent.resolve()
dialogueSound = Sound(f'file:///{cntPath}/sounds/dialogue3.mp3')
succes=Sound(f'file:///{cntPath}/sounds/succes.mp3')

# import json data
with open(f'./scene8.json', 'r', encoding="utf8") as file:
    scene8 = json.load(file)


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
        app.player.x+=8
        app.sceneTicks += 1
        if app.sceneTicks == 12:
            app.sceneState = 3
    if 5 > app.sceneState > 2 or 7 > app.sceneState > 5:
        app.dialogueBox.stepSelf()
    if app.sceneState == 5:
        if app.player.x>1200:
            succes.play(restart=True)
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
            dialogueSound.play(restart=True)
            app.sceneState += 1
    if app.sceneState == 7:
        nextScene(app)
        cleanAppVariables(app)


def scene8OnJoyPress(app, button, joystick):
    if joystick == 0:
        if  5> app.sceneState > 2 or 7 > app.sceneState > 5:
            if button == "1":
                dialogueSound.play(restart=True)
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

