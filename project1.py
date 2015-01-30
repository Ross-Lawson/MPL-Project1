from __future__ import division

import os
cwd = os.path.dirname(os.path.realpath(__file__))

import sys
sys.path.append(cwd+'\pygame')
sys.setrecursionlimit(1500)

import pygame
import random
import math

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
gridOutputSize = 32 # the pixel size of each square
gridColour = { # default colours for square types that do not have textures
	0: (255,255,255), # empty
	1: (0,0,0), # obstacle
	2: (255,0,0), # goal
	3: (0,255,0) # star
}
charPos = { # character position, in squares, 0,0 is the top left square, 1,0 is one square right from the top left etc.
	'x' : 0,
	'y' : 0
}
textures = { # texture definitions
	'char' : pygame.image.load('char.png'),
	'grass' : pygame.image.load('grass.png'), # square background
	1 : pygame.image.load('rock.png'), # obstacle
	2 : pygame.image.load('heart.png'), # goal
	3 : pygame.image.load('star.png') # star
}
textureRects = {}
for i, img in textures.iteritems():
	textureRects[i] = img.get_rect()
print textureRects

screen = pygame.display.set_mode((gridWidth*gridOutputSize,gridHeight*gridOutputSize))
clock = pygame.time.Clock()
frame = 1 # sprite-frame counter, defined which area of the sprite to draw
animationSpeed = 2 # lower is faster

def BufferScreen(grid):
	global frame
	realFrame = math.ceil(frame/animationSpeed) # repeat the same sprite position for animSpeed times
	spritePos = pygame.Rect((realFrame-1)%4*gridOutputSize,(math.ceil(realFrame/4)-1)*gridOutputSize,gridOutputSize,gridOutputSize) # define the rect position of the current frame being displayed
	for y, valy in enumerate(grid): # loop the rows
		for x, valx in enumerate(grid[y]): # loop the columns
			screen.blit(textures['grass'], [x * gridOutputSize, y * gridOutputSize])
			if valx in textures: # if this square's content has a texture, draw it
				if textureRects[valx].width == 128 and textureRects[valx].height == 64:
					screen.blit(textures[valx], [x * gridOutputSize, y * gridOutputSize], spritePos)
				else:
					screen.blit(textures[valx], [x * gridOutputSize, y * gridOutputSize])
	screen.blit(textures['char'], [charPos['x'] * gridOutputSize, charPos['y'] * gridOutputSize]) # draw the character
	frame = frame + 1 # increment sprite-frame counter
	if frame > 8*animationSpeed: # reset the sprite-frame counter if it's greater than 8
		frame = 1
	
def DrawScreen():
	pygame.display.flip() # render the buffer
	#catch close-window event (pressing x in the corner)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit(); sys.exit();

while (True): # endless loop to redraw the screen
	msElapsed = clock.tick(30) # define the fps the game should try to run at
	screen.fill(bgColour) # empty the screen
	BufferScreen(gamegrid) # buffer everything to be drawn
	DrawScreen() # draw them
