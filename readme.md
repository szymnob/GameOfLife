# Conway's Game of Life

This repository contains three implementations of Conway's Game of Life, a cellular automaton devised by the British mathematician John Conway. The Game of Life is a zero-player game, meaning its evolution is determined by its initial state, requiring no further input. The game consists of a grid of cells that follow simple rules to determine whether they live, die, or reproduce in the next iteration.

## Project Versions

### 1. Version 1: Tkinter Implementation
- The first version is implemented using **Tkinter** for the graphical user interface.
- A simple, straightforward approach showcasing the rules and behavior of the Game of Life.
- **File**: `v1_tkinter/LifeTkinter.py`

### 2. Version 2: Pygame Implementation
- The second version upgrades to **Pygame** for better graphical performance and user interaction.
- Improved visuals and a more responsive user experience compared to the Tkinter version.
- **File**: `v2_pygame/LifePygame.py`

### 3. Version 3: Pygame with Object-Oriented Design
- The third version is a refactored and enhanced implementation of Version 2.
- Uses the **pygame-gui** library for building the graphical user interface.
- Uses an **object-oriented design** for better modularity, maintainability, and extensibility.
- Includes separate modules for configuration (`conf.py`), UI management (`ControlUI.py`), grid logic (`Grid.py`), and the main application logic (`main.py`).
- **File**: `v3_pygame/main.py`



## How to Run

1. Navigate to the version directory of your choice.
2. Run the main script:
 - For Tkinter: `python LifeTkinter.old.py`
 - For Pygame Version 2: `python LifePygame.py`
 - For Pygame Object-Oriented Version 3: `python main.py`

## Features

- **Presets**: Predefined patterns like Gliders, Spaceships, and more.
- **Dynamic Grid**: Ability to scale and reset the grid.
- **Color Modes**: Choose between different cell coloring styles (black, random, etc.).
- **Save and Load**: Save current patterns to use them later.
- **User Interface with pygame-gui**:
- Includes sliders for adjusting speed and grid size.
- Dropdown menus for selecting presets and color modes.
- Buttons for starting, stopping, and resetting the simulation, as well as saving patterns.


Explore the evolution of the Game of Life across different implementations and enjoy tinkering with patterns and rules!

## License

This project is open-source and free to use under the MIT License.
