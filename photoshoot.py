import pygame
import math

class PhotoShoot:
    def __init__(self):
        self.shoot_stage = 0
        self.countdown_seconds = 5
        self.running = False
        self.start_time = None
        self.last_second_displayed = None

    def run(self):
        if self.shoot_stage == 0:
            self.set_start_time()
            self.shoot_stage += 1

        else:
            elapsed_ms = pygame.time.get_ticks() - self.start_time
            remaining_seconds = math.ceil(self.countdown_seconds - (elapsed_ms / 1000.0))
            if remaining_seconds != self.last_second_displayed: print(f"Countdown: {remaining_seconds}!")
            self.last_second_displayed = remaining_seconds
            if remaining_seconds <= 0:
                remaining_seconds = 0
                self.set_start_time()
                if self.shoot_stage == 1:
                    print("Snap photo 1")
                elif self.shoot_stage == 2:
                    print("Snap photo 2")
                elif self.shoot_stage == 3:
                    print("Snap photo 3")
                    self.running = False
                    self.start_time = None
                    self.last_second_displayed = None
                    self.shoot_stage = 0
                self.shoot_stage += 1

    def set_start_time(self):
        self.start_time = pygame.time.get_ticks()
