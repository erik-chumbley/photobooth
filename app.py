import sys
import pygame
import pygame_gui
from settings import *
from cameracontroller import CameraController
from uimanager import UIManager
from photoshootbutton import PhotoShootButton
from photoshoot import PhotoShoot

class App:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))#, pygame.FULLSCREEN | pygame.SCALED)
        self.clock = pygame.time.Clock()
        self.running = True
        if ENABLECAM:
            self.cameracontroller = CameraController()
            self.photoshoot = PhotoShoot(self.cameracontroller)
        else:
            self.photoshoot = PhotoShoot()
        self.ui = UIManager(WIDTH, HEIGHT)
        self.photoshootbutton = PhotoShootButton(self.ui.manager)

    def run(self):
        while self.running:
            td = self.clock.tick(FPS)/1000.0
            self.handle_events()
            self.update(td)
            self.draw()
        if ENABLECAM: self.cameracontroller.close_camera()
        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.photoshootbutton.button:
                    self.photoshoot.running = True
            self.ui.manager.process_events(event)
        # if ENABLECAM: self.cameracontroller.camera_event_listener()

    def update(self, time_delta):
        self.ui.manager.update(time_delta)
        self.photoshootbutton.update_button_visibility()
        if self.photoshoot.running:
            self.photoshoot.run()
            self.photoshootbutton.hidden = True
        else: self.photoshootbutton.hidden = False

    def draw(self):
        self.screen.fill((0, 100, 255))
        if ENABLECAM: self.cameracontroller.display_preview(self.screen)
        self.ui.manager.draw_ui(self.screen)
        self.photoshoot.draw_countdown(self.screen)
        pygame.display.flip()