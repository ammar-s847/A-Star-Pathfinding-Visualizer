import pygame
import io
import numpy as np
import sys

pygame.display.set_caption("A-star Pathfinder")
RUN = True

class Node:

    def __init__(self, x, y, walkable):
        self.x = x
        self.y = y
        self.walkable = walkable

class Grid:

    def __init__(self, rows, cols):
        grid = np.empty([rows, cols], dtype=Node)
        self.cols = cols
        self.rows = rows
        self.radius = 5
        self.unwalkable = []
        self.windowHeight = 20 * self.rows
        self.windowWidth = 20 * self.cols

    def setupGrid(self):
        global SCREEN, CLOCK, RUN
        pygame.init()
        SCREEN = pygame.display.set_mode((self.windowWidth, self.windowHeight))
        CLOCK = pygame.time.Clock()
        SCREEN.fill((0,0,0))

        while RUN:
            self.drawGrid()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

    def drawGrid(self):
        blockSize = 20 #Set the size of the grid block
        for x in range(self.windowWidth):
            for y in range(self.windowHeight):
                rect = pygame.Rect(x*blockSize, y*blockSize,
                                   blockSize, blockSize)
                pygame.draw.rect(SCREEN, (200,200,200), rect, 1)


grid = Grid(25,25)
grid.setupGrid()