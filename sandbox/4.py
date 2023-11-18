from cmu_graphics import *
def drawText(linesList):
    lineHeight = 35
    # lineY starts out at the top of the dialogue box (400)
    lineY = 200
    for line in linesList:
        # Create a label for each line, and move lineY down so the next
        # line is drawn lower
        Label(line, 200, lineY, align='center', size=25, font="monospace", bold=True)
        lineY += lineHeight

drawText(["123456789",
          "abcdefghejklmnopqrstuvwxyz",
          "سشبشثقبثشءغفعتهعة شلااؤلا فقرش"])

'arial', 'monospace', 'cursive', 'caveat', 'cinzel', 'montserrat', 'grenze', 'sacramento', 'orbitron', 'symbols'

"""Arcade Classic2
FFF Forward2
Blox BRK2
Merchant Copy2
Joystix2
Paper Cut2
Back to 19822
Subway Ticker2
3x52"""

"monospace"
"sacramento"

cmu_graphics.run()