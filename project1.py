#genereate grid
import random
import sys
sys.setrecursionlimit(1500)

size = 8
total = size * size
gamegrid = [[0 for i in xrange(size)] for i in xrange(size)]

obstacles = int(total * 0.25)
stars = int(total * 0.2)

#control = ["empty", "wall", "goal", "star", "visited"]
control = [0, 1, 2, 3, 4]

def PlaceObjects(state, num):
    for i in range(num):                                    #For each required instance of the object
        while True:
            ranx = random.randint(0, size-1)                #Selects random square
            rany = random.randint(0, size-1)
            
            if gamegrid[ranx][rany] == 0:                   #Checks if empty
                gamegrid[ranx][rany] = control[state]       #Sets to new state
                break                                       #Breaks out while
    
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
        if grid[row+1][column] == 0 and row+1 <= size:
            return True
        if grid[row-1][column] == 0 and row-1 >= 0:
            return True
        if grid[row][column+1] == 0 and column <= size:
            return True
        if grid[row][column-1] == 0 and column-1 >= 0:
            return True
        return False
    except IndexError:
        return False
    


while True:
    gamegrid = [[0 for i in xrange(size)] for i in xrange(size)]
    
    PlaceObjects(1, obstacles)
    PlaceObjects(2, 1)
    PlaceObjects(3, stars)
    temp = test(gamegrid)
    
    if temp == True:
        break

OutputGrid(gamegrid)