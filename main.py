""" Graph Visualizer using Pygame
"""
import sys
import enum
import math
import pygame


class Color(enum.Enum):
    Red = (255, 0, 0)
    Green = (0, 255, 0)
    Blue = (0, 255, 0)
    Yellow = (255, 255, 0)
    White = (255, 255, 255)
    Black = (0, 0, 0)
    Purple = (128, 0, 128)
    Orange = (255, 165 ,0)
    Grey = (128, 128, 128)
    Turquoise = (64, 224, 208)


class Node:
    def __init__(self, row, col, width, height, total_rows):
        self._row = row
        self._col = col
        self._x = row * width
        self._y = col * height
        self._width = width
        self._height = height
        self._color = Color.White
        self._neighbors = []
        self._total_rows = total_rows

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

    def get_coordinate(self):
        return self._row, self._col


    def draw(self, screen):
        """

        """
        radius = 0
        frame_rate = 60

        # Use pygame Clock to control the framerate of the program
        fps_clock = pygame.time.Clock()

        if self._color.value == Color.Purple.value:
            while True:
                pygame.draw.circle(screen, self._color.value, (self._x + self._width // 2, self._y + self._height // 2), radius)
                radius += 2
                pygame.display.update()
                fps_clock.tick(frame_rate)

                if radius > (height // 2):
                    break
        
        pygame.draw.rect(screen, self._color.value, (self._x, self._y, self._width, self._height))
        
        if self._color.value == Color.Purple.value:
            fps_clock.tick(frame_rate)


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
            
            # Don't append last row to leave space for padding when drawing
            if row == num_rows - 1:
                continue
            
            grid[row].append(Node(row, col, node_width, node_height, num_rows))

    return grid


def draw_grid_borders(screen, rows, cols, node_width, node_height):
    """This function draws the borders between our graph nodes

    Args:
        screen (pygame.display): The screen that pygame draws on
        rows (int): Number of rows in the graph
        cols (int): Number of columns in the graph
        node_width (int): Width of a single node
        node_height (int): Height of a single node
    """
    # Get display size on any monitor - width x height
    info = pygame.display.Info()
    size = screen_width, screen_height = info.current_w, info.current_h

    for row in range(rows):
        pygame.draw.line(screen, Color.Black.value, (0, row * node_height), (screen_width, row * node_height))

        # Omit drawing the last raw for space padding
        if row == rows - 1:
            break

        for col in range(cols):
            pygame.draw.line(screen, Color.Black.value, (col * node_width, row * node_height), (col * node_width, row * node_height + node_height))


def refresh_screen(screen, grid, rows, cols, node_width, node_height):
    """This function is used to refresh the screen during each framerate

    Args:
        screen (pygame.display): The screen that pygame draws on
        grid (list): Nested list of lists representing each node in our graph
        rows (int): Number of rows in the graph 
        cols (int): Number of columns in the graph
        node_width ([type]): Width of a single node
        node_height ([type]): Height of a single node
    """
    screen.fill(Color.White.value)

    for row in grid:
        for node in row:
            node.draw(screen)
    
    draw_grid_borders(screen, rows, cols, node_width, node_height)
    pygame.display.update()


def main():
    pygame.init()
    screen = pygame.display.set_mode()
    pygame.display.set_caption("PyGraphVisualizer")

    # Get display size on any monitor - width x height
    info = pygame.display.Info()
    size = screen_width, screen_height = info.current_w, info.current_h

    #Calculate each node's width and height
    rows = cols = 90
    node_width = screen_width / rows
    node_height = screen_height // cols
    
    grid = init_grid(rows, cols, node_width, node_height)

    # Main event loop
    while True:
        refresh_screen(screen, grid, rows, cols, node_width, node_height)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            
            # Keyboard input - space
            if event.type == pygame.KEYDOWN:
                pass
                # if event.key == pygame.K_SPACE:
                #     node = Node(3, 4, 50, 40, 10)
                #     draw_visited_node(screen, node, 50, 40)

        # Sleep for 50 milliseconds to release the CPU to other processors
        # pygame.time.wait(50)


if __name__ == "__main__":
    main()
