# import the library
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
from global_classes import *
from global_helper_functions import *


def gameDimensions(app):
    # These values are set to the writeup defaults
    rows = 17
    cols = 10
    cellSize = 10*app.scale
    margin = 12*app.scale
    offsetx=590*app.scale+app.offsetx
    offsety=161*app.scale+app.offsety
    return (rows, cols, cellSize, margin, offsetx, offsety)


def loadTetris(app):
    # initiate the game by creating and assigning all necessary variables

    # Seven "standard" pieces (tetrominoes)
    iPiece = [
        [True, True, True, True]
    ]

    jPiece = [
        [True, False, False],
        [True, True, True]
    ]

    lPiece = [
        [False, False, True],
        [True, True, True]
    ]

    oPiece = [
        [True, True],
        [True, True]
    ]

    sPiece = [
        [False, True, True],
        [True, True, False]
    ]

    tPiece = [
        [False, True, False],
        [True, True, True]
    ]

    zPiece = [
        [True, True, False],
        [False, True, True]
    ]
    app.tetrisPieces = [iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece]
    # colors
    app.tetrisPieceColors = ["red", "yellow",
                             "magenta", "pink", "cyan", "green", "orange"]
    app.emptyColor = 'blue'
    app.color = 'orange'
    # dimension and board
    app.rows, app.cols, app.cellSize, app.margin, app.tetrisOffsetx, app.tetrisOffsety = gameDimensions(app)
    app.board = [[app.emptyColor for _ in range(app.cols)] for _ in
                 range(app.rows)]
    # game states variable
    app.runningBonus = False
    app.isPaused = False
    app.isGameOver = False
    app.score = 0
    # first falling piece of the game needs to be created here
    newFallingPiece(app)


def stepTetris(app):
    if app.sceneTicks%30==0:
        app.rows, app.cols, app.cellSize, app.margin, app.tetrisOffsetx, app.tetrisOffsety = gameDimensions(app)
        if not app.isGameOver and not app.isPaused and not moveFallingPiece(app,
                                                                            1, 0):
            placeFallingPiece(app)
            newFallingPiece(app)
            # ends the game if right after making a new falling piece, it is in
            # an illegal state
            if not fallingPieceIsLegal(app):
                app.isGameOver = True


def drawTetris(app):
        drawRect(app.tetrisOffsetx, app.tetrisOffsety, 2*app.margin+app.cols*app.cellSize,2*app.margin+app.rows*app.cellSize, fill='orange')
        # draws the game window

        # draw the different element of the board, which are the board the
        # falling piece and the score
        drawBoard(app)
        drawFallingPiece(app)
        drawScore(app)
        # if the player is dead draws a Game over message
        if app.isGameOver:
            drawRect(app.margin + app.tetrisOffsetx, app.margin + app.cellSize + app.tetrisOffsety,
                    app.cols * app.cellSize, app.cellSize * 2)
            drawLabel("Game Over!", app.cols // 2 * app.cellSize + app.margin + app.tetrisOffsetx,
                    2 * app.cellSize + app.margin + app.tetrisOffsety, fill='yellow', align='center',
                    size=app.cellSize, bold=True)


#################################################
# Tetris tutorial's functions in order
#################################################
def drawBoard(app):
    # draw the board by going through every row and every cell in that row
    # and drawing that cell

    for irow in range(app.rows):
        for jcol in range(app.cols):
            drawCell(app, irow, jcol)


def drawCell(app, row, col, color=None):
    # draws cells which are squares on the game window

    # if it is a board cell, the position arguments are the final coordinates
    finalcol = col * app.cellSize + app.margin + app.tetrisOffsetx
    finalrow = row * app.cellSize + app.margin + app.tetrisOffsety
    if color is None:
        color = app.board[row][col]
    # if it is not a board cell then we need to add the relative position of
    # the piece to the final coordinates
    else:
        finalcol += app.fallingPieceCol * app.cellSize
        finalrow += app.fallingPieceRow * app.cellSize
    drawRect(finalcol, finalrow, app.cellSize,
             app.cellSize, fill=color, border='black')


def newFallingPiece(app):
    # generate a new falling piece

    # selects a random piece and store calculated useful attribute of this
    # piece in the app (module)
    import random
    randomIndex = random.randint(0, len(app.tetrisPieces) - 1)
    app.fallingPiece = copy.deepcopy(app.tetrisPieces[randomIndex])
    # if in bonus mode the color of the piece will be a randomised color from
    # tetrisPieceColors, which make the game more challenging
    if app.runningBonus:
        randomIndex = random.randint(0, len(app.tetrisPieces) - 1)
    app.fallingPieceColor = app.tetrisPieceColors[randomIndex]
    app.numFallingPieceCols = len(app.fallingPiece[0])
    app.numFallingPieceRows = len(app.fallingPiece)
    app.fallingPieceRow = 0
    app.fallingPieceCol = app.cols // 2 - app.numFallingPieceCols // 2


def drawFallingPiece(app):
    # draws falling piece in the same way the board is drawn

    for irow in range(app.numFallingPieceRows):
        for jcol in range(app.numFallingPieceCols):
            if app.fallingPiece[irow][jcol]:
                drawCell(app, irow, jcol, app.fallingPieceColor)


def moveFallingPiece(app, drow, dcol):
    # move the falling piece only if the move is legal in 3 steps

    # move the falling piece by changing its coordinate
    app.fallingPieceCol += dcol
    app.fallingPieceRow += drow
    # check if the new coordinate result in a legal state
    if not fallingPieceIsLegal(app):
        # if not undo the change to the coordinates
        app.fallingPieceCol -= dcol
        app.fallingPieceRow -= drow
        return False
    return True


