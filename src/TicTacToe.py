import os

import pygame
from pygame.locals import *

# Kollar of annat typsnitt finns i mapp

withFont = False
for file in os.listdir("."):
    if file.endswith(".ttf"):
        withFont = file
        break
try:
    print("Använder typsnitt: ", withFont[0:-4])
except:
    print("Hittade inget typsnitt")
fontType = withFont if type(withFont) == str else None
ySize = 775

XO = "X"
started = "X"
available = None
running = 1

xSprite = None
xWinSprite = None
oSprite = None
oWinSprite = None
greenGrid = None
blueGrid = None
restartImg = None
textBG = None

grid = [[[[None, None, None], [None, None, None], [None, None, None]],
         [[None, None, None], [None, None, None], [None, None, None]],
         [[None, None, None], [None, None, None], [None, None, None]]],

        [[[None, None, None], [None, None, None], [None, None, None]],
         [[None, None, None], [None, None, None], [None, None, None]],
         [[None, None, None], [None, None, None], [None, None, None]]],

        [[[None, None, None], [None, None, None], [None, None, None]],
         [[None, None, None], [None, None, None], [None, None, None]],
         [[None, None, None], [None, None, None], [None, None, None]]]]

gridCoords = [[[[None, None, None], [None, None, None], [None, None, None]],
               [[None, None, None], [None, None, None], [None, None, None]],
               [[None, None, None], [None, None, None], [None, None, None]]],

              [[[None, None, None], [None, None, None], [None, None, None]],
               [[None, None, None], [None, None, None], [None, None, None]],
               [[None, None, None], [None, None, None], [None, None, None]]],

              [[[None, None, None], [None, None, None], [None, None, None]],
               [[None, None, None], [None, None, None], [None, None, None]],
               [[None, None, None], [None, None, None], [None, None, None]]]]

winner = None


class button():
    def __init__(self, x, y, width, height, appearance=(255, 255, 255), text=''):
        self.appearance = appearance
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont(fontType, 30)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def fromImg(self, win):
        win.blit(self.appearance, (self.x, self.y))
        pygame.display.flip()

    def isOver(self, pos):
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True

        return False


def drawStatus(board):
    global XO, winner, startButton

    if (winner is None):
        message = "Spelare: " + XO

        font = pygame.font.Font(fontType, 70)
        text = font.render(message, 1, (250, 250, 250))

        board.blit(textBG, (0, 675))
        board.blit(text, (10, 675))
        return False
    else:
        color = (50, 205, 50)
        message = "Vinnare: " + winner
        font = pygame.font.Font(fontType, 70)
        text = font.render(message, 1, (0, 255, 0))
        highlight(board, None, None, (available[0], available[1]), True)

        board.blit(textBG, (0, 675))
        board.blit(text, (10, 675))
        startButton = button(430, 676, 203, 90, restartImg)
        startButton.fromImg(board)
        return True


def showBoard(size, board):
    global running

    get = drawStatus(board)
    size.blit(board, (0, 0))
    pygame.display.flip()
    if get:
        running = 2

        while running == 2:
            pygame.display.flip()
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    running = 0
                    pygame.quit()
                    quit()

                if event.type is MOUSEBUTTONDOWN:
                    if startButton.isOver(pos):
                        board.fill((250, 250, 250))
                        newGame(board)
                if event.type is MOUSEMOTION:
                    if startButton.isOver(pos):
                        startButton.color = (88, 160, 195)
                    else:
                        startButton.color = (173, 216, 230)


def boardPos(mouseX, mouseY):
    if 10 <= mouseY <= 79:
        row = (1, 1)
    elif 80 <= mouseY <= 149:
        row = (1, 2)
    elif 150 <= mouseY <= 219:
        row = (1, 3)
    elif 232 <= mouseY <= 301:
        row = (2, 1)
    elif 302 <= mouseY <= 371:
        row = (2, 2)
    elif 372 <= mouseY <= 441:
        row = (2, 3)
    elif 455 <= mouseY <= 524:
        row = (3, 1)
    elif 525 <= mouseY <= 596:
        row = (3, 2)
    elif 597 <= mouseY <= 668:
        row = (3, 3)
    else:
        return None, None

    if 10 <= mouseX <= 79:
        col = (1, 1)
    elif 80 <= mouseX <= 149:
        col = (1, 2)
    elif 150 <= mouseX <= 219:
        col = (1, 3)
    elif 232 <= mouseX <= 301:
        col = (2, 1)
    elif 302 <= mouseX <= 371:
        col = (2, 2)
    elif 372 <= mouseX <= 441:
        col = (2, 3)
    elif 455 <= mouseX <= 524:
        col = (3, 1)
    elif 525 <= mouseX <= 596:
        col = (3, 2)
    elif 597 <= mouseX <= 668:
        col = (3, 3)
    else:
        return (None, None)

    return (row, col)


