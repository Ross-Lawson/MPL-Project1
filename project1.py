from __future__ import division
import random
import math

import sys
sys.path.insert(0, '/usr/lib/python2.7/dist-packages/') # linux fix, install pygame with apt-get install python-pygame and it sould work
import pygame

#config vars
gridWidth = 12
gridHeight = 8
total = gridHeight * gridWidth
squareRenderSize = 64 # the pixel size of each square
animationSpeed = 2 # lower is faster
bgColour = (255,255,255)

obstacles = int(total * 0.25)
stars = int(total * 0.2)

#control = ["empty", "wall", "goal", "star", "visited"]
control = [0, 1, 2, 3, 4]

def PlaceObjects(state, num, grid):
    for i in range(num):                                    #For each required instance of the object
        while True:
            ranx = random.randint(0, gridWidth-1)           #Selects random square
            rany = random.randint(0, gridHeight-1)          
            
            if grid[rany][ranx] == 0:                   #Checks if empty
                grid[rany][ranx] = control[state]       #Sets to new state
                break                                       #Breaks out while loop
    return

def OutputGrid(grid):
    for row in grid:
        out = ""
        for val in row:
            out = str(out) + " " + str(val)
        print out

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
        if grid[row+1][column] == 0 and row+1 <= gridHeight:
            return True
        if grid[row-1][column] == 0 and row-1 >= 0:
            return True
        if grid[row][column+1] == 0 and column <= gridWidth:
            return True
        if grid[row][column-1] == 0 and column-1 >= 0:
            return True
        return False
    except IndexError:
        return False
   
def generateLevel():
	while True:
		gamegrid = [[0 for i in xrange(gridWidth)] for i in xrange(gridHeight)]

		PlaceObjects(1, obstacles, gamegrid)
		PlaceObjects(2, 1, gamegrid)
		PlaceObjects(3, stars, gamegrid)
		temp = test(gamegrid)

		if temp == True:
			return gamegrid
			break

gamegrid = None # just initialising the variable

#Graphical stuff
pygame.init()
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
status = {
	'mode' : 'startscreen',
	'level' : 0,
	'score' : 0,
	'timeLeft' : 30000, # milliseconds
	'timeStart' : 0
}
textures = { # texture definitions, they must be either 32x32 or 128x64 (8x 32x32 images that will be animated)
	'start' : pygame.image.load('start.png'),
	'cut' : pygame.image.load('cut.png'),
	'char' : pygame.image.load('char.png'),
	'grass' : pygame.image.load('grass.png'), # square background
	1 : pygame.image.load('rock.png'), # obstacle
	2 : pygame.image.load('heart.png'), # goal
	3 : pygame.image.load('star.png') # star
}
textureRects = {} # store texture dimensions into a variable
for i, img in textures.iteritems():
	textureRects[i] = img.get_rect() # store the dimensions
if squareRenderSize != 32: # scale textures if render scale is not the native 32px/square
	renderScale = squareRenderSize/32 # store the scale
	for i, rect in textureRects.iteritems():
		scaledTexture = pygame.transform.scale(textures[i], (int(textureRects[i].width * renderScale), int(textureRects[i].height * renderScale))) # rescale the image
		textures[i] = scaledTexture # save the rescaled image
		textureRects[i].width = textureRects[i].width * renderScale # update the rect width to reflect new scale
		textureRects[i].height = textureRects[i].height * renderScale # update the rect height to reflect new scale


screen = pygame.display.set_mode((gridWidth*squareRenderSize,(gridHeight+1)*squareRenderSize)) # initialise the window
clock = pygame.time.Clock()
fontSize = int(round(squareRenderSize*0.6))
font = pygame.font.Font(None, fontSize)
divider = int(round(squareRenderSize*0.1))
pygame.key.set_repeat(1, 250)
frame = 1 # sprite-frame counter, defined which area of the sprite to draw

