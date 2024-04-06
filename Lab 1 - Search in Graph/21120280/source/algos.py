from math import sqrt, ceil
from time import process_time
import pygame
from const import *
from maze import SearchSpace, Node

def DFS(g: SearchSpace, sc: pygame.Surface):
    print('Implement DFS algorithm')
    stack = [g.start]
    closed_set = []

    father = [-1] * g.get_length()

    while stack:
        node = stack.pop()
        node.set_color(YELLOW, sc)
        if node == g.goal:
            break

        closed_set.append(node)

        for next_node in g.get_neighbors(node):
            if father[next_node.id] == -1 and next_node not in closed_set:
                next_node.set_color(RED, sc)
                stack.append(next_node)
                father[next_node.id] = node.id

        node.set_color(BLUE, sc)
        
    if g.is_goal(node):
        g.start.set_color(ORANGE, sc)
        g.goal.set_color(PURPLE, sc)

        path_cost = 0
        while father[node.id] != -1:
            pygame.draw.line(sc, WHITE, (node.rect.centerx, node.rect.centery),
                            (g.grid_cells[father[node.id]].rect.centerx, g.grid_cells[father[node.id]].rect.centery),
                            3)
            path_cost += distance_between(node, g.grid_cells[father[node.id]])
            pygame.time.delay(100)
            pygame.display.flip()
            node = g.grid_cells[father[node.id]]
        print("Path cost:", path_cost)
    else:
        print("No path found")
def BFS(g: SearchSpace, sc: pygame.Surface):
    print('Implement BFS algorithm')
    open_set = [g.start]
    closed_set = []

    father = [-1] * g.get_length()

    while open_set:
        node = open_set.pop(0)

        node.set_color(YELLOW, sc)
        if node == g.goal:
            break

        closed_set.append(node)

        for next_node in g.get_neighbors(node):
            if father[next_node.id] == -1 and next_node not in closed_set:
                next_node.set_color(RED, sc)
                open_set.append(next_node)
                father[next_node.id] = node.id

        node.set_color(BLUE, sc)
    if g.is_goal(node):
        g.start.set_color(ORANGE, sc)
        g.goal.set_color(PURPLE, sc)

        path_cost = 0
        while father[node.id] != -1:
            pygame.draw.line(sc, WHITE, (node.rect.centerx, node.rect.centery),
                            (g.grid_cells[father[node.id]].rect.centerx, g.grid_cells[father[node.id]].rect.centery), 3)
            path_cost += distance_between(node, g.grid_cells[father[node.id]])
            pygame.time.delay(100)
            pygame.display.flip()
            node = g.grid_cells[father[node.id]]
        print("Path cost:", path_cost)
    else:
        print("No path found")

def UCS(g: SearchSpace, sc: pygame.Surface):
    print('Implement UCS algorithm')
    open_set = [(0, g.start.id)]
    closed_set = set()
    father = [-1] * g.get_length()
    
    cost = [100_000] * g.get_length()
    cost[g.start.id] = 0
    
    while open_set:
        
        open_set.sort(key=lambda x: x[0])  # Sort the open_set by cost

        node_cost, node_id = open_set.pop(0)
        node = g.grid_cells[node_id]
        
        node.set_color(YELLOW, sc)

        if g.is_goal(node):
            break
        if node in closed_set:
            continue
        closed_set.add(node)

        for next_node in g.get_neighbors(node):
            if next_node not in closed_set:
                tentative_cost = node_cost + distance_between(node, next_node)

                if tentative_cost < cost[next_node.id]:
                    # If the node is not in the open set, add it to the open set and update its cost and father node
                    if(next_node.id not in [x[1] for x in open_set]):
                        open_set.append((tentative_cost, next_node.id))

                    
                    # If the node is in the open set, update its cost and father node if the new cost is lower
                    elif tentative_cost < [x[0] for x in open_set if x[1] == next_node.id][0]:
                        for i, (cost_value, node_id_s) in enumerate(open_set):
                            if node_id_s == next_node.id:
                                open_set[i] = (tentative_cost, next_node.id)
                                break
                    else:
                        continue
                    next_node.set_color(RED, sc)
                    father[next_node.id] = node.id
                    cost[next_node.id] = tentative_cost

        node.set_color(BLUE, sc)
    if g.is_goal(node):
        g.start.set_color(ORANGE, sc)
        g.goal.set_color(PURPLE, sc)

        path_cost = 0
        while father[node.id] != -1:
            pygame.draw.line(sc, WHITE, (node.rect.centerx, node.rect.centery),
                             (g.grid_cells[father[node.id]].rect.centerx, g.grid_cells[father[node.id]].rect.centery), 3)
            path_cost += distance_between(node, g.grid_cells[father[node.id]])
            pygame.time.delay(100)
            pygame.display.update()
            node = g.grid_cells[father[node.id]]
        print("Path cost:", path_cost)
    else:
        print("No path found")

