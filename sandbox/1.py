from cmu_graphics import *

# Load the image once
def onAppStart(app):
    app.img = Image("images/salem adventure/assets/Home made/background garaje door/background garaje door v2.png", 0, 0)
#doesn't work, cs2 mode isn't compatible with cs3 mode
def onKeyHold(app, events): 
    # Draw the image in onStep
    if "up" in events or "w" in events:
        app.img.centerY -= 10
    if "down" in events or "s" in events:
        app.img.centerY += 10
    if "right" in events or "d" in events:
        app.img.centerX += 10
    if "left" in events or "a" in events:
        app.img.centerX -= 10

runApp(width=1305,height=720)
