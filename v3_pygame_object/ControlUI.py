import pygame
import pygame_gui

from conf import *
from v3_pygame_object.presets import PRESETS

class ControlUI:

    def __init__(self, manager):

        self.manager = manager

        self.iteration = 0

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
            start_value=INITIAL_SPEED,
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
            start_value=INITIAL_GRID_CELLS_NUMBER,
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
            starting_option="black",
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
            text=f'Iteration: 0',
            manager=self.manager, container=self.controls_panel,
            anchors={"left": "left", "bottom": "bottom", "right": "right"}
        )