# PyGraphVisualizer
Python Graph Algorithm Visualizer Using Pygame.

# About Pygame
Pygame is a python library used for creating 2D and 3D games and applications. This program uses pygame as well, so before running it one must install pygame first. For more information on how to do that based on your platform please visit the [Getting Started](https://www.pygame.org/wiki/GettingStarted) pygame page. I have developed this application with pygame2 in mind and using version 2's documentation so it is preferable for one to use version 2 of the librray.

# Usage
Python version 3 is the recommended version to use when running this. File main.py provides a shebang, which defaults to the latest version of python 3 so one can simply run main.py in terminal like an executable:
```
./main.py [options]
```
For more detailed information regarding the options, type:
```
./main.py --help
```

# Examples
### Run Fullscreen A star on a 50x50 board
```
./main.py -f -a AStar -b 50
```

### Run Breadth First Search in Windowed Mode on a 30x30 board
```
./main.py -a BFS -b 30
```

To clear the board press TAB.
To exit press either ESCAPE or the corresponding key combination to close apps on your OS. For example on macOS - ⌘+Q

# Caveats
Beware that the larger the grid, the more time the algorithm will take to complete. I have synchronized pygame to work at 60 FPS, however, as previously stated the larger the grid the more sluggish and unresponsive the graphics may appear especially when dragging and selecting the barriers. Ideally the grid should be anywhere from 30 to 60 (that is 30x30 to 60x60).