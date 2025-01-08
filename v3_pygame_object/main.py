from threading import Thread

import pygame
import pygame_gui

from ControlUI import ControlUI
from Grid import Grid


from conf import *

class GameOfLife:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Game of Life")

        self.manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.ui = ControlUI(self.manager)
        self.grid = Grid(WINDOW_WIDTH - CONTROL_PANEL_SIZE, INITIAL_GRID_CELLS_NUMBER)

        self.is_running = True
        self.sim_running = False
        self.speed = 5
        self.iteration = 0

        self.clock = pygame.time.Clock()

        self.ui.create_ui()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            grid_margin = (self.grid.grid_size - self.grid.cells_number * self.grid.cell_size) // 2

            grid_x, grid_y = int((x - grid_margin) // self.grid.cell_size), int(
                (y - grid_margin) // self.grid.cell_size)
            if 0 <= grid_x < self.grid.cells_number and 0 <= grid_y < self.grid.cells_number:
                self.grid.grid[grid_y][grid_x] = 1 - self.grid.grid[grid_y][grid_x]

        elif event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.ui.start_button:
                self.start_simulation()
            elif event.ui_element == self.ui.stop_button:
                self.sim_running = False
            elif event.ui_element == self.ui.reset_button:
                self.reset()
            elif event.ui_element == self.ui.save_button:
                self.grid.save()

        elif event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == self.ui.color_mode_menu:
                self.grid.set_color_mode(event.text)
            if event.ui_element == self.ui.preset_menu:
                self.reset()
                self.grid.load_preset(event.text)


        elif event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            if event.ui_element == self.ui.speed_slider:
                self.speed = int(self.ui.speed_slider.get_current_value())
            elif event.ui_element == self.ui.grid_cells_slider:
                self.grid.scale_grid(int(self.ui.grid_cells_slider.get_current_value()))

    def load_preset(self, preset_name):
        error = self.grid.load_preset(preset_name)
        if error:
            self.ui.iteration_label.set_text(error)


    def reset(self):
        self.sim_running = False
        self.grid.reset_grid()
        self.iteration = 0
        self.ui.iteration_label.set_text(f'Iteration: {self.iteration}')

    def update_iteration_label(self):
        self.ui.iteration_label.set_text(f'Iteration: {self.iteration}')

    def simulation(self):
        print(self.speed)
        while self.sim_running:
            self.iteration += 1
            self.update_iteration_label()
            if not self.grid.simulation(): self.sim_running = False
            self.clock.tick(self.speed)

    def start_simulation(self):
        self.sim_running = True
        Thread(target=self.simulation).start()

    def run(self):
        while self.is_running:
            time_delta = self.clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                self.handle_event(event)
                self.manager.process_events(event)

            self.screen.fill((33, 40, 45))
            self.grid.draw(self.screen)

            self.manager.update(time_delta)
            self.manager.draw_ui(self.screen)

            pygame.display.flip()

        pygame.quit()

if __name__ == '__main__':
    game = GameOfLife()
    game.run()