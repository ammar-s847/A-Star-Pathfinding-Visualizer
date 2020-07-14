import pygame
import sys
import math

pygame.init()
WinX, WinY = 600, 400
SCREEN = pygame.display.set_mode((WinX, WinY))
CLOCK = pygame.time.Clock()
SCREEN.fill((0,0,0))
pygame.display.set_caption("A-star Pathfinder")

# Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PURPLE = (204, 0, 204) # Start Node
BLUE = (0, 0, 255) # End Node
YELLOW = (255, 255, 0) # Final Path nodes
RED = (255, 0, 0) # Analyzed Nodes

# Classes
class Node(object):
    def __init__(self, x, y, barrier=False, start=False, end=False, closed=False):
        self.x = x
        self.y = y
        self.barrier = barrier
        self.start = start
        self.end = end
        self.closed = closed
        self.fCost = None # gCost + hCost
        self.gCost = None # Distance from Current node
        self.hCost = None # Distance from End node
    
    def setCost(self):
        global endX, endY, current
        self.gCost = int(math.sqrt((self.x - current[0]) ** 2 + (self.y - current[1]) ** 2) * 10)
        self.hCost = int(math.sqrt((endX - current[0]) ** 2 + (endY - current[1]) ** 2) * 10)
        self.fCost = self.gCost + self.hCost
    
    def setSurrounding(self):
        global closed_nodes, grid
        if self.x > 0 and grid[self.y][self.x - 1].barrier == False:
            closed_nodes.append((self.x - 1, self.y))
        if self.x < len(grid[0]) - 1 and grid[self.y][self.x + 1].barrier == False:
            closed_nodes.append((self.x + 1, self.y))
        if self.y > 0 and grid[self.y - 1][self.x].barrier == False:
            closed_nodes.append((self.x, self.y - 1))
        if self.y < len(grid) - 1 and grid[self.y + 1][self.x].barrier == False:
            closed_nodes.append((self.x, self.y + 1))


# Variables
run = True
drag = False # Detecting Mouse Drag.
algorithm = False # When the SPACE key is presssed and the algorithm has started.
nodeSize = 20 # Pixel side length of each grid node.
grid = [[Node(x, y) for x in range(WinX // 20)] for y in range(WinY // 20)]
startX, startY = 24, 3
endX, endY = 3, 17
current = (startX, startY)
closed_nodes = [] # nodes already evaluated.
open_nodes = [] # nodes about to be evaluated.
path = [] # x, y pairs of nodes that belong to the shortest path.
grid[startY][startX].start = True
grid[endY][endX].end = True
grid[startY][startX].setCost()
print(grid[startY][startX].fCost)

# Functions
def setBarrier(x, y):
    x = x // 20
    y = y // 20
    if grid[y][x].start == False and grid[y][x].end == False:
        grid[y][x].barrier = True
    else:
        grid[y][x].barrier = False

def drawGrid():
    global nodeSize, startX, startY, endX, endY
    for n in grid:
        for Node in n:
            if Node.barrier == False:
                rect = pygame.Rect(Node.x * nodeSize, Node.y * nodeSize, nodeSize, nodeSize)
                pygame.draw.rect(SCREEN, WHITE, rect, 1)
                if Node.start == True:
                    rect = pygame.Rect(Node.x * nodeSize, Node.y * nodeSize, nodeSize, nodeSize)
                    pygame.draw.rect(SCREEN, PURPLE, rect, 0)
                    startX, startY = Node.x, Node.y
                elif Node.end == True:
                    rect = pygame.Rect(Node.x * nodeSize, Node.y * nodeSize, nodeSize, nodeSize)
                    pygame.draw.rect(SCREEN, BLUE, rect, 0)
                    endX, endY = Node.x, Node.y
            elif Node.barrier == True:
                rect = pygame.Rect(Node.x * nodeSize, Node.y * nodeSize, nodeSize, nodeSize)
                pygame.draw.rect(SCREEN, WHITE, rect, 0)
    for i in closed_nodes:
        rect = pygame.Rect(i[0] * nodeSize, i[1] * nodeSize, nodeSize, nodeSize)
        pygame.draw.rect(SCREEN, RED, rect, 0)

def drawPath():
    global nodeSize
    for i in path: # i is a tuple
        rect = pygame.Rect(i[0] * nodeSize, i[1] * nodeSize, nodeSize, nodeSize)
        pygame.draw.rect(SCREEN, YELLOW, rect, 0)

def analyze():
    global current
    if current[0] == endX and current[1] == endY:
        drawPath()
    else:
        print("analyzing")
        grid[current[1]][current[0]].setSurrounding()
        pygame.time.delay(150)

# PyGame Loop
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_SPACE: # Press "SPACE" key to start the Algorithm.
                algorithm = True
        #elif event.type == pygame.KEYDOWN: 
            #if event.key == pygame.K_r: # Press "R" key to restart the program.
                #grid = [[Node(x, y) for x in range(WinX // 20)] for y in range(WinY // 20)]
        elif event.type == pygame.MOUSEBUTTONDOWN: # Drag mouse while holding left click to add barriers.
            if event.button == 1:            
                drag = True
                mouseX, mouseY = event.pos
                setBarrier(mouseX, mouseY)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:            
                drag = False
        elif event.type == pygame.MOUSEMOTION:
            if drag:
                mouseX, mouseY = event.pos
                setBarrier(mouseX, mouseY)

    if algorithm:
        analyze()
    drawGrid()
    pygame.display.update()

if not run:
    pygame.quit()
    sys.exit()