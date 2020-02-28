import os

import pygame
from pygame.locals import *

# Kollar of annat typsnitt finns i mapp

withFont = False
for file in os.listdir("."):
    if file.endswith(".ttf"):
        withFont = file
        break
print("Using font: ", withFont[0:-4])

fontType = withFont if type(withFont) == str else None
ySize = 520

XO = "X"
available = None
running = 1

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


class button():
    def __init__(self, buttonColor, x, y, width, height, text=''):
        self.color = buttonColor
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
    def isOver(self, pos):
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True

        return False


def initBoard(ttt):
    background = pygame.Surface(ttt.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    pygame.draw.line(background, (0, 0, 0), (50, 0), (50, 450), 2)
    pygame.draw.line(background, (0, 0, 0), (100, 0), (100, 450), 2)
    pygame.draw.line(background, (0, 0, 0), (150, 0), (150, 450), 3)
    pygame.draw.line(background, (0, 0, 0), (200, 0), (200, 450), 2)
    pygame.draw.line(background, (0, 0, 0), (250, 0), (250, 450), 2)
    pygame.draw.line(background, (0, 0, 0), (300, 0), (300, 450), 3)
    pygame.draw.line(background, (0, 0, 0), (350, 0), (350, 450), 2)
    pygame.draw.line(background, (0, 0, 0), (400, 0), (400, 450), 2)
    pygame.draw.line(background, (0, 0, 0), (450, 0), (450, 450), 3)
    pygame.draw.line(background, (0, 0, 0), (0, 0), (450, 0), 3)
    pygame.draw.line(background, (0, 0, 0), (0, 450), (450, 450), 3)

    pygame.draw.line(background, (0, 0, 0), (0, 50), (450, 50), 2)
    pygame.draw.line(background, (0, 0, 0), (0, 100), (450, 100), 2)
    pygame.draw.line(background, (0, 0, 0), (0, 150), (450, 150), 3)
    pygame.draw.line(background, (0, 0, 0), (0, 200), (450, 200), 2)
    pygame.draw.line(background, (0, 0, 0), (0, 250), (450, 250), 2)
    pygame.draw.line(background, (0, 0, 0), (0, 300), (450, 300), 3)
    pygame.draw.line(background, (0, 0, 0), (0, 350), (450, 350), 2)
    pygame.draw.line(background, (0, 0, 0), (0, 400), (450, 400), 2)
    pygame.draw.line(background, (0, 0, 0), (0, 450), (450, 450), 3)
    pygame.draw.line(background, (0, 0, 0), (0, 0), (0, 450), 3)
    pygame.draw.line(background, (0, 0, 0), (450, 0), (450, 450), 3)

    return background


def drawStatus(board):
    global XO, winner

    if (winner is None):
        message = "Spelare: " + XO

        font = pygame.font.Font(fontType, 50)
        text = font.render(message, 1, (10, 10, 10))

        board.fill((250, 250, 250), (0, 450, 450, 100))
        board.blit(text, (10, 450))
        return False
    else:
        color = (50, 205, 50)
        resetGrid(board)
        message = "Vinnare: " + winner
        font = pygame.font.Font(fontType, 50)
        text = font.render(message, 1, (10, 10, 10))

        board.fill(color, (0, 450, 450, 100))
        board.blit(text, (10, 450))
        return True


def showBoard(ttt, board):
    global running

    get = drawStatus(board)
    ttt.blit(board, (0, 0))
    pygame.display.flip()
    if get:
        running = 2
        startButton = button((173, 216, 230), 300, 460, 170, 30, "Kör igen!")
        startButton.draw(board, (0, 0, 0))

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
                        resetGrid(board)
                if event.type is MOUSEMOTION:
                    if startButton.isOver(pos):
                        startButton.color = (88, 160, 195)
                    else:
                        startButton.color = (173, 216, 230)





def boardPos(mouseX, mouseY):
    if (mouseY < 50):
        row = (1, 1)
    elif (mouseY < 100):
        row = (1, 2)
    elif (mouseY < 150):
        row = (1, 3)
    elif (mouseY < 200):
        row = (2, 1)
    elif (mouseY < 250):
        row = (2, 2)
    elif (mouseY < 300):
        row = (2, 3)
    elif (mouseY < 350):
        row = (3, 1)
    elif (mouseY < 400):
        row = (3, 2)
    else:
        row = (3, 3)

    if (mouseX < 50):
        col = (1, 1)
    elif (mouseX < 100):
        col = (1, 2)
    elif (mouseX < 150):
        col = (1, 3)
    elif (mouseX < 200):
        col = (2, 1)
    elif (mouseX < 250):
        col = (2, 2)
    elif (mouseX < 300):
        col = (2, 3)
    elif (mouseX < 350):
        col = (3, 1)
    elif (mouseX < 400):
        col = (3, 2)
    else:
        col = (3, 3)

    return (row, col)


def resetGrid(board):
    pygame.draw.line(board, (0, 0, 0), (50, 0), (50, 450), 2)
    pygame.draw.line(board, (0, 0, 0), (100, 0), (100, 450), 2)
    pygame.draw.line(board, (0, 0, 0), (150, 0), (150, 450), 3)
    pygame.draw.line(board, (0, 0, 0), (200, 0), (200, 450), 2)
    pygame.draw.line(board, (0, 0, 0), (250, 0), (250, 450), 2)
    pygame.draw.line(board, (0, 0, 0), (300, 0), (300, 450), 3)
    pygame.draw.line(board, (0, 0, 0), (350, 0), (350, 450), 2)
    pygame.draw.line(board, (0, 0, 0), (400, 0), (400, 450), 2)
    pygame.draw.line(board, (0, 0, 0), (450, 0), (450, 450), 3)
    pygame.draw.line(board, (0, 0, 0), (0, 0), (450, 0), 3)
    pygame.draw.line(board, (0, 0, 0), (0, 450), (450, 450), 3)

    pygame.draw.line(board, (0, 0, 0), (0, 50), (450, 50), 2)
    pygame.draw.line(board, (0, 0, 0), (0, 100), (450, 100), 2)
    pygame.draw.line(board, (0, 0, 0), (0, 150), (450, 150), 3)
    pygame.draw.line(board, (0, 0, 0), (0, 200), (450, 200), 2)
    pygame.draw.line(board, (0, 0, 0), (0, 250), (450, 250), 2)
    pygame.draw.line(board, (0, 0, 0), (0, 300), (450, 300), 3)
    pygame.draw.line(board, (0, 0, 0), (0, 350), (450, 350), 2)
    pygame.draw.line(board, (0, 0, 0), (0, 400), (450, 400), 2)
    pygame.draw.line(board, (0, 0, 0), (0, 450), (450, 450), 3)
    pygame.draw.line(board, (0, 0, 0), (0, 0), (0, 450), 3)
    pygame.draw.line(board, (0, 0, 0), (450, 0), (450, 450), 3)


def highlight(board, xIn, yIn):
    x = (xIn - 1) * 150
    y = (yIn - 1) * 150

    resetGrid(board)

    pygame.draw.line(board, (255, 0, 0), (x, y), (x + 150, y), 3)
    pygame.draw.line(board, (255, 0, 0), (x, y), (x, y + 150), 3)
    pygame.draw.line(board, (255, 0, 0), (x + 50, y), (x + 50, y + 150), 2)
    pygame.draw.line(board, (255, 0, 0), (x + 100, y), (x + 100, y + 150), 2)
    pygame.draw.line(board, (255, 0, 0), (x + 150, y), (x + 150, y + 150), 3)
    pygame.draw.line(board, (255, 0, 0), (x, y + 50), (x + 150, y + 50), 2)
    pygame.draw.line(board, (255, 0, 0), (x, y + 100), (x + 150, y + 100), 2)
    pygame.draw.line(board, (255, 0, 0), (x, y + 150), (x + 150, y + 150), 3)


def drawMove(board, boardRow, boardCol, Piece, onWin=None):
    bigCol = (boardCol[0])
    bigRow = (boardRow[0])
    smallCol = (boardCol[1])
    smallRow = (boardRow[1])

    centerX = (((bigCol - 1) * 3 + smallCol - 1) * 50) + 25

    centerY = (((bigRow - 1) * 3 + smallRow - 1) * 50) + 25
    if onWin == None:
        if (Piece == 'O'):
            pygame.draw.circle(board, (70, 70, 170), (centerX, centerY), 17, 2)
        else:
            pygame.draw.line(board, (0, 0, 0), (centerX - 11, centerY - 11),
                             (centerX + 11, centerY + 11), 2)
            pygame.draw.line(board, (0, 0, 0), (centerX + 11, centerY - 11),
                             (centerX - 11, centerY + 11), 2)

        grid[bigRow - 1][bigCol - 1][smallRow - 1][smallCol - 1] = Piece
    else:
        if (Piece == 'O'):
            pygame.draw.circle(board, (50, 205, 50), (centerX, centerY), 17, 4)
        else:
            pygame.draw.line(board, (50, 205, 50), (centerX - 11, centerY - 11),
                             (centerX + 11, centerY + 11), 8)
            pygame.draw.line(board, (50, 205, 50), (centerX + 11, centerY - 11),
                             (centerX - 11, centerY + 11), 8)


def clickBoard(board):
    global grid, XO, available

    (mouseX, mouseY) = pygame.mouse.get_pos()
    (row, col) = boardPos(mouseX, mouseY)

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

    available = (smallCol, smallRow)

    avGrid = grid[available[1] - 1][available[0] - 1]

    noneCount = 0
    for x, y, z in avGrid:
        if x == None:
            noneCount += 1
        if y == None:
            noneCount += 1
        if z == None:
            noneCount += 1

    if noneCount != 0:
        highlight(board, available[0], available[1])
    else:
        available = None
        resetGrid(board)

    if (XO == "X"):
        XO = "O"
    else:
        XO = "X"


def gameWon(board):
    global grid, winner

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


# --------------------------------------------------------------------
def newGame(board):
    global XO, available, grid, winner, running

    XO = "O"
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


def startGame():

    global running

    pygame.init()
    ttt = pygame.display.set_mode((450, ySize))
    pygame.display.set_caption('Davids 3-i-rad')

    board = initBoard(ttt)

    while running == 1:
        for event in pygame.event.get():
            if event.type is QUIT:
                running = 0
            elif event.type is MOUSEBUTTONDOWN:
                clickBoard(board)

            gameWon(board)

            showBoard(ttt, board)


if __name__ == "__main__":
    startGame()
