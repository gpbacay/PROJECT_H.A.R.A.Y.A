import cv2
from sound_system import SoundSystem

def take_snapshot():
    sound_system = SoundSystem()
    # Open the default camera (index 0)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not access the camera.")
        return

    # Read a frame from the camera
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read a frame from the camera.")
        cap.release()
        return

    # Define the path where the snapshot will be saved
    save_path = r".\\snapshots\\snapshot.jpg"
    # Save the captured frame as an image file
    cv2.imwrite(save_path, frame)
    sound_system.playCameraShutterSound()
    print(f"Snapshot taken and saved to {save_path}.")

    # Release the camera resource
    cap.release()

if __name__ == "__main__":
    take_snapshot()

# python snapshot.py