# import the library
from cmu_graphics import *
import json
from global_classes import *
from global_helper_functions import *
from tetris import *

import pathlib
cntPath = pathlib.Path(__file__).parent.resolve()
music = Sound(f'file:///{cntPath}/sounds/Hotel lobby music.mp3')


with open(f'./scene12.json', 'r', encoding="utf8") as file:
    scene12 = json.load(file)

#################################################
# scene 12 classes
#################################################
#################################################
# Scene 12 function
#################################################

def loadScene12(app):
    music.play(restart=True)
    appendToUnplayable(app, scene12,"static")
    appendToUnplayable(app, scene12,"rotating", rotatingSpriteClass)
    loadTetris(app)


def scene12OnKeyPress(app, event):
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
    if event == "enter" and  20-app.sceneTicks//30<=0:
        nextScene(app)
        cleanAppVariables(app)


def scene12OnJoyPress(app, button, joystick):
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
            music.pause()
            nextScene(app)
            cleanAppVariables(app)


def scene12OnDigitalJoyAxis(app, results, joystick):
    if joystick==0:
        if (1,1) in results:
            moveFallingPiece(app, 1, 0)
        elif (0,1) in results:
            moveFallingPiece(app, 0, 1)
        elif (0,-1) in results:
            moveFallingPiece(app, 0, -1)


def scene12Step(app):
    # code executed at every frame

    # if the game is running and the falling piece can't fall anymore calls
    # placeFallingPiece to place it on the board the makes a new piece
    if app.sceneState==0:
        loadScene12(app)
        app.sceneState=1
    else:
        app.sceneTicks+=1
        for isprite in app.unplayableSprites:
            isprite.stepSelf()
        stepTetris(app)


def scene12Draw(app):
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