def AStar(g: SearchSpace, sc: pygame.Surface):
    print('Implement AStar algorithm')

    open_set = [(0, g.start.id)]
    closed_set = set()
    father = [-1] * g.get_length()
    cost = [100_000] * g.get_length()
    cost[g.start.id] = 0


    while open_set:
        open_set.sort(key=lambda x: x[0])  # Sort the open_set by cost
    
        node_cost, node_id = open_set.pop(0)
        node = g.grid_cells[node_id]
        node.set_color(YELLOW, sc)

        if g.is_goal(node):
            break

        if node in closed_set:
            continue

        closed_set.add(node)

        for next_node in g.get_neighbors(node):
            if next_node in closed_set:
                continue
            else:
                g_cost = cost[node.id] + distance_between(node, next_node)
                h_cost = combined_heuristic(next_node, g.goal)
                f_cost = g_cost + h_cost

                # If the node is not in the open set, add it to the open set and update its cost and father node 
                if(next_node.id not in [x[1] for x in open_set]):
                    open_set.append((f_cost, next_node.id))
                
                # If the node is in the open set, update its cost and father node if the new cost is lower
                elif f_cost < [x[0] for x in open_set if x[1] == next_node.id][0]:
                    for i, (cost_value, node_id_s) in enumerate(open_set):
                        if node_id_s == next_node.id:
                            open_set[i] = (f_cost, next_node.id)
                            break
                else:
                    continue

                next_node.set_color(RED, sc)
                father[next_node.id] = node.id
                cost[next_node.id] = g_cost


        node.set_color(BLUE, sc)
    if g.is_goal(node):
        g.start.set_color(ORANGE, sc)
        g.goal.set_color(PURPLE, sc)

        path_cost = 0
        while father[node.id] != -1:
            pygame.draw.line(sc, WHITE, (node.rect.centerx, node.rect.centery),
                             (g.grid_cells[father[node.id]].rect.centerx, g.grid_cells[father[node.id]].rect.centery), 3)
            path_cost += distance_between(node, g.grid_cells[father[node.id]])
            pygame.time.delay(100)
            pygame.display.update()
            node = g.grid_cells[father[node.id]]
        print("Path cost:", path_cost)
    else:
        print("No path found")

def distance_between(a:Node, b:Node):
    return sqrt((a.rect.centerx - b.rect.centerx)**2 + (a.rect.centery - b.rect.centery)**2)

# Calculates the Euclidean distance
def euclidean_distance(node: Node, goal: Node):
    dx = node.rect.centerx - goal.rect.centerx
    dy = node.rect.centery - goal.rect.centery
    return sqrt(dx * dx + dy * dy)

# Calculates the Manhattan distance with obstacles
# obstacle_cost is the cost of moving through an obstacle 
# obstacle_cost depends on your specific problem and how you want to prioritize obstacle avoidance
# low obstacle_cost (close to 1), it indicates that the algorithm doesn't strongly penalize moving through obstacles
def manhattan_distance_with_obstacles(node: Node, goal: Node, obstacle_cost):
    dx = abs(node.rect.centerx - goal.rect.centerx)
    dy = abs(node.rect.centery - goal.rect.centery)
    return (dx + dy) + (obstacle_cost - 1) * min(dx, dy)

# Combines the Euclidean and Manhattan distances with obstacles using a weights parameter (0 <= weights <= 1) 
# High Euclidean prioritize accuracy in estimating distances to the goal
# High Manhattan prioritize admissibility to ensure that the heuristic never overestimates the true cost
def combined_heuristic(node: Node, goal: Node, obstacle_cost = 1, euclidean_weight = 1):
    manhattan_weight = 1 - euclidean_weight
    euclidean = euclidean_weight * euclidean_distance(node, goal)
    manhattan = manhattan_weight * manhattan_distance_with_obstacles(node, goal, obstacle_cost)
    return euclidean + manhattan