def highlight(board, xIn, yIn, old, full=False):
    global greenGrid, blueGrid

    new = getBigPos(xIn, yIn)

    if old is not None:
        xOld = old[0]
        yOld = old[1]
        old = getBigPos(xOld, yOld)
        board.blit(blueGrid, (old[0], old[1]))
    if not full:
        board.blit(greenGrid, (new[0], new[1]))
    else:
        board.blit(blueGrid, (old[0], old[1]))


def getBigPos(x, y):
    highlightPosX = {
        1: 7,
        2: 231,
        3: 454,
        None: None
    }

    highlightPosY = {
        1: 7,
        2: 230,
        3: 453,
        None: None
    }

    return highlightPosX[x], highlightPosY[y]


def drawMove(board, boardRow, boardCol, Piece, onWin=None):
    bigCol = (boardCol[0])
    bigRow = (boardRow[0])
    smallCol = (boardCol[1])
    smallRow = (boardRow[1])

    (mouseX, mouseY) = pygame.mouse.get_pos()

    if 10 <= mouseX <= 79:
        xPos = 9
    elif 80 <= mouseX <= 149:
        xPos = 80
    elif 150 <= mouseX <= 219:
        xPos = 151
    elif 232 <= mouseX <= 301:
        xPos = 232
    elif 302 <= mouseX <= 371:
        xPos = 304
    elif 372 <= mouseX <= 441:
        xPos = 375
    elif 455 <= mouseX <= 524:
        xPos = 456
    elif 525 <= mouseX <= 596:
        xPos = 527
    elif 597 <= mouseX <= 668:
        xPos = 599
    else:
        xPos = None

    if 10 <= mouseY <= 79:
        yPos = 10
    elif 80 <= mouseY <= 149:
        yPos = 82
    elif 150 <= mouseY <= 219:
        yPos = 152
    elif 232 <= mouseY <= 301:
        yPos = 233
    elif 302 <= mouseY <= 371:
        yPos = 304
    elif 372 <= mouseY <= 441:
        yPos = 375
    elif 455 <= mouseY <= 524:
        yPos = 456
    elif 525 <= mouseY <= 596:
        yPos = 528
    elif 597 <= mouseY <= 668:
        yPos = 598
    else:
        yPos = None

    if onWin is None:
        if Piece == 'O':
            # pygame.draw.circle(board, (70, 70, 170), (centerX, centerY), 17, 2)
            board.blit(oSprite, (xPos + 5, yPos + 2))
            xa = xPos + 5
            ya = yPos + 2
        else:
            board.blit(xSprite, (xPos + 5, yPos + 4))
            xa = xPos + 5
            ya = yPos + 4

        grid[bigRow - 1][bigCol - 1][smallRow - 1][smallCol - 1] = Piece
        gridCoords[bigRow - 1][bigCol - 1][smallRow - 1][smallCol - 1] = (xa, ya)

    else:

        (xPos, yPos) = gridCoords[bigRow - 1][bigCol - 1][smallRow - 1][smallCol - 1]

        if Piece == 'O':
            board.blit(oWinSprite, (xPos, yPos))
        else:
            board.blit(xWinSprite, (xPos, yPos))


def clickBoard(board):
    global grid, XO, available

    (mouseX, mouseY) = pygame.mouse.get_pos()
    (row, col) = boardPos(mouseX, mouseY)

    if (row, col) == (None, None):
        return

    bigRow = row[0]
    smallRow = row[1]

    bigCol = col[0]
    smallCol = col[1]

    if ((grid[bigRow - 1][bigCol - 1][smallRow - 1][smallCol - 1] == "X") or (
            grid[bigRow - 1][bigCol - 1][smallRow - 1][smallCol - 1] == "O")):
        return

    if available == None:
        pass
    else:
        if available == (bigCol, bigRow):
            pass
        else:
            return

    drawMove(board, row, col, XO)
    oldAv = available
    available = (smallCol, smallRow)

    avGrid = grid[available[1] - 1][available[0] - 1]

    noneCount = 0
    for x, y, z in avGrid:
        if x is None:
            noneCount += 1
        if y is None:
            noneCount += 1
        if z is None:
            noneCount += 1

    if noneCount != 0:
        highlight(board, available[0], available[1], oldAv)
    else:
        available = None
        highlight(board, None, None, oldAv, True)

    if XO == "X":
        XO = "O"
    else:
        XO = "X"

    if oldAv is None:
        oldAv = (None, None)
    noneCount = 0
    found = False
    for q, w, e in grid:
        for x, y, z in q, w, e:
            for a, s, d in x, y, z:
                noneCount += 1 if a is None else 0
                noneCount += 1 if s is None else 0
                noneCount += 1 if d is None else 0
                if noneCount >= 1:
                    found = True
                    break
            if found:
                break
        if found:
            break
    if noneCount == 0:
        board.fill(255, 255, 255)
        message = "Trodde inte ens att det kunde bli lika"

        font = pygame.font.Font(fontType, 70)
        text = font.render(message, 1, (10, 10, 10))

        board.fill((250, 250, 250), (0, 0, 675, 100))
        board.blit(text, (10, 675))
        return False


