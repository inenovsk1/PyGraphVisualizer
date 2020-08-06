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
    Light_blue = (102, 204, 255)
    Yellow = (255, 255, 0)
    White = (255, 255, 255)
    Black = (0, 0, 0)
    Purple = (128, 0, 128)
    Light_purple = (102, 102, 255)
    Orange = (255, 165 ,0)
    Pink = (255, 192, 203)
    Grey = (128, 128, 128)
    Turquoise = (64, 224, 208)


class Node:
    """Represents a single node in our graph
    """
    def __init__(self, row, col, width, height, total_rows, total_cols):
        self._row = row
        self._col = col
        self._x = row * width
        self._y = col * height
        self._width = width
        self._height = height
        self._color = Color.White
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

    def get_coord_position(self):
        return self._row, self._col

    def is_barrier(self):
        return self._color == Color.Black

    def is_visited(self):
        return self._color == Color.Red

    def is_open(self):
        return self._color == Color.Green

    def is_start(self):
        return self._color == Color.Light_blue

    def is_end(self):
        return self._color == Color.Light_purple

    def is_path(self):
        return self._color == Color.Pink

    def reset(self):
        self._color = Color.White

    def make_start(self):
        self._color = Color.Light_blue

    def make_closed(self):
        self._color = Color.Red

    def make_open(self):
        self._color = Color.Green

    def make_barrier(self):
        self._color = Color.Black

    def make_end(self):
        self._color = Color.Light_purple

    def make_path(self):
        self._color = Color.Pink

    def __eq__(self, other):
        return self._row == other._row and self._col == other._col


    def draw(self, screen):
        """Draw a single node on the graph. Make appropriate animations based on
        node type

        Args:
            screen (pygame.display): The surface to draw the node on

        Returns:
            list: All points that need to be redrawn by pygame due to a change.
                  This way one saves resources and does not redraw the entire screen.
        """
        radius = 0
        frame_rate = 60
        updated_points = list()

        # Use pygame Clock to control the framerate of the program
        fps_clock = pygame.time.Clock()

        if self.is_path():
            while True:
                changed = pygame.draw.circle(screen, self._color.value, (self._x + self._width // 2, self._y + self._height // 2), radius)
                radius += 2
                pygame.display.update(changed)
                fps_clock.tick(frame_rate)

                if radius > (height // 2):
                    break
        
        dimensions = pygame.draw.rect(screen, self._color.value, (self._x, self._y, self._width, self._height))
        updated_points.append(dimensions)
        
        if self.is_path():
            fps_clock.tick(frame_rate)

        return updated_points

    def update_neighbors(self, grid):
        """Update properly every node's neighbors after each redraw of the screen

        Args:
            grid (list): In memory representation of the graph as a 2D vector
        """
        # Reset current neighbors and update based on current frame
        self._neighbors = list()

        # total_rows - 2 since we omit the drawing of the last row for alignment purposes
        if self._row < self._total_rows - 2 and not grid[self._row + 1][self._col].is_barrier():
            self._neighbors.append(grid[self._row + 1][self._col])

        if self_row > 0 and not grid[self._row - 1][self._col].is_barrier():
            self._neighbors.append(grid[self._row - 1][self._col])

        if self._col < self._total_cols - 1 and not grid[self._row][self._col + 1].is_barrier():
            self._neighbors.append(grid[self._row][self._col + 1])

        if self._col > 0 and not grid[self._row][self._col - 1].is_barrier():
            self._neighbors.append(grid[self._row][self._col - 1])


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
        node_width (int): Width of a single node
        node_height (int): Height of a single node
    """
    screen.fill(Color.White.value)
    updated_points = list()

    for row in grid:
        for node in row:
            changed_area = node.draw(screen)
            updated_points += changed_area
    
    draw_grid_borders(screen, rows, cols, node_width, node_height)
    pygame.display.update(updated_points)



def get_clicked_position(pos, node_width, node_height):
    x, y = pos

    row = x // node_width
    col = y // node_height

    return int(row), int(col)


def main():
    pygame.init()
    screen = pygame.display.set_mode()
    pygame.display.set_caption("PyGraphVisualizer")

    # Get display size on any monitor - width x height
    info = pygame.display.Info()
    size = screen_width, screen_height = info.current_w, info.current_h

    #Calculate each node's width and height
    rows = cols = 30
    node_width = screen_width / rows
    node_height = screen_height // cols
    
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
            
            # Keyboard input - space
            # if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                mouse_position = pygame.mouse.get_pos()
                grid_position = get_clicked_position(mouse_position, node_width, node_height)
                print(grid_position)
                row, col = grid_position
                node = grid[row][col]

                if not start_node:
                    node.make_start()
                    start_node = node

                elif start_node and not end_node:
                    node.make_end()
                    end_node = node

                elif node != start_node and node != end_node:
                    print("different")
                    node.make_barrier()

                print(start_node)
                print(end_node)

        # Sleep for 50 milliseconds to release the CPU to other processors
        pygame.time.wait(25)


if __name__ == "__main__":
    main()
