# import the library
from cmu_graphics import *
import json
from global_classes import *
from global_helper_functions import *

# import sounds
import pathlib
cntPath = pathlib.Path(__file__).parent.resolve()
dialogueSound = Sound(f'file:///{cntPath}/sounds/dialogue3.mp3')
portalSound = Sound(f'file:///{cntPath}/sounds/portal.mp3')

# import json data
with open(f'./scene10.json', 'r', encoding="utf8") as file:
    scene10 = json.load(file)

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
        app.unplayableSprites[0].stepSelf()
        app.sceneTicks += 1
        if app.sceneTicks == 30:
            portalSound.play()
            app.sceneState = 2
            app.sceneTicks=0
    if app.sceneState == 2:
        app.unplayableSprites[0].stepSelf()
        app.unplayableSprites[1].stepSelf()
        app.sceneTicks += 1
        if app.sceneTicks == 30:
            portalSound.pause()
            app.sceneState = 3
            app.unplayableSprites[1].todraw=[1,0]
    elif app.sceneState >= 3:
        app.unplayableSprites[0].stepSelf()
        app.dialogueBox.stepSelf()


def scene10OnKeyPress(app, event):
    if app.sceneState >= 3 and app.sceneState < 9:
        if "enter" == event or "space" == event:
            dialogueSound.play(restart=True)
            app.sceneState += 1
    if app.sceneState == 9:
        nextScene(app)
        cleanAppVariables(app)


def scene10OnJoyPress(app, button, joystick):
    if joystick == 0:
        if app.sceneState >= 3 and app.sceneState < 9:
            if button == "1":
                dialogueSound.play(restart=True)
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

