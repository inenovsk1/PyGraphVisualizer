"""
Implementation of graph algorithms used in the visualizer
"""
import sys
import pygame
from collections import deque

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
