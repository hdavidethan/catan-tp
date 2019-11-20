from catan import *
import math

# Creates a list representing a hexagonal grid given axial dimensions r x q.
def generateAxialList(r, q):
    result = [[None] * q for _ in range(r)]
    halfPoint = (r + 1) // 2
    for i in range(halfPoint):
        gap = halfPoint - 1 - i
        end = gap - 1
        for j in range(q-1, end, -1):
            result[i][j] = Tile(i, j)
    for i in range(halfPoint, r):
        gap = i - halfPoint + 1
        end = q - gap
        for j in range(end):
            result[i][j] = Tile(i, j)
    return result

# Counts the number of hexes in each side of the board.
def sideCount(r, q):
    rCount = math.ceil(r/2)
    qCount = math.ceil(q/2)
    return rCount, qCount

# Calculates the sum of positive integers to n.
def sumToN(n):
    return n * (n + 1) / 2

# Counts the number of hexes in a board with axial dimensions r x q.
def hexCount(r, q):
    n = r - r // 2 - 1
    return int(r * q - sumToN(n) * 2)

# Check if tuple position is adjacent to tuple position on the board.
# e.g. areAdjacent((2,2), (2, 3)) == True
def areAdjacent(referencePos, checkPos, r=5, q=5):
    row1, col1 = referencePos
    row2, col2 = checkPos
    if ((row1 < 0 or row1 >= r) or (row2 < 0 or row2 >= r) or (col1 < 0 or 
        col1 >= q) or (col2 < 0) or (col2 >= q)):
        return False
    elif (row1 == row2):
        return (abs(col2 - col1) == 1)
    elif (row1 - row2 == 1):
        return (col2 == col1) or (col1 + 1 == col2)
    elif (row2 - row1 == 1):
        return (col2 == col1) or (col1 - 1 == col2)
    else:
        return False

# Returns adjacent hex in direction and its edge index in the adjacency
def getAdjacencyInDirection(referencePos, direction, r=5, q=5):
    row, col = referencePos
    dirs = [(0, -1), (1, -1), (1, 0), (0, +1), (-1, +1), (-1, 0)]
    relativeCol, relativeRow = dirs[direction]
    newRow, newCol = row + relativeRow, col + relativeCol

    # Only returns a value if there exists a hex in specified direction
    if (newRow < r and newCol < q and newRow >= 0 and newCol >= 0 and
        generateAxialList(r, q)[newRow][newCol] != None):
        return (newRow, newCol), (direction + 3) % 6