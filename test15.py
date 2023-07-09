import math
from playsound import playsound
from threading import Thread
import time

class test15():
    def Runtest15(seconds=15, loading_tag="Loading", end_tag="Loaded successfully", finish_loading=False):
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
                exit()

        if finish_loading:
            seconds = 0.5
        numbers = [x * int(seconds * 2.3) for x in range(1000)]
        results = []
        progressBar(0, len(numbers))
        for i, x in enumerate(numbers):
            results.append(math.factorial(x))
            progressBar(i + 1, len(numbers))
    
    t1 = Thread(target=playsound, args=(U"loadbar.mp3",))
    t1.daemon = True
    t1.start()
    
    time.sleep(1)
    t2 = Thread(target=Runtest15, args=(1,"Loading", "Loading completed"))
    t2.start()
    t2.join()
    
if __name__ == '__main__':
    test15()
        
#____________python test15.py