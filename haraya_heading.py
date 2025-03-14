import threading
import colorama
from sound_system import SoundSystem  # Import SoundSystem for audio playback

class HarayaHeading:
    def __init__(self):
        """
        Initializes the HarayaHeading module.
        - Starts a thread to play the startup sound.
        - Displays the header in a separate thread.
        """
        colorama.init(autoreset=True)  # Ensure colors reset after usage
        self.sound_system = SoundSystem()  # Create an instance of SoundSystem

        self.header_str = (
            "\t\t\t\tH.A.R.A.Y.A "
            "(High-functioning Autonomous Responsive Anthropomorphic Yielding Assistant)\t\t\t\t\n"
        )
        self.header = colorama.Style.BRIGHT + colorama.Fore.GREEN + self.header_str

        # Start the startup sound in a separate thread
        self.t_startup = threading.Thread(target=self.sound_system.playStartUpSound)
        self.t_startup.start()

        # Start the header display in a separate thread
        self.t_header = threading.Thread(target=self.display_header)
        self.t_header.start()

    def display_header(self):
        """Prints the header string to the console."""
        print(self.header)


# If this module is run directly, test the functionality
if __name__ == "__main__":
    haraya_heading = HarayaHeading()

# Run Command: python haraya_heading.py