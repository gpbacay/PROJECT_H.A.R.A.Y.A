import math
from playsound import playsound
from threading import Thread
import time
import colorama
colorama.init(autoreset=True)

class LoadingBar():
    def RunLoadingBar(seconds=15, loading_tag="LOADING", end_tag="LOADED SUCCESSFULLY!", finish_loading=False):
        t1 = Thread(target=playsound, args=(u"audioFiles\\loadingbar.mp3",), daemon=True)
        t1.start()
        time.sleep(0.5)
        def progressBar(progress, total):
            percent = 100 * (progress / float(total))
            bar = '█' * int(percent) + '░' * (100 - int(percent))
            if percent <= 50:
                print(colorama.Fore.LIGHTRED_EX + f"\r {loading_tag}...│{bar}│{percent:.2f}%              ", end="\r")
            elif percent == 100:
                print(colorama.Fore.LIGHTGREEN_EX + f"\r {end_tag}│{bar}│{percent:.2f}%              ", end="\r")
                print("\n")
                playsound(u"audioFiles\\loadcomplete.mp3")

        if finish_loading:
            seconds = 0.5
        numbers = [x * int(seconds * 2.3) for x in range(1000)]
        results = []
        progressBar(0, len(numbers))
        for i, x in enumerate(numbers):
            results.append(math.factorial(x))
            progressBar(i + 1, len(numbers))
        print(colorama.Fore.RESET)
    
if __name__ == '__main__':
    LoadingBar.RunLoadingBar(10)

#____________pip install colorama
#____________python LoadingBar.py