import pygame_gui

class UIManager:
    def __init__(self, width, height):
        self.manager = pygame_gui.UIManager((width, height), 'theme.json')