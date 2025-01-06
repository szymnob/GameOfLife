import random

import pygame
import pygame_gui
from pygame.threads import Thread

from presets import PRESETS

GRID_COLOR = (200,200,200)

CELL_SIZE = 20
CELL_SIZE_MIN = 10
CELL_SIZE_MAX = 50

GRID_SIZE = 800

CONTROL_PANEL_SIZE = 200

WINDOW_WIDTH = GRID_SIZE + CONTROL_PANEL_SIZE
WINDOW_HEIGHT = GRID_SIZE

MIN_SPEED = 1
MAX_SPEED = 20

class Life:
    def __init__(self):
        pygame.init()

        self.grid_size = GRID_SIZE


        self.total_window_width = WINDOW_WIDTH + 200
        self.grid_cells_number = 32
        self.cell_size = self.calculate_cell_size()



        self.is_running = True

        self.sim_running = False

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Game of Life")

        self.grid = [[0 for _ in range(self.grid_cells_number)] for _ in range(self.grid_cells_number)]

        self.speed = 5
        self.iteration = 0

        self.cell_color_mode = "black"
        self.cell_colors = []
        self.set_new_colors()

        self.clock = pygame.time.Clock()
        self.manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT))

        self.create_ui()

    def calculate_cell_size(self):
        return GRID_SIZE // self.grid_cells_number

    def create_ui(self):
        panel_width = CONTROL_PANEL_SIZE

        self.controls_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((GRID_SIZE, 0), (panel_width, WINDOW_HEIGHT)),
            manager=self.manager
        )

        panel_width = self.controls_panel.get_container().get_relative_rect().width

        size = (panel_width - 20, 30)
        label_size = (panel_width - 20, -1)

        # Add buttons and sliders to the panel
        self.start_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, 20), size),
            text='Start', manager=self.manager, container=self.controls_panel,
            anchors={"left": "left", "top": "top", "right": "right"}
        )

        self.stop_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, 10), size),
            text='Stop', manager=self.manager, container=self.controls_panel,
            anchors={"left": "left", "top": "top", "right": "right", "top_target": self.start_button}
        )

        self.reset_button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((10, 10), size),
                text='Reset', manager=self.manager, container=self.controls_panel,
                anchors={"left": "left", "top": "top", "right": "right", "top_target": self.stop_button}
        )

        self.speed_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 20), label_size),
            text='Speed:',  manager=self.manager, container=self.controls_panel,
            anchors={"left": "left", "top": "top", "right": "right", "top_target": self.reset_button}
        )

        self.speed_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((10, 10), size),
            start_value=self.speed,
            value_range=(MIN_SPEED, MAX_SPEED),
            manager=self.manager, container=self.controls_panel,
            anchors={"left": "left", "top": "top", "right": "right", "top_target": self.speed_label}
        )

        self.preset_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 20), label_size),
            text='Preset:', manager=self.manager, container=self.controls_panel,
            anchors={"left": "left", "top": "top", "right": "right", "top_target": self.speed_slider}
        )

        self.preset_menu = pygame_gui.elements.UIDropDownMenu(
            options_list=list(PRESETS.keys()),
            starting_option='None',
            relative_rect=pygame.Rect((10, 10), size),
            manager=self.manager, container=self.controls_panel,
            anchors={"left": "left", "top": "top", "right": "right", "top_target": self.preset_label}
        )

        self.grid_cells_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 20), label_size),
            text='Number of Cells:', manager=self.manager, container=self.controls_panel,
            anchors={"left": "left", "top": "top", "right": "right", "top_target": self.preset_menu}
        )

        self.grid_cells_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((10, 10), size),
            start_value=self.grid_cells_number,
            value_range=(10, 50),
            manager=self.manager, container=self.controls_panel,
            anchors={"left": "left", "top": "top", "right": "right", "top_target": self.grid_cells_label}
        )

        self.color_mode_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 10), label_size),
            text='Cell Color Mode:', manager=self.manager, container=self.controls_panel,
            anchors={"left": "left", "top": "top", "right": "right", "top_target": self.grid_cells_slider}
        )

        self.color_mode_menu = pygame_gui.elements.UIDropDownMenu(
            options_list=["black", "random", "random_for_new"],
            starting_option=self.cell_color_mode,
            relative_rect=pygame.Rect((10, 10), size),
            manager=self.manager, container=self.controls_panel,
            anchors={"left": "left", "top": "top", "right": "right", "top_target": self.color_mode_label}
        )

        self.save_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, 40), size),
            text='Save', manager=self.manager, container=self.controls_panel,
            anchors={"left": "left", "top": "top", "right": "right", "top_target": self.color_mode_menu}
        )

        #iteration label
        self.iteration_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, -40), label_size),
            text=f'Iteration: {self.iteration}',
            manager=self.manager, container=self.controls_panel,
            anchors={"left": "left", "bottom": "bottom", "right": "right"}
        )

    def set_new_colors(self, y = None, x = None, was_alive = False):
        if self.cell_color_mode == "black" and (y is None or x is None):
            self.cell_colors = [[(0, 0, 0) for _ in range(self.grid_cells_number)] for _ in range(self.grid_cells_number)]
        elif self.cell_color_mode == "random" and (y is None or x is None):
            self.cell_colors = [[(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in range(self.grid_cells_number)] for _ in range(self.grid_cells_number)]
        elif self.cell_color_mode == "random_for_new":
            if y is not None and x is not None:
                if not was_alive:
                    self.cell_colors[y][x] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                else:
                    self.cell_colors[y][x] = (0, 0, 0)

    def draw_grid(self):
        #center grid in the middle so margin is the same on all sides, need to be used when calculating click position
        self.grid_margin = (self.grid_size - self.grid_cells_number * self.cell_size) // 2
        pygame.draw.rect(self.screen, GRID_COLOR, (0,0, self.grid_size, self.grid_size))
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        for y in range(self.grid_cells_number):
            for x in range(self.grid_cells_number):
                color = self.cell_colors[y][x] if self.grid[y][x] else GRID_COLOR
                pygame.draw.rect(self.screen, color, (x*self.cell_size + self.grid_margin, y*self.cell_size + self.grid_margin, self.cell_size, self.cell_size))

                pygame.draw.rect(self.screen, (170, 170, 170), (x*self.cell_size + self.grid_margin, y*self.cell_size + self.grid_margin, self.cell_size, self.cell_size), 1)
    def count_alive_neighbours(self, x, y):
        count = 0
        #left
        if x > 0:
            count += self.grid[y][x-1]
        #right
        if x < self.grid_cells_number - 1:
            count += self.grid[y][x+1]
        #top
        if y > 0:
            count += self.grid[y-1][x]
        #bottom
        if y < self.grid_cells_number - 1:
            count += self.grid[y+1][x]
        #top left
        if x > 0 and y > 0:
            count += self.grid[y-1][x-1]
        #top right
        if x < self.grid_cells_number - 1 and y > 0:
            count += self.grid[y-1][x+1]
        #bottom left
        if x > 0 and y < self.grid_cells_number - 1:
            count += self.grid[y+1][x-1]
        #bottom right
        if x < self.grid_cells_number - 1 and y < self.grid_cells_number - 1:
            count += self.grid[y+1][x+1]

        return count

    def update_iteration_label(self):
        self.iteration_label.set_text(f'Iteration: {self.iteration}')

    def reset(self):
        self.sim_running = False
        self.grid = [[0 for _ in range(self.grid_cells_number)] for _ in range(self.grid_cells_number)]
        self.iteration = 0
        self.update_iteration_label()

    def start(self):
        self.sim_running = True
        Thread(target=self.simulation, daemon=True).start()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                x, y = event.pos
                grid_x, grid_y = int((x - self.grid_margin) // self.cell_size), int((y - self.grid_margin) // self.cell_size)
                if 0 <= grid_x < self.grid_cells_number and 0 <= grid_y < self.grid_cells_number:
                    self.grid[grid_y][grid_x] = 1 - self.grid[grid_y][grid_x]

        elif event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.start_button:
                self.start()
            elif event.ui_element == self.stop_button:
                self.sim_running = False
            elif event.ui_element == self.reset_button:
                self.reset()
            elif event.ui_element == self.save_button:
                self.normalize_and_save()

        elif event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == self.preset_menu:
                self.load_preset(event.text)
            elif event.ui_element == self.color_mode_menu:
                self.cell_color_mode = event.text

        elif event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            if event.ui_element == self.speed_slider:
                self.speed = int(self.speed_slider.get_current_value())
            elif event.ui_element == self.grid_cells_slider:
                self.scale_grid(int(self.grid_cells_slider.get_current_value()))

    def scale_grid(self, new_cells_number):
        """Scales the grid while maintaining the current state of the cells"""
        self.sim_running = False

        offset = new_cells_number//2 - self.grid_cells_number//2

        new_grid = [[0 for _ in range(new_cells_number)] for _ in range(new_cells_number)]

        for y in range(self.grid_cells_number):
            for x in range(self.grid_cells_number):
                x_scaled = x + offset
                y_scaled = y + offset
                if 0 <= x_scaled < self.grid_cells_number and 0 <= y_scaled < self.grid_cells_number:
                    try:
                        new_grid[y_scaled][x_scaled] = self.grid[y][x]
                    except IndexError:
                        pass

        self.grid_cells_number = new_cells_number
        self.cell_size = self.calculate_cell_size()
        self.grid = new_grid

        self.set_new_colors()


    def simulation(self):
        while self.sim_running:

            self.iteration += 1
            self.update_iteration_label()
            added = False

            new_grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]

            for y in range(self.grid_cells_number):
                for x in range(self.grid_cells_number):
                    alive = self.count_alive_neighbours(x, y)

                    if (self.grid[y][x] == 1 and alive in (2, 3)) or (self.grid[y][x] == 0 and alive == 3):
                        new_grid[y][x] = 1
                        added = True
                        self.set_new_colors(y, x, self.grid[y][x])

            self.grid = new_grid

            self.set_new_colors()

            if not added:
                self.sim_running = False

            self.clock.tick(self.speed)

    def load_preset(self, preset_name):
        self.reset()

        center_x = self.grid_cells_number // 2
        center_y = self.grid_cells_number // 2

        for x, y in PRESETS[preset_name]:
            try:
                self.grid[center_y + y][center_x + x] = 1
            except IndexError:
                self.reset()
                self.iteration_label.set_text(f'Too small grid size!')
                return

        self.draw_grid()

    def run(self):
        while self.is_running:
            time_delta = self.clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                    pygame.quit()
                    return
                self.handle_event(event)
                self.manager.process_events(event)

            self.screen.fill((33, 40, 45))
            self.draw_grid()

            self.manager.update(time_delta)
            self.manager.draw_ui(self.screen)

            pygame.display.flip()

        pygame.quit()

    def normalize_and_save(self):
        """Normalizes the grid to be centered around 0,0 and saves it to a file which can be then added to presets file"""
        tab = []

        for x in range(self.grid_cells_number):
            for y in range(self.grid_cells_number):
                if self.grid[y][x] == 1:
                    tab.append((x,y))

        x_min = min(p[0] for p in tab)
        x_max = max(p[0] for p in tab)
        y_min = min(p[1] for p in tab)
        y_max = max(p[1] for p in tab)

        center_x = (x_min + x_max) // 2
        center_y = (y_min + y_max) // 2

        normalized_tab = [(x - center_x, y - center_y) for x, y in tab]

        with open("presets.txt", "a") as file:
            file.write(f"{normalized_tab}\n")

if __name__ == "__main__":
    life = Life()
    life.run()