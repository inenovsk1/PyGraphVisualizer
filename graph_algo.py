"""
Implementation of graph algorithms used in the visualizer
"""
import sys
import math
import pygame
from collections import deque
from queue import PriorityQueue

#####################################################
############### Breadth First Search ################
#####################################################

def BFS(refresh_func, construct_path, grid, start_node, end_node):
    """Implementation of Breadth First Search for the visualizer

    Args:
        refresh_func (partial): Callable object with the proper arguments to redraw graph after each move
        construct_path (partial): Callable object with first 2 arguments to draw the path the algo found.
        Only the came_from parameter needs to be supplied which was constructed by the algo.
        grid (list): Representation of the graph as a 2D matrix
        start_node (Node): Start Node for the algorithm
        end_node (Node): End node for the algorithm

    Returns:
        bool: True if we were able to find a path, False otherwise
    """
    visited = set()
    came_from = dict()
    q = deque([])
    
    q.append(start_node)
    visited.add(start_node)

    while q:
        # Handle exiting while algo is running
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

        current = q.popleft()

        if current == end_node:
            construct_path(came_from)
            return True

        for neighbor in current.get_neighbors():
            if neighbor not in visited:
                q.append(neighbor)
                came_from[neighbor] = current
                visited.add(neighbor)
                
                if neighbor != end_node:
                    neighbor.make_open()

        refresh_func()

        if current != start_node:
            current.make_closed()

    return False

#####################################################
############### Depth First Search ##################
#####################################################
stop_recursion = False

def DFSUtil(refresh_func, construct_path, came_from, current, visited, start_node, end_node, found_path):
    """Utility helper function that would perform depth traversal from each node

    Args:
        refresh_func (partial): Callable object with the proper arguments to redraw graph after each move
        construct_path (partial): Callable object with first 2 arguments to draw the path the algo found
        came_from (dict): Dictionary representing { destination -> source } to construct the path 
        current (Node): Current node in the algorithm's execution
        visited (set): Set of all visited nodes so far
        start_node (set): Start node of the algorithm
        end_node (Node): End node of the algorithm
        found_path (Node): Whether a path was found and no more recursion is needed

    Returns:
        True or False whether a path was found or not
    """
    # Handle exiting while algo is running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

    global stop_recursion

    if found_path:
        stop_recursion = True
        return True
    
    visited.add(current)
    
    if current != end_node:
        current.make_open()

    for neighbor in current.get_neighbors():
        if stop_recursion:
            break

        if neighbor in visited:
            if neighbor != start_node:
                neighbor.make_closed()
        
        if neighbor not in visited:
            came_from[neighbor] = current

            if current != start_node:
                current.make_closed()

            if neighbor == end_node:
                construct_path(came_from)
                found_path = True
                stop_recursion = True
            
            refresh_func()

            if not found_path:
                return DFSUtil(refresh_func, construct_path, came_from, neighbor, visited, start_node, end_node, found_path)

def DFS(refresh_func, construct_path, grid, start_node, end_node):
    """Implementation of Depth First Search for the Visualizer

    Args:
        refresh_func (partial): Callable object with the proper arguments to redraw graph after each move
        construct_path (partial): Callable object with first 2 arguments to draw the path the algo found
        grid (list): Representation of the graph as a 2D matrix
        start_node (Node): Start node of the algorithm
        end_node (Node): End node of the algorithm

    Returns:
        Bool: True or False whether a path was found or not
    """
    sys.setrecursionlimit(10000)
    visited = set()
    visited.add(start_node)
    
    global stop_recursion
    stop_recursion = False

    came_from = dict()

    for neighbor in start_node.get_neighbors():
        if neighbor not in visited:
            found = DFSUtil(refresh_func, construct_path, came_from, neighbor, visited, start_node, end_node, False)

            if found:
                return True

    return False

#####################################################
####################### A Star ######################
#####################################################

def heuristic(start_node, end_node):
    """Heuristic function used to calculate the distance between start node
    and end node for the A start path finding algorithm. For this function
    we will use Euclidean distance to calculate the H score

    Args:
        start_node (Node): Start node for the heuristic
        end_node (Node): End node for the heuristic
    """
    x1, y1 = start_node.get_coord_position()
    x2, y2 = end_node.get_coord_position()
    # return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    return abs(x1-x2) + abs(y1-y2)

def AStar(refresh_func, construct_path_func, grid, start_node, end_node):
    """Implementation of the A star algorithm using F score, G score, and
    calculating heuristics by using Euclidean distance.

    Args:
        refresh_func (partial): Callable object with the proper arguments to redraw graph after each move
        construct_path_func (partial): Callable object with the first 2 arguments to draw the path the algo found
        grid (list): Representation of the graph as a 2D matrix
        start_node (Node): Start node of the algorithm
        end_node (Node): End node of the algorithm

    Returns:
        Bool: True or False whether a path was found or not
    """
    item_order = 0
    q = PriorityQueue()
    q.put((0, item_order, start_node))

    came_from = dict()
    g_score = {node: float("inf") for row in grid for node in row}
    f_score = {node: float("inf") for row in grid for node in row}
    g_score[start_node] = 0
    f_score[start_node] = g_score[start_node] + heuristic(start_node, end_node)

    open_set = set([start_node])

    while not q.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Get the third item in our tuple, which will be the node
        current = q.get()[2]
        open_set.remove(current)

        if current == end_node:
            construct_path_func(came_from)
            return True

        for neighbor in current.get_neighbors():
            neighbor_g_score = g_score[current] + 1

            if neighbor_g_score < g_score[neighbor]:
                g_score[neighbor] = neighbor_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, end_node)
                came_from[neighbor] = current

                if neighbor not in open_set:
                    item_order += 1
                    q.put((f_score[neighbor], item_order, neighbor))
                    open_set.add(neighbor)
                    
                    if neighbor != end_node:
                        neighbor.make_open()

        refresh_func()

        if current != start_node:
            current.make_closed()

    return False