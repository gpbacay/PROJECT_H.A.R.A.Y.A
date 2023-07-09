import math
from playsound import playsound
from threading import Thread
import time
import sys

def LoadingBar(seconds=15, loading_tag="Loading", end_tag="Loaded successfully", finish_loading=False):
    def RunLoadingBar(seconds=15, loading_tag="Loading", end_tag="Loaded successfully", finish_loading=False):
        print("\n")
        def progressBar(progress, total):
            percent = 100 * (progress / float(total))
            bar = '█' * int(percent) + '·' * (100 - int(percent))
            if percent != 100:
                print(f"\r {loading_tag}...|{bar}| {percent:.2f}%              ", end="\r")
            else:
                print(f"\r {end_tag}:|{bar}| {percent:.2f}%              ", end="\r")
                print("\n")
                playsound(U"loadcomplete.mp3")
                sys.exit()

        if finish_loading:
            seconds = 0.5
        numbers = [x * int(seconds * 2.3) for x in range(1000)]
        results = []
        progressBar(0, len(numbers))
        for i, x in enumerate(numbers):
            results.append(math.factorial(x))
            progressBar(i + 1, len(numbers))
    
    t1 = Thread(target=playsound, args=(U"loadbar.mp3",), daemon=True)
    t1.start()
    
    time.sleep(1)
    t2 = Thread(target=RunLoadingBar, args=(seconds,loading_tag,end_tag,finish_loading))
    t2.start()
    t2.join()
    
if __name__ == '__main__':
    LoadingBar()
        
#____________python LoadingBar.py