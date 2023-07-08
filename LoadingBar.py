import math

def RunLoadingBar(seconds = 15, loading_tag = "Loading", end_tag = "Loaded successfully", finish_loading = False):
    print("\n")
    def progressBar(progress, total):
        percent = 100 * (progress / float(total))
        bar = '█' * int(percent) + '·' * (100 - int(percent))
        if percent != 100:
            print(f"\r {loading_tag}...|{bar}| {percent:.2f}%              ", end="\r")
        else:
            print(f"\r {end_tag}:|{bar}| {percent:.2f}%              ", end="\r")
    
    if finish_loading == True:
        seconds = 0.5
    numbers = [x * int(seconds*2.3) for x in range(1000)]
    results = []
    progressBar(0, len(numbers))
    for i, x in enumerate(numbers):
        results.append(math.factorial(x))
        progressBar(i+1, len(numbers))
    print("\n")
    
if __name__ == '__main__':
    RunLoadingBar(finish_loading=False)
#____________python LoadingBar.py