def fallingPieceIsLegal(app):
    # checks if the falling piece is in a legal state

    # To return true and validate the piece state, it confirms that:
    # (1) the cell is in fact on the board
    # (2) the color at that location on the board is the emptyColor
    # Otherwise it immediately returns False
    for cellRow in range(len(app.fallingPiece)):
        pieceRow = app.fallingPiece[cellRow]
        for cellCol in range(len(pieceRow)):
            cell = pieceRow[cellCol]
            if cell:
                if app.fallingPieceCol < 0 or app.fallingPieceCol + \
                        app.numFallingPieceCols > app.cols or \
                        app.fallingPieceRow + app.numFallingPieceRows > \
                        app.rows or app.fallingPieceRow < 0:
                    return False
                for boardCol in range(app.cols):
                    for boardRow in range(app.rows):
                        if app.board[boardRow][
                            boardCol] != app.emptyColor and boardCol == \
                                app.fallingPieceCol + cellCol and boardRow == \
                                app.fallingPieceRow + cellRow:
                            return False
    return True


def rotateFallingPiece(app):
    # rotate the falling piece only if the move is legal in 5 steps

    # 1. Store the relevant values associated with the old piece
    tempNumFallingPieceCols = app.numFallingPieceCols
    tempNumFallingPieceRows = app.numFallingPieceRows
    tempfallingPieceCol = app.fallingPieceCol
    tempFallingPieceRow = app.fallingPieceRow
    tempFallingPiece = copy.deepcopy(app.fallingPiece)
    # 2. Compute the relevant values according to the old dimensions.
    app.numFallingPieceCols = tempNumFallingPieceRows
    app.numFallingPieceRows = tempNumFallingPieceCols
    app.fallingPieceCol = tempfallingPieceCol + tempNumFallingPieceCols // 2 \
                          - app.numFallingPieceCols // 2
    app.fallingPieceRow = tempFallingPieceRow + tempNumFallingPieceRows // 2 \
                          - app.numFallingPieceRows // 2
    # 3. Assigns fallingPiece to a 2D list, based on the new dimensions, filled
    # with None values.
    app.fallingPiece = [[None for _ in range(app.numFallingPieceCols)] for _ in
                        range(app.numFallingPieceRows)]
    # 4. Iterate through each of the cells in the original piece, and move
    # each value to its new location in the new piece.

    for cellRow in range(len(tempFallingPiece)):
        pieceRow = tempFallingPiece[cellRow]
        for cellCol in range(len(pieceRow)):
            cell = pieceRow[cellCol]
            app.fallingPiece[app.numFallingPieceRows - cellCol - 1][cellRow] \
                = cell
    # 5. Check whether the new piece is legal. If it isn't, restore the all
    # of the values based on the temporary variables created in Step 1.
    if not fallingPieceIsLegal(app):
        app.fallingPiece = copy.deepcopy(tempFallingPiece)
        app.numFallingPieceCols = tempNumFallingPieceCols
        app.numFallingPieceRows = tempNumFallingPieceRows
        app.fallingPieceRow = tempFallingPieceRow
        app.fallingPieceCol = tempfallingPieceCol


def placeFallingPiece(app):
    # places the falling piece on the bard

    # iterates through each cell of the piece
    for irow in range(app.numFallingPieceRows):
        for jcol in range(app.numFallingPieceCols):
            # if the cell is a colored one, change the color of the board at
            # the coordinates of that cell to the color of the piece
            if app.fallingPiece[irow][jcol]:
                finalrow = irow + app.fallingPieceRow
                finalcol = jcol + app.fallingPieceCol
                app.board[finalrow][finalcol] = app.fallingPieceColor
    # after the piece has been placed, it is necessary to remove any full rows
    removeFullRows(app)


def removeFullRows(app):
    # removes full rows from the board

    # we first count how many full row there is as it is needed later
    fullRows = 0
    for irow in range(app.rows):
        if not app.emptyColor in app.board[irow]:
            fullRows += 1
    # we make a new board by replacing full rows by an empty list
    noFullRowBoard = [[color for color in copy.copy(app.board[irow])
                       if app.emptyColor in app.board[irow]] for irow in
                      range(app.rows)]
    # remove all the empty lists from our new board effectively deleting the
    # full rows
    i = 0
    while i < len(noFullRowBoard):
        if noFullRowBoard[i] == []:
            noFullRowBoard.pop(i)
        else:
            i += 1
    # replace the previous board with full rows number of empty rows (so at
    # the top of our new board), and below that, the rest of the board that was
    # not empty
    app.board = [[app.emptyColor for _ in range(
        app.cols)] for _ in range(fullRows)] + copy.deepcopy(noFullRowBoard)
    # updates the score by adding the square of the number of rows removed
    app.score += fullRows ** 2


def drawScore(app):
    # displays the score on the top of the game window

    drawLabel("Score: " + str(app.score),
              app.cols // 2 * app.cellSize + app.margin + app.tetrisOffsetx,
              app.margin // 2 + app.tetrisOffsety, fill='blue', align='center',
              size=app.cellSize // 1.2, bold=True)


def hardDropFallingPiece(app):
    # hard drops the piece by moving it down until it can't be moved any further

    while moveFallingPiece(app, 1, 0):
        moveFallingPiece(app, 1, 0)
