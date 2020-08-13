#!/usr/bin/env python3

""" Graph Visualizer using Pygame
"""
import sys
import enum
import math
import pygame
import argparse
import graph_algo
from functools import partial


class Color(enum.Enum):
    # Material Theme Colors
    Background = (38, 49, 50)
    Barrier = (176, 190, 196)
    Visited = (255, 81, 81)
    Open = (105, 240, 173)
    Start = (64, 196, 254)
    End = (255, 215, 63)
    Path = (81, 45, 168)
    Grid = (96, 124, 139)


class Node:
    """Represents a single node in our graph
    """
    def __init__(self, x, y, width, height, total_rows, total_cols):
        self._xcoord = x
        self._ycoord = y
        self._x = x * width
        self._y = y * height
        self._width = width
        self._height = height
        self._color = Color.Background
        self._neighbors = []
        self._total_rows = total_rows
        self._total_cols = total_cols

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, val):
        self._x = val

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, val):
        self._y = val

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, val):
        self._width = val

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, val):
        self._height = val

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, new_color):
        self._color = new_color

    def get_neighbors(self):
        return self._neighbors

    def get_coord_position(self):
        return self._xcoord, self._ycoord

    def is_barrier(self):
        return self._color == Color.Barrier

    def is_closed(self):
        return self._color == Color.Visited

    def is_open(self):
        return self._color == Color.Open

    def is_start(self):
        return self._color == Color.Start

    def is_end(self):
        return self._color == Color.End

    def is_path(self):
        return self._color == Color.Path

    def reset(self):
        self._color = Color.Background

    def make_start(self):
        self._color = Color.Start

    def make_closed(self):
        self._color = Color.Visited

    def make_open(self):
        self._color = Color.Open

    def make_barrier(self):
        self._color = Color.Barrier

    def make_end(self):
        self._color = Color.End

    def make_path(self):
        self._color = Color.Path

    def __eq__(self, other):
        return self._xcoord == other._xcoord and self._ycoord == other._ycoord

    def __hash__(self):
        return hash((self._xcoord, self._ycoord))

    def draw(self, screen):
        """Draw a single node on the graph.

        Args:
            screen (pygame.display): The surface to draw the node on

        Returns:
            pygame.Rect: Rectangle representing the points that need to be updated when redrawing the screen
        """
        dimensions = pygame.draw.rect(screen, self._color.value, (self._x, self._y, self._width, self._height))
        return dimensions

    def update_neighbors(self, grid):
        """Update properly every node's neighbors after each redraw of the screen

        Args:
            grid (list): In memory representation of the graph as a 2D vector
        """
        # Reset current neighbors and update based on current frame
        self._neighbors = list()

        # total_rows - 2 since we omit the drawing of the last row for alignment purposes
        if self._xcoord < self._total_rows - 1 and not grid[self._xcoord + 1][self._ycoord].is_barrier():
            self._neighbors.append(grid[self._xcoord + 1][self._ycoord])

        if self._xcoord > 0 and not grid[self._xcoord - 1][self._ycoord].is_barrier():
            self._neighbors.append(grid[self._xcoord - 1][self._ycoord])

        if self._ycoord < self._total_cols - 1 and not grid[self._xcoord][self._ycoord + 1].is_barrier():
            self._neighbors.append(grid[self._xcoord][self._ycoord + 1])

        if self._ycoord > 0 and not grid[self._xcoord][self._ycoord - 1].is_barrier():
            self._neighbors.append(grid[self._xcoord][self._ycoord - 1])


def init_grid(num_rows, num_cols, node_width, node_height):
    """Used to initialize the grid(graph) in the beginning of the program

    Args:
        num_rows (int): Total number of rows expected in the graph
        num_cols (int): Total number of rows expected in the graph
        node_width (int): Width of a single node
        node_height (int): Height of a single node

    Returns:
        list: Nested list of nodes representing the graph/grid
    """
    grid = list()
    for row in range(num_rows):
        grid.append([])
        for col in range(num_cols):
            grid[row].append(Node(row, col, node_width, node_height, num_rows, num_cols))

    return grid


def draw_grid_borders(screen, rows, cols, node_width, node_height):
    """This function draws the borders between our graph nodes

    Args:
        screen (pygame.display): The screen that pygame draws on
        rows (int): Number of rows in the graph
        cols (int): Number of columns in the graph
        node_width (int): Width of a single node
        node_height (int): Height of a single node

    Returns:
        list: All points that need to be redrawn by pygame due to a change.
              This way one saves resources and does not redraw the entire screen.
    """
    # Get display size on any monitor - width x height
    info = pygame.display.Info()
    size = screen_width, screen_height = info.current_w, info.current_h
    updated_points = list()

    for row in range(rows):
        dims1 = pygame.draw.aaline(screen, Color.Grid.value, (0, row * node_height), (screen_width, row * node_height))
        updated_points.append(dims1)

        for col in range(cols):
            dims2 = pygame.draw.aaline(screen, Color.Grid.value, (col * node_width, row * node_height), (col * node_width, row * node_height + node_height))
            updated_points.append(dims2)

    return updated_points


