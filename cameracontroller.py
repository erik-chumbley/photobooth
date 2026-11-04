import io
import os
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
        self.file_path = None

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

    def capture_image_alt(self, target_path="/tmp/photo.jpg"):
        print('Capturing image')
        file_path = self.camera.capture(gp.GP_CAPTURE_IMAGE)
        print(f"Captured: {file_path.folder}/{file_path.name}")

        camera_file = self.camera.file_get(
            file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL
        )
        camera_file.save(target_path)
        print(f"Saved to {target_path}")

    def capture_image(self):
        self.file_path = self.camera.trigger_capture()
        print("Capture triggered. Waiting for event...")

    def camera_event_listener(self):
        event_type, data = self.camera.wait_for_event(1000)
        if event_type == gp.GP_EVENT_FILE_ADDED:
            print(f"File created on camera: {data.folder}/{data.name}")
            camera_file = self.camera.file_get(
                data.folder, data.name, gp.GP_FILE_TYPE_NORMAL
            )
            camera_file.save(data.name)
            print(f"Downloaded {data.name} locally.")