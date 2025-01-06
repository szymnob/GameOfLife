import pygame
import pygame_gui
from pygame.threads import Thread

from presets import PRESETS

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

CELL_SIZE = 30
CELL_SIZE_MIN = 10
CELL_SIZE_MAX = 50

GRID_SIZE = 20
GRID_SIZE_MIN = 10
GRID_SIZE_MAX = 50

MIN_SPEED = 1
MAX_SPEED = 20

class Life:
    def __init__(self):
        pygame.init()

        self.grid_size = GRID_SIZE
        self.cell_size = CELL_SIZE

        self.is_running = True

        self.sim_running = False

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Game of Life")

        self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        self.speed = (MIN_SPEED + MAX_SPEED) // 2
        self.iteration = 0

        self.clock = pygame.time.Clock()
        self.manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT))

        self.create_ui()

    def create_ui(self):
        panel_width = WINDOW_WIDTH - CELL_SIZE * self.grid_size

        self.controls_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((CELL_SIZE * self.grid_size, 0), (panel_width, WINDOW_HEIGHT)),
            manager=self.manager
        )

        panel_width = self.controls_panel.get_container().get_relative_rect().width

        size = (panel_width - 20, 30)
        label_size = (panel_width - 20, -1)

        # Add buttons and sliders to the panel
        self.start_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, 10), size),
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
            relative_rect=pygame.Rect((10, 10), label_size),
            text='Speed:',  manager=self.manager, container=self.controls_panel,
            anchors={"left": "left", "top": "top", "right": "right", "top_target": self.reset_button}
        )

        self.speed_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((10, 20), size),
            start_value=self.speed,
            value_range=(MIN_SPEED, MAX_SPEED),
            manager=self.manager, container=self.controls_panel,
            anchors={"left": "left", "top": "top", "right": "right", "top_target": self.speed_label}
        )

        self.preset_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 10), label_size),
            text='Preset:', manager=self.manager, container=self.controls_panel,
            anchors={"left": "left", "top": "top", "right": "right", "top_target": self.speed_slider}
        )

        self.preset_menu = pygame_gui.elements.UIDropDownMenu(
            options_list=list(PRESETS.keys()),
            starting_option='None',
            relative_rect=pygame.Rect((10, 10), size),
            manager=self.manager, container=self.controls_panel,
            anchors={"left": "left", "top": "top", "right": "right", "top_target": self.speed_slider}
        )

        self.grid_size_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 20), label_size),
            text='Grid Size:', manager=self.manager, container=self.controls_panel,
            anchors={"left": "left", "top": "top", "right": "right", "top_target": self.preset_menu}
        )

        self.grid_size_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((10, 10), size),
            start_value=self.grid_size,
            value_range=(GRID_SIZE_MIN, GRID_SIZE_MAX),
            manager=self.manager, container=self.controls_panel,
            anchors={"left": "left", "top": "top", "right": "right", "top_target": self.grid_size_label}
        )

        self.cell_size_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 10), label_size),
            text='Cell Size:', manager=self.manager, container=self.controls_panel,
            anchors={"left": "left", "top": "top", "right": "right", "top_target": self.grid_size_slider}
        )

        self.cell_size_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((10, 10), size),
            start_value=self.cell_size,
            value_range=(CELL_SIZE_MIN, CELL_SIZE_MAX),
            manager=self.manager, container=self.controls_panel,
            anchors={"left": "left", "top": "top", "right": "right", "top_target": self.cell_size_label}
        )

        self.iteration_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, -40), label_size),
            text=f'Iteration: {self.iteration}',
            manager=self.manager, container=self.controls_panel,
            anchors={"left": "left", "bottom": "bottom", "right": "right"}
        )

    def draw_grid(self):
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                color = (0, 0,0) if self.grid[y][x] else (255, 255, 255)
                pygame.draw.rect(self.screen, color, (x*self.cell_size, y*self.cell_size, self.cell_size, self.cell_size))
                pygame.draw.rect(self.screen, (200, 200, 200), (x*self.cell_size, y*self.cell_size, self.cell_size, self.cell_size), 1)

    def count_alive_neighbours(self, x, y):
        count = 0
        #left
        if x > 0:
            count += self.grid[y][x-1]
        #right
        if x < self.grid_size - 1:
            count += self.grid[y][x+1]
        #top
        if y > 0:
            count += self.grid[y-1][x]
        #bottom
        if y < self.grid_size - 1:
            count += self.grid[y+1][x]
        #top left
        if x > 0 and y > 0:
            count += self.grid[y-1][x-1]
        #top right
        if x < self.grid_size - 1 and y > 0:
            count += self.grid[y-1][x+1]
        #bottom left
        if x > 0 and y < self.grid_size - 1:
            count += self.grid[y+1][x-1]
        #bottom right
        if x < self.grid_size - 1 and y < self.grid_size - 1:
            count += self.grid[y+1][x+1]

        return count

    def update_iteration_label(self):
        self.iteration_label.set_text(f'Iteration: {self.iteration}')

    def reset(self):
        self.sim_running = False
        self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.iteration = 0
        self.update_iteration_label()

    def start(self):
        self.sim_running = True
        Thread(target=self.simulation, daemon=True).start()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                x, y = event.pos
                grid_x, grid_y = x // CELL_SIZE, y // CELL_SIZE
                if 0 <= grid_x < self.grid_size and 0 <= grid_y < self.grid_size:
                    self.grid[grid_y][grid_x] = 1 - self.grid[grid_y][grid_x]

        elif event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.start_button:
                self.start()
            elif event.ui_element == self.stop_button:
                self.sim_running = False
            elif event.ui_element == self.reset_button:
                self.reset()
        elif event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == self.preset_menu:
                self.load_preset(event.text)

        elif event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            if event.ui_element == self.speed_slider:
                self.speed = int(self.speed_slider.get_current_value())
            elif event.ui_element == self.grid_size_slider:
                self.grid_size = int(self.grid_size_slider.get_current_value())
                self.reset()
            elif event.ui_element == self.cell_size_slider:
                self.cell_size = int(self.cell_size_slider.get_current_value())
                self.reset()


    def simulation(self):
        while self.sim_running:
            self.iteration += 1
            self.update_iteration_label()
            added = False

            new_grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]

            for y in range(self.grid_size):
                for x in range(self.grid_size):
                    alive = self.count_alive_neighbours(x, y)

                    if self.grid[y][x] == 1 and alive in (2, 3):
                        new_grid[y][x] = 1
                        added = True

                    elif self.grid[y][x] == 0 and alive == 3:
                        new_grid[y][x] = 1
                        added = True

            self.grid = new_grid

            if not added:
                self.sim_running = False

            pygame.time.wait(1000 // self.speed)
            print(self.speed)

    def load_preset(self, preset_name):
        self.reset()

        center_x = self.grid_size // 2
        center_y = self.grid_size // 2

        for x, y in PRESETS[preset_name]:
            self.grid[center_y + y][center_x + x] = 1

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


if __name__ == "__main__":
    life = Life()
    life.run()