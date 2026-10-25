import pygame
import pygame_gui
from settings import *

class PhotoShootButton:
    def __init__(self, ui_manager):
        self.create_button(ui_manager)

    def create_button(self, ui_manager):
        btn_diam = 100
        x_pos = (WIDTH - btn_diam) / 2
        y_pos = (HEIGHT - btn_diam) - 25
        self.button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((x_pos, y_pos), (btn_diam, btn_diam)),
            text='Snap!',
            manager=ui_manager,
            object_id='#circular_button'
        )