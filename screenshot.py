from PIL import ImageGrab
from sound_system import SoundSystem
import os

def take_screenshot():
    sound_system = SoundSystem()
    try:
        # Capture the screen
        snapshot = ImageGrab.grab()
        sound_system.playCameraShutterSound()
        # Define the path where the screenshot will be saved
        save_path = r".\screenshots\screenshot.jpg"
        # Save the screenshot to the specified path in JPEG format
        snapshot.save(save_path, "JPEG")
        print(f"Screenshot taken and saved to {save_path}.")
        # Open the screenshot using the default image viewer (Windows)
        os.startfile(save_path)
    except Exception as e:
        print(f"An error occurred while taking a screenshot: {e}")

if __name__ == "__main__":
    take_screenshot()

# python screenshot.py