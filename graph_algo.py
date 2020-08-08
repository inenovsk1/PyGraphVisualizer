"""
Implementation of graph algorithms used in the visualizer
"""
import sys
import pygame
from collections import deque

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
############### Depth First Search ################
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
    """
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