def gameWon(board):
    global grid, winner
    won = False
    for bigRow in range(1, 4):
        for bigCol in range(1, 4):
            for smallRow in range(1, 4):
                if ((grid[bigRow - 1][bigCol - 1][smallRow - 1][0] == grid[bigRow - 1][bigCol - 1][smallRow - 1][1] ==
                     grid[bigRow - 1][bigCol - 1][smallRow - 1][2]) and
                        (grid[bigRow - 1][bigCol - 1][smallRow - 1][0] is not None)):
                    winner = grid[bigRow - 1][bigCol - 1][smallRow - 1][0]
                    drawMove(board, (bigRow, smallRow), (bigCol, 1), winner, True)
                    drawMove(board, (bigRow, smallRow), (bigCol, 2), winner, True)
                    drawMove(board, (bigRow, smallRow), (bigCol, 3), winner, True)
                    break

    for bigRow in range(1, 4):
        for bigCol in range(1, 4):
            for smallCol in range(1, 4):
                if (grid[bigRow - 1][bigCol - 1][0][smallCol - 1] == grid[bigRow - 1][bigCol - 1][1][smallCol - 1] ==
                    grid[bigRow - 1][bigCol - 1][2][smallCol - 1]) and \
                        (grid[bigRow - 1][bigCol - 1][0][smallCol - 1] is not None):
                    winner = grid[bigRow - 1][bigCol - 1][0][smallCol - 1]
                    drawMove(board, (bigRow, 1), (bigCol, smallCol), winner, True)
                    drawMove(board, (bigRow, 2), (bigCol, smallCol), winner, True)
                    drawMove(board, (bigRow, 3), (bigCol, smallCol), winner, True)
                    break

    for x in range(0, 3):
        for y in range(0, 3):
            if (grid[x][y][0][0] == grid[x][y][1][1] == grid[x][y][2][2]) and \
                    (grid[x][y][0][0] is not None):
                winner = grid[x][y][0][0]
                drawMove(board, (x + 1, 1), (y + 1, 1), winner, True)
                drawMove(board, (x + 1, 2), (y + 1, 2), winner, True)
                drawMove(board, (x + 1, 3), (y + 1, 3), winner, True)

            if (grid[y][x][0][2] == grid[y][x][1][1] == grid[y][x][2][0]) and \
                    (grid[y][x][0][2] is not None):
                winner = grid[y][x][0][2]
                drawMove(board, (y + 1, 3), (x + 1, 1), winner, True)
                drawMove(board, (y + 1, 2), (x + 1, 2), winner, True)
                drawMove(board, (y + 1, 1), (x + 1, 3), winner, True)


def initBoard(size):
    background = pygame.Surface(size.get_size())
    background = background.convert()
    background.fill((250, 250, 250))
    bg = pygame.image.load("./img/bg.png")
    background.blit(bg, (0, 0))

    return background


# --------------------------------------------------------------------
def newGame(board):
    global XO, available, grid, winner, running, started

    XO = "O" if started == "X" else "X"
    started = str(XO)
    available = None

    grid = [[[[None, None, None], [None, None, None], [None, None, None]],
             [[None, None, None], [None, None, None], [None, None, None]],
             [[None, None, None], [None, None, None], [None, None, None]]],

            [[[None, None, None], [None, None, None], [None, None, None]],
             [[None, None, None], [None, None, None], [None, None, None]],
             [[None, None, None], [None, None, None], [None, None, None]]],

            [[[None, None, None], [None, None, None], [None, None, None]],
             [[None, None, None], [None, None, None], [None, None, None]],
             [[None, None, None], [None, None, None], [None, None, None]]]]

    winner = None
    running = 1
    startGame()


def startGame():
    global running, xSprite, oSprite, greenGrid, blueGrid, oWinSprite, xWinSprite, restartImg, textBG

    pygame.init()
    size = pygame.display.set_mode((675, ySize))
    pygame.display.set_caption('Extrem 3-i-rad')

    board = initBoard(size)

    xSprite = pygame.image.load("./img/X.png").convert_alpha()
    xWinSprite = pygame.image.load("./img/XWin.png")
    oSprite = pygame.image.load("./img/O.png").convert_alpha()
    oWinSprite = pygame.image.load("./img/OWin.png").convert_alpha()
    greenGrid = pygame.image.load("./img/greenGrid.png").convert_alpha()
    blueGrid = pygame.image.load("./img/blueGrid.png").convert_alpha()
    restartImg = pygame.image.load("./img/restart.png").convert_alpha()
    textBG = pygame.image.load("./img/textBG.png").convert_alpha()


    xOld = None
    yOld = None

    while running == 1:
        for event in pygame.event.get():
            if event.type is QUIT:
                running = 0
            elif event.type is MOUSEBUTTONDOWN:
                clickBoard(board)
            gameWon(board)
            showBoard(size, board)


if __name__ == "__main__":
    startGame()
