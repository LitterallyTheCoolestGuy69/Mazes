from copy import deepcopy
import random

def saveMaze(maze, fileName):
    with open(fileName, 'w') as file:
        for row in maze:
            file.write(''.join(row)+'\n')

def loadMaze(fileName):
    with open(fileName) as file:
        return [[char for char in line.strip()] for line in file]

def blankMaze(size):
    maze = []
    if size % 2 == 0:
        size += 1
    for row in range(size):
        currRow = []
        for col in range(size):
            currRow.append('#' if row%2==0 or col%2==0 else ' ')
        maze.append(currRow)
    return maze

def printMaze(maze):
    for row in maze:
        for col in row:
            print(col, end=' ')
        print()
    print()

def printPath(maze, path):
    maze2 = deepcopy(maze)
    for index in range(len(path) - 1):
        cell = path[index]
        nextCell = path[index + 1]
        if nextCell[0] == cell[0] - 2:
            maze2[cell[0]][cell[1]] = '^'
            maze2[cell[0]-1][cell[1]] = '^'
        elif nextCell[1] == cell[1] - 2:
            maze2[cell[0]][cell[1]] = '<'
            maze2[cell[0]][cell[1]-1] = '<'
        elif nextCell[0] == cell[0] + 2:
            maze2[cell[0]][cell[1]] = 'v'
            maze2[cell[0]+1][cell[1]] = 'v'
        elif nextCell[1] == cell[1] + 2:
            maze2[cell[0]][cell[1]] = '>'
            maze2[cell[0]][cell[1]+1] = '>'
    lastCell = path[-1]
    maze2[lastCell[0]][lastCell[1]] = 'x'

    printMaze(maze2)

def getNeighbors(cell, mazeVisited):
    neighbors = [False,False,False,False]
    cellX = cell[1]
    cellY = cell[0]
    if cellX > 2:
        neighbors[0] = mazeVisited[cellY][cellX-2] != '*'
    if cellY > 2:
        neighbors[1] = mazeVisited[cellY-2][cellX] != '*'
    if cellX < len(mazeVisited)-2:
        neighbors[2] = mazeVisited[cellY][cellX+2] != '*'
    if cellY < len(mazeVisited)-2:
        neighbors[3] = mazeVisited[cellY+2][cellX] != '*'
    return neighbors

def dfMazeGen(maze,mazeVisited,cells):
    ##input()
    ##printMaze(maze)
    if len(cells) <= 0:
        return True
    cell = cells[-1]
    mazeVisited[cell[0]][cell[1]] = '*'
    neighbors = getNeighbors(cell, mazeVisited)
    if any(neighbors):
        dir = random.randint(0,100)
        if dir < 40:    dir = 0 ##left
        elif dir < 50:  dir = 1 ##up
        elif dir < 90:  dir = 2 ##right
        else:           dir = 3 ##down
        while not neighbors[dir]:
            dir = random.randint(0, 100)
            if dir < 40:    dir = 0
            elif dir < 50:  dir = 1
            elif dir < 90:  dir = 2
            else:   dir = 3
        if dir == 0:
            cell = (cell[0],cell[1]-2)
            maze[cell[0]][cell[1]+1] = ' '
        elif dir == 1:
            cell = (cell[0]-2, cell[1])
            maze[cell[0]+1][cell[1]] = ' '
        elif dir == 2:
            cell = (cell[0],cell[1]+2)
            maze[cell[0]][cell[1] - 1] = ' '
        else:
            cell = (cell[0]+2, cell[1])
            maze[cell[0] - 1][cell[1]] = ' '
        cells.append(cell)
        return dfMazeGen(maze,mazeVisited,cells)
    cells.pop()
    return dfMazeGen(maze,mazeVisited,cells)
#GENERATION ^^^

#SOLVING vvv
def dfMazeSolve(maze, mazeVisited, cells, finish):
    if len(cells) <= 0:
        return False
    cell = cells[-1]
    mazeVisited[cell[0]][cell[1]] = '*'
    if cell == finish:
        return cells
    neighbors = getNeighbors(cell, mazeVisited)
    if neighbors[0] and maze[cell[0]][cell[1] - 1] != '#':
        cell = (cell[0], cell[1] - 2)
        cells.append(cell)
        return dfMazeSolve(maze, mazeVisited, cells, finish)
    elif neighbors[1] and maze[cell[0] - 1][cell[1]] != '#':
        cell = (cell[0] - 2, cell[1])
        cells.append(cell)
        return dfMazeSolve(maze, mazeVisited, cells, finish)
    elif neighbors[2] and maze[cell[0]][cell[1] + 1] != '#':
        cell = (cell[0], cell[1] + 2)
        cells.append(cell)
        return dfMazeSolve(maze, mazeVisited, cells, finish)
    elif neighbors[3] and maze[cell[0] + 1][cell[1]] != '#':
        cell = (cell[0] + 2, cell[1])
        cells.append(cell)
        return dfMazeSolve(maze, mazeVisited, cells, finish)

    cells.pop()
    return dfMazeSolve(maze, mazeVisited, cells, finish)






mazeSize = 41
maze = blankMaze(mazeSize)
dfMazeGen(maze, deepcopy(maze), [(1,1)])
saveMaze(maze,'testMaze.txt')
printMaze(loadMaze('testMaze.txt'))

finish = (mazeSize - 2, mazeSize - 2)
path = dfMazeSolve(maze, deepcopy(maze), [(1,1)], finish)

printPath(maze, path)