def BufferScreen(grid):
	global frame
	if status['mode'] == "startscreen":
		titleText = font.render("Welcome to StarCollector!", True, (0,0,0))
		infoText = font.render("Collect stars, get to the heart", True, (0,0,0))
		controlText = font.render("Use wasd keys to move", True, (0,0,0))
		
		screen.blit(titleText, [gridWidth / 2 * squareRenderSize - titleText.get_width() / 2, 1 * squareRenderSize])
		screen.blit(infoText, [gridWidth / 2 * squareRenderSize - infoText.get_width() / 2, 1 * squareRenderSize + fontSize])
		screen.blit(controlText, [gridWidth / 2 * squareRenderSize - controlText.get_width() / 2, 1 * squareRenderSize + fontSize * 2])
		screen.blit(textures['start'], [gridWidth / 2 * squareRenderSize - textures['start'].get_width() / 2, (gridHeight + 1) / 2 * squareRenderSize - textures['start'].get_height() / 2]) # draw the start button
	elif status['mode'] == "game":
		realFrame = math.ceil(frame/animationSpeed) # repeat the same sprite position for animSpeed times
		spritePos = pygame.Rect((realFrame-1)%4*squareRenderSize,(math.ceil(realFrame/4)-1)*squareRenderSize,squareRenderSize,squareRenderSize) # define the rect position of the current frame being displayed
		for y, valy in enumerate(grid): # loop the rows
			for x, valx in enumerate(grid[y]): # loop the columns
				screen.blit(textures['grass'], [x * squareRenderSize, y * squareRenderSize])
				if valx in textures: # if this square's content has a texture, draw it
					if textureRects[valx].width == 4*squareRenderSize and textureRects[valx].height == 2*squareRenderSize: # if the texture is an animated one
						screen.blit(textures[valx], [x * squareRenderSize, y * squareRenderSize], spritePos)
					else: # or a static one
						screen.blit(textures[valx], [x * squareRenderSize, y * squareRenderSize])
		screen.blit(textures['char'], [charPos['x'] * squareRenderSize, charPos['y'] * squareRenderSize], spritePos) # draw the character
		
		#draw the UI
		for x in range(gridWidth):
			screen.blit(textures['cut'], [x * squareRenderSize, gridHeight * squareRenderSize])
		uiTex = {
			'test' : font.render("Level: {}".format(status['level']), True, (0,0,0)),
			'time' : font.render("Time left: {}".format(status['timeLeft']), True, (0,0,0)),
			'score' : font.render("Score: {}".format(status['score']), True, (0,0,0))
		}
		screen.blit(uiTex['test'], [divider, gridHeight * squareRenderSize + divider * 3])
		screen.blit(uiTex['time'], [gridWidth / 2 * squareRenderSize - uiTex['time'].get_width() / 2, gridHeight * squareRenderSize + divider * 3])
		screen.blit(uiTex['score'], [gridWidth * squareRenderSize - uiTex['score'].get_width() - divider, gridHeight * squareRenderSize + divider * 3])
		
		frame = frame + 1 # increment sprite-frame counter
		if frame > 8 * animationSpeed: # reset the sprite-frame counter if it's greater than 8
			frame = 1
	elif status['mode'] == "gameover":
		statusText = font.render("Game Over", True, (0,0,0))
		levelText = font.render("Final level: {}".format(status['level']), True, (0,0,0))
		scoreText = font.render("Final score: {}".format(status['score']), True, (0,0,0))
		
		screen.blit(textures['start'], [gridWidth / 2 * squareRenderSize - textures['start'].get_width() / 2, (gridHeight + 1) / 2 * squareRenderSize - textures['start'].get_height() / 2]) # draw the start button
		screen.blit(statusText, [gridWidth / 2 * squareRenderSize - statusText.get_width() / 2, (gridHeight + 1) / 2 * squareRenderSize - textures['start'].get_height() / 2 - fontSize])
		screen.blit(levelText, [gridWidth / 2 * squareRenderSize - levelText.get_width() / 2, (gridHeight + 1) / 2 * squareRenderSize + textures['start'].get_height() / 2 + fontSize])
		screen.blit(scoreText, [gridWidth / 2 * squareRenderSize - scoreText.get_width() / 2, (gridHeight + 1) / 2 * squareRenderSize + textures['start'].get_height() / 2 + fontSize * 2])
		
def GameLogic(): # do everything regarding game logic, events, collecting start etc here
	global gamegrid, charPos
	beforeCoords = {'x' : charPos['x'], 'y' : charPos['y']}
	for event in pygame.event.get(): # events
		if status['mode'] == "startscreen" or status['mode'] == "gameover":
			if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
				if event.pos[0] > gridWidth / 2 * squareRenderSize - textures['start'].get_width() / 2 and event.pos[0] < gridWidth / 2 * squareRenderSize + textures['start'].get_width() / 2 and event.pos[1] > (gridHeight + 1) / 2 * squareRenderSize - textures['start'].get_height() / 2 and event.pos[1] < (gridHeight + 1) / 2 * squareRenderSize + textures['start'].get_height() / 2:
					StartGame()
		elif status['mode'] == "game":
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_w:
					charPos['y'] -= 1
				elif event.key == pygame.K_a:
					charPos['x'] -= 1
				elif event.key == pygame.K_s:
					charPos['y'] += 1
				elif event.key == pygame.K_d:
					charPos['x'] += 1

				if charPos['x'] < 0:
					charPos['x'] = 0
				elif charPos['x'] > gridWidth-1:
					charPos['x'] = gridWidth-1
				if charPos['y'] < 0:
					charPos['y'] = 0
				elif charPos['y'] > gridHeight-1:
					charPos['y'] = gridHeight-1
				
		#catch close-window event (pressing x in the corner)
		if event.type == pygame.QUIT:
			pygame.quit(); sys.exit();
	
	#game logic here
	
	if status['mode'] == "game":
		currentTime = pygame.time.get_ticks() # this frame's tick time
		levelTime = currentTime - status['timeStart'] # time spent on current level
		status['timeLeft'] = 30 - int(math.ceil(levelTime/1000))
		if levelTime > 30000: # time's our
			GameOver()
		currentTile = gamegrid[charPos['y']][charPos['x']]
		if currentTile != 0:
			if currentTile == 3: # it's a star
				status['score'] += 1
				gamegrid[charPos['y']][charPos['x']] = 0
			elif currentTile == 1: # it's a rock
				charPos = beforeCoords
			elif currentTile == 2: # it's the goal
				gamegrid = generateLevel()
				status['level'] += 1
				status['timeStart'] = pygame.time.get_ticks()
	
def DrawScreen():
	pygame.display.flip() # render the buffer

def GameOver():
	status['mode'] = "gameover"

def StartGame():
	global gamegrid
	gamegrid = generateLevel()
	status['level'] = 1
	status['score'] = 0
	status['mode'] = "game"
	status['timeStart'] = pygame.time.get_ticks()

while (True): # endless loop to redraw the screen
	msElapsed = clock.tick(30) # define the fps the game should try to run at
	screen.fill(bgColour) # empty the screen
	GameLogic() # everything related to game logic
	BufferScreen(gamegrid) # buffer everything to be drawn
	DrawScreen() # draw them
