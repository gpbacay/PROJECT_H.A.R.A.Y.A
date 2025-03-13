import math
import time
from threading import Thread
import colorama
from sound_system import SoundSystem

colorama.init(autoreset=True)

class LoadingBar:
    def __init__(self, seconds: int = 15, loading_tag: str = "LOADING", end_tag: str = "LOADING COMPLETE!", finished_loading: bool = False) -> None:
        """
        Initializes the LoadingBar with default customizable parameters.

        :param seconds: Default duration for the simulated work.
        :param loading_tag: Default tag to display during loading.
        :param end_tag: Default tag to display upon completion.
        :param finished_loading: Default flag to reduce duration.
        """
        self.seconds = seconds
        self.loading_tag = loading_tag
        self.end_tag = end_tag
        self.finished_loading = finished_loading
        self.sound_system = SoundSystem()  # Instance to handle audio cues

    def _progress_bar(self, progress: int, total: int, loading_tag: str, end_tag: str) -> None:
        """
        Updates the progress bar display and plays the complete sound when finished.
        """
        percent = 100 * (progress / float(total))
        bar = '█' * int(percent) + '░' * (100 - int(percent))
        if percent < 100:
            print(colorama.Fore.LIGHTRED_EX + f"\r {loading_tag} │{bar}│{percent:.2f}%              ", end="\r")
        else:
            print(colorama.Fore.LIGHTGREEN_EX + f"\r {end_tag} │{bar}│{percent:.2f}%              ", end="\r")
            print("\n")
            self.sound_system.playLoadCompleteSound()

    def run_loadingbar(self, seconds: int = None, loading_tag: str = None, end_tag: str = None, finished_loading: bool = None) -> None:
        """
        Runs the simulated loading bar while performing a dummy workload.
        Allows overriding default parameters.

        :param seconds: Duration for the simulated work.
        :param loading_tag: Tag to display during loading.
        :param end_tag: Tag to display upon completion.
        :param finished_loading: Flag to reduce duration.
        """
        # Use provided arguments if given; otherwise, fallback to instance defaults.
        seconds = seconds if seconds is not None else self.seconds
        loading_tag = loading_tag if loading_tag is not None else self.loading_tag
        end_tag = end_tag if end_tag is not None else self.end_tag
        finished_loading = finished_loading if finished_loading is not None else self.finished_loading

        # Play the loading bar sound in a separate thread.
        t1 = Thread(target=self.sound_system.playLoadingBarSound, daemon=True)
        t1.start()
        time.sleep(0.5)

        if finished_loading:
            seconds = 0.5

        # Simulate work by generating a list of numbers.
        numbers = [x * int(seconds * 2.3) for x in range(1000)]
        results = []
        self._progress_bar(0, len(numbers), loading_tag, end_tag)
        for i, x in enumerate(numbers):
            # Simulate a computation (dummy workload)
            results.append(math.factorial(x))
            self._progress_bar(i + 1, len(numbers), loading_tag, end_tag)
        print(colorama.Fore.RESET)

if __name__ == '__main__':
    # Create an instance of LoadingBar.
    loading_bar = LoadingBar()
    
    # Create a thread to run the loading bar concurrently.
    thread = Thread(
        target=loading_bar.run_loadingbar,
        kwargs={
            "seconds": 5,
            "loading_tag": "PROCESSING",
            "end_tag": "PROCESS COMPLETE!",
        }
    )
    
    # Start and wait for the thread to complete.
    thread.start()
    thread.join()
    
    print("Loading bar has finished running in the thread.")


#____________pip install colorama
#____________python loading_bar.py