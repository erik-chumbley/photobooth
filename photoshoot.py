import pygame
import math
from settings import *

class PhotoShoot:
    def __init__(self, camera_controller=None):
        self.shoot_stage = 0
        self.running = False
        self.start_time = None
        self.last_second_displayed = None
        self.font = pygame.font.Font(None, 150)
        self.remaining_seconds = 0
        self.elapsed_ms = 0
        self.camera_controller = camera_controller

    def run(self):
        if self.shoot_stage == 0:
            self.set_start_time()
            self.shoot_stage += 1
        else:
            self.elapsed_ms = pygame.time.get_ticks() - self.start_time
            self.remaining_seconds = math.ceil(COUNTDOWN - (self.elapsed_ms / 1000.0))
            self.last_second_displayed = self.remaining_seconds
            if self.remaining_seconds <= 0:
                self.remaining_seconds = 0
                self.set_start_time()
                if self.shoot_stage < PHOTOS:
                    print(f"Snap photo {self.shoot_stage}")
                    if ENABLECAM: self.camera_controller.capture_image()
                elif self.shoot_stage >= PHOTOS:
                    print(f"Snap photo {self.shoot_stage}")
                    if ENABLECAM: self.camera_controller.capture_image()
                    self.running = False
                    self.start_time = None
                    self.last_second_displayed = None
                    self.shoot_stage = 0
                    return
                self.shoot_stage += 1

    def set_start_time(self):
        self.start_time = pygame.time.get_ticks()

    def draw_countdown(self, screen):
        cd_surface = self.font.render(str(self.remaining_seconds), True, (255, 255, 255))
        cd_surface = cd_surface.convert_alpha()
        cd_surface.set_alpha(self.calculate_alpha())
        cd_rect = cd_surface.get_rect()
        cd_rect.center = (WIDTH // 2, HEIGHT // 2)
        if self.remaining_seconds > 0: screen.blit(cd_surface, cd_rect)

    def calculate_alpha(self):
        current_elapsed_ms = self.elapsed_ms % 1000
        percentage = current_elapsed_ms / 1000.0
        ease = percentage ** 4
        alpha_value = int((1.0 - ease) * 255)
        return alpha_value