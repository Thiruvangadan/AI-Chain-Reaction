import random

import pygame
import sys
from math import *

# Initialization of Pygame
pygame.init()

width = 400
height = 400
display = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Colors
background = (0, 0, 0)
border = (255, 255, 255)
red = (231, 76, 60)
white = (244, 246, 247)
violet = (136, 78, 160)


playerColor = [red,violet]

font = pygame.font.SysFont("Times New Roman", 30)

blocks = 100


noPlayers = 2
pygame.display.set_caption("Chain Reaction")

score = []
for i in range(noPlayers):
    score.append(0)

players = []
for i in range(noPlayers):
    players.append(playerColor[i])

d = blocks // 2 - 2

cols = int(width // blocks)
rows = int(height // blocks)

grid = []


def make_move(grid,move):
    r=4
    c=4
    global countt
    countt = 0
    global neighbor_count,neighbors
    neighbors=[]
    neighbor_count=[[None for _ in range(c)] for _ in range(r)]
    for i in range(4):
        for j in range(4):
            neighbor_count[i][j]=-1
    if move <= 1:
        x = random.randint(0, 4 - 1)
        y = random.randint(0, 4 - 1)
        if grid[x][y].color == playerColor[1]:
            getmin(x, y, neighbor_count)
        elif grid[x][y].color == playerColor[0]:
            make_move(grid, move)
        else:
            getmin(x, y, neighbor_count)


    else:
        for i in range(4):
            for j in range(4):
                if grid[i][j].color == playerColor[1]:
                    neighbors=get_neighbors(grid,i,j,neighbor_count)
        max=0
        getmax(max,neighbor_count)



def getmax(max,neighbor_count):
    a = 0
    b = 0
    global countt
    for i in range(4):
        for j in range(4):
            if neighbor_count[i][j] >= max:
                max = neighbor_count[i][j]
                a = i
                b = j

    if countt > 50:
        x= random.randint(0, 4 - 1)
        y = random.randint(0, 4 - 1)
        if grid[x][y].color == playerColor[0]:
            make_move(grid, move)
        else:
            print("AI move :", y, x)
            addAtom(x, y, players[1])
    else:
        getmin(a, b, neighbor_count)





def getmin(a,b,neighbor_count):
    next_move=True
    global countt
    countt +=1
    if a > 0 and grid[a - 1][b].color == playerColor[0] and next_move==True:
        if(grid[a - 1][b].noAtoms-len(grid[a-1][b].neighbors)) > (grid[a][b].noAtoms-len(grid[a][b].neighbors)):
            neighbor_count[a][b]=0
            next_move=False

    if a < 4 - 1 and grid[a + 1][b].color == playerColor[0] and next_move==True:
        if (grid[a + 1][b].noAtoms - len(grid[a + 1][b].neighbors)) > (grid[a][b].noAtoms - len(grid[a][b].neighbors)):
            neighbor_count[a][b] = 0
            next_move = False

    if b > 0 and grid[a][b - 1].color == playerColor[0] and next_move==True:
        if (grid[a][b-1].noAtoms - len(grid[a][b - 1].neighbors)) > (grid[a][b].noAtoms - len(grid[a][b].neighbors)):
            neighbor_count[a][b] = 0
            next_move = False

    if b < 4 - 1 and grid[a][b+1].color == playerColor[0] and next_move==True:
        if (grid[a][b + 1].noAtoms - len(grid[a][b + 1].neighbors)) > (grid[a][b].noAtoms - len(grid[a][b].neighbors)):
            neighbor_count[a][b] = 0
            next_move = False

    if next_move == True:
        print("AI move :", b, a)
        addAtom(a, b, players[1])
    else:
        max=0
        getmax(max,neighbor_count)


def get_neighbors(grid,x,y,neighbor_count):
    global neighbors
    neighbors=[]
    if x> 0 and grid[x-1][y].color ==playerColor[0]:
        neighbors.append((grid[x-1][y],(x-1,y)))
        neighbor_count[x][y] +=1
    if x<4-1 and grid[x+1][y].color ==playerColor[0]:
        neighbors.append((grid[x + 1][y], (x + 1, y)))
        neighbor_count[x][y] +=1
    if y>0 and grid[x][y-1].color ==playerColor[0]:
        neighbors.append((grid[x][y - 1], (x, y - 1)))
        neighbor_count[x][y] +=1
    if y<4-1 and grid[x][y+1].color ==playerColor[0]:
        neighbors.append((grid[x][y + 1], (x, y + 1)))
        neighbor_count[x][y] += 1
    neighbor_count[x][y]+=1
    return neighbor_count,neighbors


# Quit or Close the Game Window
def close():
    pygame.quit()
    sys.exit()


# Class for Each Spot in Grid
class Spot():
    def __init__(self):
        self.color = border
        self.neighbors = []
        self.noAtoms = 0

    def addNeighbors(self, i, j):
        if i > 0:
            self.neighbors.append(grid[i - 1][j])
        if i < rows - 1:
            self.neighbors.append(grid[i + 1][j])
        if j < cols - 1:
            self.neighbors.append(grid[i][j + 1])
        if j > 0:
            self.neighbors.append(grid[i][j - 1])





# Initializing the Grid with "Empty or 0"
def initializeGrid():
    global grid, score, players
    score = []
    for i in range(noPlayers):
        score.append(0)

    players = []
    for i in range(noPlayers):
        players.append(playerColor[i])
    grid = [[] for _ in range(cols)]
    for i in range(cols):
        for j in range(rows):
            newObj = Spot()
            grid[i].append(newObj)
    for i in range(cols):
        for j in range(rows):
            grid[i][j].addNeighbors(i, j)


# Draw the Grid in Pygame Window
def drawGrid(currentIndex):
    r = 0
    c = 0
    for i in range(width // blocks):
        r += blocks
        c += blocks
        pygame.draw.line(display, players[currentIndex], (c, 0), (c, height))
        pygame.draw.line(display, players[currentIndex], (0, r), (width, r))


# Draw the Present Situation of Grid
def showPresentGrid(vibrate=1):
    r = -blocks
    c = -blocks
    padding = 2
    for i in range(cols):
        r += blocks
        c = -blocks
        for j in range(rows):
            c += blocks
            if grid[i][j].noAtoms == 0:
                grid[i][j].color = border
            elif grid[i][j].noAtoms == 1:
                pygame.draw.ellipse(display, grid[i][j].color,
                                    (r + blocks / 2 - d / 2 + vibrate, c + blocks / 2 - d / 2, d, d))
            elif grid[i][j].noAtoms == 2:
                pygame.draw.ellipse(display, grid[i][j].color, (r + 5, c + blocks / 2 - d / 2 - vibrate, d, d))
                pygame.draw.ellipse(display, grid[i][j].color,
                                    (r + d / 2 + blocks / 2 - d / 2 + vibrate, c + blocks / 2 - d / 2, d, d))
            elif grid[i][j].noAtoms == 3:
                angle = 90
                x = r + (d / 2) * cos(radians(angle)) + blocks / 2 - d / 2
                y = c + (d / 2) * sin(radians(angle)) + blocks / 2 - d / 2
                pygame.draw.ellipse(display, grid[i][j].color, (x - vibrate, y, d, d))
                x = r + (d / 2) * cos(radians(angle + 90)) + blocks / 2 - d / 2
                y = c + (d / 2) * sin(radians(angle + 90)) + 5
                pygame.draw.ellipse(display, grid[i][j].color, (x + vibrate, y, d, d))
                x = r + (d / 2) * cos(radians(angle - 90)) + blocks / 2 - d / 2
                y = c + (d / 2) * sin(radians(angle - 90)) + 5
                pygame.draw.ellipse(display, grid[i][j].color, (x - vibrate, y, d, d))

    pygame.display.update()



# Increase the Atom when Clicked
def addAtom(i, j, color):
    grid[i][j].noAtoms += 1
    grid[i][j].color = color
    if grid[i][j].noAtoms >= len(grid[i][j].neighbors):
        overFlow(grid[i][j], color)


# Split the Atom when it Increases the "LIMIT"
def overFlow(cell, color):
    global count
    res = checkWon()
    if res < 9999:
        gameOver(res)
    showPresentGrid()
    cell.noAtoms = 0
    for m in range(len(cell.neighbors)):
        cell.neighbors[m].noAtoms += 1
        cell.neighbors[m].color = color
        if cell.neighbors[m].noAtoms >= len(cell.neighbors[m].neighbors):
            count +=1
            if count > 15:
                isPlayerInGame()
                display.fill(background)
                vibrate = 0
                vibrate *= -1
                if m // 2 == 0:
                    drawGrid(1)
                else:
                    drawGrid(0)
                showPresentGrid(vibrate)
                pygame.display.update()
                res=9999

            overFlow(cell.neighbors[m], color)



# Checking if Any Player has WON!
def isPlayerInGame():
    global score
    playerScore = []
    for i in range(noPlayers):
        playerScore.append(0)
    for i in range(cols):
        for j in range(rows):
            for k in range(noPlayers):
                if grid[i][j].color == playerColor[k]:
                    playerScore[k] += grid[i][j].noAtoms
    score = playerScore[:]

# GAME OVER
def gameOver(playerIndex):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    close()
                if event.key == pygame.K_r:
                    gameLoop()
        if (playerIndex + 1) == 1:
            text = font.render("Player %d Won!" % (playerIndex + 1), True, white)
        else:
            text = font.render("Computer Won!", True, white)
        text2 = font.render("Press \'r\' to Reset!", True, white)

        display.blit(text, (width / 4, height / 3))
        display.blit(text2, (width / 4, height / 2))

        pygame.display.update()
        clock.tick(5)


def checkWon():
    num = 0
    for i in range(noPlayers):
        if score[i] == 0:
            num += 1
    if num == noPlayers-1:
        for i in range(noPlayers):
            if score[i] > 0:
                return i
    return 9999


# Main Loop
def gameLoop():
    initializeGrid()
    global count
    count=0
    loop = True
    global move
    move=1
    turns = 0

    currentPlayer = 0

    vibrate = 0

    while loop:
        if currentPlayer == 1:
            make_move(grid, move)
            move = move + 1
            turns += 1
            currentPlayer += 1
            if currentPlayer >= noPlayers:
                currentPlayer = 0
            if turns >= noPlayers:
                turns = 1
                isPlayerInGame()
            display.fill(background)
            # Vibrate the Atoms in their Cells
            vibrate *= -1

            drawGrid(currentPlayer)
            showPresentGrid(vibrate)

            pygame.display.update()

            res = checkWon()
            if res < 9999:
                gameOver(res)

            clock.tick(5)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    close()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                i = int(x / blocks)
                j = int(y / blocks)
                if grid[i][j].color == players[currentPlayer] or grid[i][j].color == border:
                    turns += 1
                    addAtom(i, j, players[currentPlayer])
                    currentPlayer += 1
                if turns >= noPlayers:
                    turns=1
                    isPlayerInGame()
            display.fill(background)

            # Vibrate the Atoms in their Cells
            vibrate *= -1

            drawGrid(currentPlayer)
            showPresentGrid(vibrate)

            pygame.display.update()

            res = checkWon()
            if res < 9999:
                gameOver(res)
            clock.tick(5)

gameLoop()
