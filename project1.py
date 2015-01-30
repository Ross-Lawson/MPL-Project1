
import os
cwd = os.path.dirname(os.path.realpath(__file__))

import sys
sys.path.append(cwd+'\pygame')
sys.setrecursionlimit(1500)

import pygame
import random

#config vars
gridWidth = 12
gridHeight = 8
bgColour = (255,255,255)

#genereate grid
total = gridWidth * gridHeight

obstacles = int(total * 0.25)
stars = int(total * 0.2)

#control = ["empty", "wall", "goal", "star", "visited"]
control = [0, 1, 2, 3, 4]

def PlaceObjects(state, num):
    for i in range(num):                                    #For each required instance of the object
        while True:
            ranx = random.randint(0, gridWidth-1)			#Selects random square
            rany = random.randint(0, gridHeight-1)           
            
            if gamegrid[rany][ranx] == 0:                   #Checks if empty
                gamegrid[rany][ranx] = control[state]       #Sets to new state
                break                                       #Breaks out while
    
    return

def OutputGrid(grid):
    for row in grid:
        out = ""
        for val in row:
            out = str(out) + " " + str(val)
        print out
	print

def find(grid):
   for row, i in enumerate(grid):
       try:
           column = i.index(2)
       except ValueError:
           continue
       return row, column
   return -1

def test(grid):
    row, column = find(grid)
    
    try:
        if grid[row+1][column] == 0 and row+1 <= gridWidth:
            return True
        if grid[row-1][column] == 0 and row-1 >= 0:
            return True
        if grid[row][column+1] == 0 and column <= gridHeight:
            return True
        if grid[row][column-1] == 0 and column-1 >= 0:
            return True
        return False
    except IndexError:
        return False
    
unsolvable = True
while unsolvable:
	gamegrid = [[0 for i in xrange(gridWidth)] for i in xrange(gridHeight)]

	PlaceObjects(1, obstacles)
	PlaceObjects(2, 1)
	PlaceObjects(3, stars)
	temp = test(gamegrid)

	if temp == True:
		unsolvable = False

OutputGrid(gamegrid)

#Graphical stuff
pygame.init()
gridOutputSize = 32
gridColour = {
	0: (255,255,255),
	1: (0,0,0),
	2: (255,0,0),
	3: (0,255,0)
}
charPos = {
	'x' : 0,
	'y' : 0
}
textures = {
	'char' : pygame.image.load('char.png')
	#'star' : pygame.image.load('star.png')
}
textureRects = {}
for i, img in textures.iteritems():
	textureRects[i] = img.get_rect()

screen = pygame.display.set_mode((gridWidth*gridOutputSize,gridHeight*gridOutputSize))
clock = pygame.time.Clock()

def BufferScreen(grid):
	for y, valy in enumerate(grid):
		for x, valx in enumerate(grid[y]):
			pygame.draw.rect(screen, (0,0,0), (x*gridOutputSize,y*gridOutputSize,gridOutputSize,gridOutputSize),1)
			pygame.draw.rect(screen, gridColour[valx], (x*gridOutputSize+5,y*gridOutputSize+5,gridOutputSize-10,gridOutputSize-10),0)
	screen.blit(textures['char'], [charPos['x'] * gridOutputSize, charPos['y'] * gridOutputSize])
	
def DrawScreen():
	pygame.display.flip()
	
	#catch close-window event (pressing x in the corner)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit(); sys.exit();

while (True):
	msElapsed = clock.tick(30)
	screen.fill(bgColour)
	BufferScreen(gamegrid)
	DrawScreen()
