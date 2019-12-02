import copy

lst = [
    [1, 1, 1, 1, 0],
    [0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0],
    [1, 1, 1, 1, 1],
    [0, 0, 0, 0, 1]
]
#      (r, c)
# src: (0, 0)
# dst: (3, 0)
# shortest path: 5

def dijkstra(lst, src, dst):
    height, width = len(lst), len(lst[0])
    distances = [[float("INF")]*width for i in range(height)]
    sy, sx = src
    distances[sy][sx] = 0
    val = rDijkstra(lst, src, dst, distances, [src])
    return val

def rDijkstra(lst, src, dst, distances, path):
    height, width = len(lst), len(lst[0])
    dy = [-1, 0, 1, 0]
    dx = [0, 1, 0, -1]
    sy, sx = src
    dsy, dsx = dst
    bestPath = path
    bestDistance = distances[dsy][dsx]
    for i in range(4):
        x = sx + dx[i]
        y = sy + dy[i]
        if 0 <= x < width and 0 <= y < height and lst[y][x] == 1:
            if 1+distances[sy][sx] < distances[y][x]:
                distances[y][x] = 1+distances[sy][sx]
                tmpDistance, tmpPath = rDijkstra(lst, (y, x), dst, distances, path + [(y, x)])
                if tmpDistance < bestDistance:
                    bestDistance = tmpDistance
                    bestPath = tmpPath
    return bestDistance, bestPath

ans = dijkstra(lst, (0, 0), (3, 0))
print("Ans", ans)

from resources.game.board import Board
from resources.game.node import Node

b = Board()

def dijkstraRoads(board, start, dest):
    inf = float('inf')
    distances = {node.id: inf for node in board.nodes}
    distances[start.id] = 0
    bestDistance, bestPath = recursiveDijkstra(board, start, dest, distances, [start.id])
    return bestPath

def recursiveDijkstra(board, start, dest, distances, path):
    adjacentNodes = start.getAdjacentNodes(board)
    bestDistance = distances[dest.id]
    bestPath = path
    for node in adjacentNodes:
        road = node.getRoadBetweenNodes(start, board)
        print(node, road)
        if (road.road == None):
            if (1+distances[start.id] < distances[node.id]):
                distances[node.id] = 1+distances[start.id]
                tmpDistance, tmpPath = recursiveDijkstra(board, node, dest, distances, path+[node.id])
                if (tmpDistance < bestDistance):
                    bestDistance = tmpDistance
                    bestPath = tmpPath
    return bestDistance, bestPath

ans = dijkstraRoads(b, Node(1), Node(34))

print(ans)