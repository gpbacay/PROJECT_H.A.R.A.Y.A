import cv2
import os
from sound_system import SoundSystem

def take_snapshot():
    sound_system = SoundSystem()
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not access the camera.")
        return

    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read a frame from the camera.")
        cap.release()
        return

    save_path = r".\snapshots\snapshot.jpg"
    cv2.imwrite(save_path, frame)
    sound_system.playCameraShutterSound()
    print(f"Snapshot taken and saved to {save_path}.")

    cap.release()

    try:
        os.startfile(save_path)
    except Exception as e:
        print(f"Error displaying the image: {e}")

if __name__ == "__main__":
    take_snapshot()

# python snapshot.py