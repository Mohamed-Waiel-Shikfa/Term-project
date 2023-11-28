# import the library
from cmu_graphics import *
import json
from global_classes import *
from global_helper_functions import *

# import sound
import pathlib
cntPath = pathlib.Path(__file__).parent.resolve()
loading = Sound(f'file:///{cntPath}/sounds/loading1.opus')

# import json data
with open(f'./scene1.json', 'r', encoding="utf8") as file:
    scene1 = json.load(file)

#################################################
# Scene 1 function
#################################################
def loadScene1(app):
    loading.play(restart=True)
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
            loading.pause()
            nextScene(app)
            cleanAppVariables(app)


def scene1Draw(app):
    drawRect(0, 0, 1305, 720)
    for iSprite in app.unplayableSprites:
        iSprite.drawSelf()