def refresh_screen(screen, grid, rows, cols, node_width, node_height):
    """This function is used to refresh the screen during each framerate

    Args:
        screen (pygame.display): The screen that pygame draws on
        grid (list): Nested list of lists representing each node in our graph
        rows (int): Number of rows in the graph 
        cols (int): Number of columns in the graph
        node_width (int): Width of a single node
        node_height (int): Height of a single node
    """
    screen.fill(Color.Background.value)
    updated_points = list()

    for row in grid:
        for node in row:
            changed_area = node.draw(screen)
            updated_points.append(changed_area)
    
    grid_dims = draw_grid_borders(screen, rows, cols, node_width, node_height)
    updated_points += grid_dims
    pygame.display.update(updated_points)


def get_clicked_position(pos, node_width, node_height):
    x, y = pos

    row = x // node_width
    col = y // node_height

    return int(row), int(col)


def construct_path(animate_path_func, current, came_from):
    """Reconstruct the path where we came from

    Args:
        animate_path_func (partial): Callable object with the proper arguments to animate found path
        end (Node): End node for the graph
        came_from (dict): Dictionary representing where we came from for each node
    """
    path = list()

    while current in came_from:
        current = came_from[current]
        if not current.is_start():
            current.make_path()
            path.append(current)

    animate_path_func(path)


def animate_path(screen, path):
    """Animate the found path on the board

    Args:
        screen (pygame.display): Surface where the animation will be drawn on
        path (list): List of nodes leading from the end node to the beginning node
    """
    frame_rate = 60

    # Use pygame Clock to control the framerate of the program
    fps_clock = pygame.time.Clock()

    for node in path:
        radius = 0

        while True:
            changed = pygame.draw.circle(screen, node.color.value, (node.x + node.width // 2, node.y + node.height // 2), radius)
            radius += 1
            pygame.display.update(changed)
            fps_clock.tick(frame_rate)

            if radius > (node.height // 2):
                dimensions = pygame.draw.rect(screen, node.color.value, (node.x, node.y, node.width, node.height))
                pygame.display.update(dimensions)
                break


def main():
    parser = argparse.ArgumentParser(description="""Python Graph Visualizer written with pygame
    Usage instructions:
    1. Press the mouse once anywhere on the grid to mark the begin node.
    2. Press the mouse twice somewhere on the grid to mark the end node.
    3. Press, hold, and drag the mouse to create barriers.
    4. Press SPACE for the algorithm to start.
    5. Press TAB for the screen to clear so 1-4 can be performed again.
    6. Press ESCAPE or OS's program shutdown combination to close.""", formatter_class=argparse.RawTextHelpFormatter)
    
    parser.add_argument('-f', '--fullscreen', action='store_true', dest='fullscreen', help='Fullscreen mode vs. Windowed mode')
    parser.add_argument('-a' '--algo', dest='algo', choices=['BFS', 'DFS', 'AStar'], required=True, help='Algorithm to visualize')
    parser.add_argument('-b', '--board', dest='board_size', required=True, help='Size of the board - if 30, then board is 30x30')
    
    args = parser.parse_args()
    algo = args.algo

    pygame.init()

    screen = None
    if args.fullscreen:
        screen = pygame.display.set_mode()
        pygame.display.toggle_fullscreen()
    else:
        screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("PyGraphVisualizer")

    # Get display size on any monitor - width x height
    info = pygame.display.Info()
    size = screen_width, screen_height = info.current_w, info.current_h

    #Calculate each node's width and height
    rows = cols = int(args.board_size)
    node_width = screen_width / rows
    node_height = screen_height / cols
    
    grid = init_grid(rows, cols, node_width, node_height)
    start_node = None
    end_node = None

    # Main event loop
    while True:
        refresh_screen(screen, grid, rows, cols, node_width, node_height)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            
            # Mouse input - left mouse button
            if pygame.mouse.get_pressed()[0]:
                mouse_position = pygame.mouse.get_pos()
                grid_position = get_clicked_position(mouse_position, node_width, node_height)
                row, col = grid_position
                node = grid[row][col]

                if not start_node:
                    node.make_start()
                    start_node = node

                elif start_node and not end_node:
                    node.make_end()
                    end_node = node

                elif node != start_node and node != end_node:
                    node.make_barrier()

            # Mouse input - right mouse button
            if pygame.mouse.get_pressed()[2]:
                mouse_position = pygame.mouse.get_pos()
                grid_position = get_clicked_position(mouse_position, node_width, node_height)
                row, col = grid_position
                node = grid[row][col]

                node.reset()
                if node == start_node:
                    start_node = None
                elif node == end_node:
                    end_node = None

            # Run selected algorithm when space is pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:

                    # Initialize neighbors
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    refresh_func = partial(refresh_screen, screen, grid, rows, cols, node_width, node_height)
                    animate_path_func = partial(animate_path, screen)
                    construct_path_func = partial(construct_path, animate_path_func, end_node)
                    
                    if algo == "BFS":
                        graph_algo.BFS(refresh_func, construct_path_func, grid, start_node, end_node)
                    elif algo == "DFS":
                        graph_algo.DFS(refresh_func, construct_path_func, grid, start_node, end_node)
                    elif algo == "AStar":
                        graph_algo.AStar(refresh_func, construct_path_func, grid, start_node, end_node)

                if event.key == pygame.K_TAB:
                    start_node = None
                    end_node = None
                    grid = init_grid(rows, cols, node_width, node_height)

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit(0)


        # Sleep for x milliseconds to release the CPU to other processes
        pygame.time.wait(10)


if __name__ == "__main__":
    main()
