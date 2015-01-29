
import os
cwd = os.path.dirname(os.path.realpath(__file__))

import sys
sys.path.append(cwd+'\pygame')
import pygame

import random

#config vars
gridWidth = 12
gridHeight = 8
bgColour = (255,255,255)

#genereate grid
total = gridWidth * gridHeight
gamegrid = [[4 for i in xrange(gridWidth)] for i in xrange(gridHeight)]

obstacles = int(total * 0.2)
stars = int(total * 0.2)

#control = ["obs", "gol", "str", "ept"]
control = [1, 2, 3, 4]

def PlaceObjects(state, num):
    for i in range(num):                                    #For each required instance of the object
        while True:
            ranx = random.randint(1, gridHeight-1)
            rany = random.randint(1, gridWidth-1)           #Selects random square
            
            if gamegrid[ranx][rany] == 4:                   #Checks if empty
                gamegrid[ranx][rany] = control[state]       #Sets to new state
                break                                       #Breaks out while
    
    return

def OutputGrid(grid):
    for row in grid:
        out = ""
        for val in row:
            out = str(out) + " " + str(val)
        print out
    print  


#OutputGrid(gamegrid)
PlaceObjects(0, obstacles)
PlaceObjects(1, 1)
PlaceObjects(2, stars)
#OutputGrid(gamegrid)

#Graphical stuff
pygame.init()
gridOutputSize = 32
gridColour = {
	1: (0,0,0),
	2: (255,0,0),
	3: (0,255,0),
	4: (255,255,255)
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

print textureRects
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
	charPos['x'] = random.randint(0,gridWidth-1)
	charPos['y'] = random.randint(0,gridHeight-1)
	screen.fill(bgColour)
	BufferScreen(gamegrid)
	DrawScreen()