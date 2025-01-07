import random

import pygame

from conf import *

from presets import PRESETS


class Grid:
    def __init__(self, grid_size, cells_number):
        self.grid_size = grid_size
        self.cells_number = cells_number
        self.cell_size = self.calculate_cell_size()
        self.grid = [[0 for _ in range(self.cells_number)] for _ in range(self.cells_number)]
        self.cell_colors = [[(0, 0, 0) for _ in range(self.cells_number)] for _ in range(self.cells_number)]

        self.color_mode = "black"

        self.clock = pygame.time.Clock()

    def calculate_cell_size(self):
        return self.grid_size // self.cells_number

    def reset_grid(self):
        self.grid = [[0 for _ in range(self.cells_number)] for _ in range(self.cells_number)]

    def scale_grid(self, new_cells_number):
        """Scales the grid while maintaining the current state of the cells"""

        offset = new_cells_number // 2 - self.cells_number // 2

        new_grid = [[0 for _ in range(new_cells_number)] for _ in range(new_cells_number)]

        for y in range(self.cells_number):
            for x in range(self.cells_number):
                x_scaled = x + offset
                y_scaled = y + offset
                if 0 <= x_scaled < self.cells_number and 0 <= y_scaled < self.cells_number:
                    try:
                        new_grid[y_scaled][x_scaled] = self.grid[y][x]
                    except IndexError:
                        pass

        self.cells_number = new_cells_number
        self.cell_size = self.calculate_cell_size()
        self.grid = new_grid

#        self.update_colors()

    def draw(self, screen):
        grid_margin = (self.grid_size - self.cells_number * self.cell_size) // 2
        pygame.draw.rect(screen, GRID_COLOR, (0, 0, self.grid_size, self.grid_size))

        for y in range(self.cells_number):
            for x in range(self.cells_number):
                color = self.cell_colors[y][x] if self.grid[y][x] else GRID_COLOR
                pygame.draw.rect(screen, color, (x * self.cell_size + grid_margin, y * self.cell_size + grid_margin, self.cell_size, self.cell_size))
                pygame.draw.rect(screen, (170, 170, 170), (x * self.cell_size + grid_margin, y * self.cell_size + grid_margin, self.cell_size, self.cell_size), 1)

    def update_colors(self, y=None, x=None, was_alive=False):
        if self.color_mode == "black":
            self.cell_colors = [[(0, 0, 0) for _ in range(self.cells_number)] for _ in range(self.cells_number)]
        elif self.color_mode == "random" and y is None and x is None:
            self.cell_colors = [[(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in range(self.cells_number)] for _ in range(self.cells_number)]
        elif self.color_mode == "random_for_new" and y is not None and x is not None:
            self.cell_colors[y][x] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) if not was_alive else (0, 0, 0)

    def set_color_mode(self, mode):
        self.color_mode = mode

    def load_preset(self, preset_name):

        center_x = self.cells_number // 2
        center_y = self.cells_number // 2

        for x, y in PRESETS[preset_name]:
            try:
                self.grid[center_y + y][center_x + x] = 1
            except IndexError:
                return "Too small grid size"

    def save(self):
        """Normalizes the grid to be centered around 0,0 and saves it to a file which can be then added to presets file"""
        tab = []

        for x in range(self.cells_number):
            for y in range(self.cells_number):
                if self.grid[y][x] == 1:
                    tab.append((x, y))

        x_min = min(p[0] for p in tab)
        x_max = max(p[0] for p in tab)
        y_min = min(p[1] for p in tab)
        y_max = max(p[1] for p in tab)

        center_x = (x_min + x_max) // 2
        center_y = (y_min + y_max) // 2

        normalized_tab = [(x - center_x, y - center_y) for x, y in tab]

        with open("presets.txt", "a") as file:
            file.write(f"{normalized_tab}\n")

        print("Saved")

    def simulation(self):
            added = False

            new_grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]

            for y in range(self.cells_number):
                for x in range(self.cells_number):
                    alive = self.count_alive_neighbours(x, y)

                    if (self.grid[y][x] == 1 and alive in (2, 3)) or (self.grid[y][x] == 0 and alive == 3):
                        new_grid[y][x] = 1
                        added = True
                        self.update_colors(y, x, self.grid[y][x])

            self.grid = new_grid

            self.update_colors()

            return added

    def count_alive_neighbours(self, x, y):
        count = 0
        #left
        if x > 0:
            count += self.grid[y][x-1]
        #right
        if x < self.cells_number - 1:
            count += self.grid[y][x+1]
        #top
        if y > 0:
            count += self.grid[y-1][x]
        #bottom
        if y < self.cells_number - 1:
            count += self.grid[y+1][x]
        #top left
        if x > 0 and y > 0:
            count += self.grid[y-1][x-1]
        #top right
        if x < self.cells_number - 1 and y > 0:
            count += self.grid[y-1][x+1]
        #bottom left
        if x > 0 and y < self.cells_number - 1:
            count += self.grid[y+1][x-1]
        #bottom right
        if x < self.cells_number - 1 and y < self.cells_number - 1:
            count += self.grid[y+1][x+1]

        return count