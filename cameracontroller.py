import io
import sys
import pygame
import gphoto2 as gp
from PIL import Image

class CameraController:
    def __init__(self):
        print("Connecting to camera... Make sure it is turned on and connected via USB.")
        try:
            self.camera = gp.Camera()
            self.camera.init()
            print(f"Connected to: {str(self.camera.get_summary())[:50]}...")
        except gp.GPhoto2Error as e:
            print(f"Camera error: {e}")
            print("Ensure no other application (like Darktable or a webcam utility) is locking the camera.")
            sys.exit(1)

    def display_preview(self, screen):
        try:
            camera_file = self.camera.capture_preview()
            file_data = camera_file.get_data_and_size()
            image_data = io.BytesIO(file_data)
            pil_img = Image.open(image_data)

            mode = pil_img.mode
            size = pil_img.size
            data = pil_img.tobytes()
            pygame_surface = pygame.image.fromstring(data, size, mode)

            window_width, window_height = screen.get_size()
            scaled_surface = pygame.transform.scale(pygame_surface, (window_width, window_height))

            screen.blit(scaled_surface, (0, 0))

        except gp.GPhoto2Error as e:
            print(f"Frame drop or error: {e}")

    def close_camera(self):
        print("Closing camera connection...")
        self.camera.exit()