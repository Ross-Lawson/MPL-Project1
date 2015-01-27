#genereate grid
import random

size = 8
total = size * size
gamegrid = [[4 for i in xrange(size)] for i in xrange(size)]

obstacles = int(total * 0.2)
stars = int(total * 0.2)

#control = ["obs", "gol", "str", "ept"]
control = [1, 2, 3, 4]

def PlaceObjects(state, num):
    for i in range(num):                                    #For each required instance of the object
        while True:
            ranx = random.randint(1, size-1)                #Selects random square
            rany = random.randint(1, size-1)
            
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

OutputGrid(gamegrid)








