import pygame
import sys
import math

pygame.init()
WinX, WinY = 600, 400
SCREEN = pygame.display.set_mode((WinX, WinY))
CLOCK = pygame.time.Clock()
SCREEN.fill((0,0,0))
pygame.display.set_caption("A-star Pathfinder")
run = True
drag = False

# Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PURPLE = (204, 0, 204) # Start Node
BLUE = (0, 0, 255) # End Node
YELLOW = (255, 255, 0) # Final Path nodes
RED = (255, 0, 0) # Analyzed Nodes

# Classes
class Node(object):
    def __init__(self, x, y, barrier=False, start=False, end=False):
        self.x = x
        self.y = y
        self.barrier = barrier
        self.start = start
        self.end = end
        self.fCost = None # gCost + hCost
        self.gCost = None # Distance from Current node
        self.hCost = None # Distance from End node
    
    def setCost(self):
        global endX, endY, current
        self.gCost = int(math.sqrt((self.x - current[0]) ** 2 + (self.y - current[1]) ** 2) * 10)
        self.hCost = int(math.sqrt((endX - current[0]) ** 2 + (endY - current[1]) ** 2) * 10)
        self.fCost = self.gCost + self.hCost

# Variables
nodeSize = 20 # Pixel side length of each grid node.
grid = [[Node(x, y) for x in range(WinX // 20)] for y in range(WinY // 20)]
startX, startY = 24, 3
endX, endY = 3, 17
current = (startX, startY)
analyzed = []
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
    global nodeSize
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

def drawPath():
    for i in path: # i is a tuple
        rect = pygame.Rect(i[0] * nodeSize, i[1] * nodeSize, nodeSize, nodeSize)
        pygame.draw.rect(SCREEN, YELLOW, rect, 0)

def analyze():
    if current[0] = endX and current[1] = endY:
        drawPath()
    else:
        

# PyGame Loop
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
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

    drawGrid()

    pygame.display.update()

if not run:
    pygame.quit()
    sys.exit()