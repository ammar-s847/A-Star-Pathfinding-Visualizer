import pygame
import io
import sys

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
        self.fCost = None
        self.gCost = None
        self.hCost = None

# Variables
grid = [[Node(x, y) for x in range(WinX // 20)] for y in range(WinY // 20)]
barriers = []
startX, startY = int(), int()
endX, endY = int(), int()
grid[4][5].start = True
grid[14][21].end = True

def setBarrier(x, y):
    global barriers
    x = x // 20
    y = y // 20
    if grid[y][x].start == False and grid[y][x].end == False:
        grid[y][x].barrier = True
    else:
        grid[y][x].barrier = False

def drawGrid():
    nodeSize = 20 # Pixel side length of each grid node.
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