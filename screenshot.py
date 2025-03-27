from PIL import ImageGrab
from sound_system import SoundSystem
import os

def take_screenshot():
    sound_system = SoundSystem()
    try:
        snapshot = ImageGrab.grab()
        sound_system.playCameraShutterSound()
        save_path = r".\screenshots\screenshot.jpg"
        snapshot.save(save_path, "JPEG")
        print(f"Screenshot taken and saved to {save_path}.")
        os.startfile(save_path)
    except Exception as e:
        print(f"An error occurred while taking a screenshot: {e}")

if __name__ == "__main__":
    take_screenshot()

# python screenshot.py