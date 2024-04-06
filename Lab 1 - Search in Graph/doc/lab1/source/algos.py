import pygame
from maze import SearchSpace

def DFS(g: SearchSpace, sc: pygame.Surface):
    print('Implement DFS algorithm')

    open_set = [g.start.id]
    closed_set = []
    father = [-1]*g.get_length()

    raise NotImplementedError('not implemented')

def BFS(g: SearchSpace, sc: pygame.Surface):
    print('Implement BFS algorithm')

    open_set = [g.start.id]
    closed_set = []
    father = [-1]*g.get_length()

    raise NotImplementedError('not implemented')

def UCS(g: SearchSpace, sc: pygame.Surface):
    print('Implement UCS algorithm')

    # +1 respect if you can implement UCS with a priority queue
    open_set = [(0, g.start.id)]
    closed_set = []
    father = [-1]*g.get_length()
    cost = [100_000]*g.get_length()
    cost[g.start.id] = 0

    raise NotImplementedError('not implemented')

def AStar(g: SearchSpace, sc: pygame.Surface):
    print('Implement AStar algorithm')

    # +1 respect if you can implement AStar with a priority queue
    open_set = [(0, g.start.id)]
    closed_set = []
    father = [-1]*g.get_length()
    cost = [100_000]*g.get_length()
    cost[g.start.id] = 0

    raise NotImplementedError('not implemented')
