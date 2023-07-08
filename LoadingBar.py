import math

def RunLoadingBar(seconds = 10):
    print("\n")
    def progressBar(progress, total):
        percent = 100 * (progress / float(total))
        bar = '█' * int(percent) + '-' * (100 - int(percent))
        if percent == 100:
            print(f"\r Done Loading:|{bar}| {percent:.2f}%", end="\r")
        else:
            print(f"\r Loading:|{bar}| {percent:.2f}%", end="\r")
        
    numbers = [x * int(seconds*2.3) for x in range(1000)]
    results = []
    progressBar(0, len(numbers))
    for i, x in enumerate(numbers):
        results.append(math.factorial(x))
        progressBar(i+1, len(numbers))
    print("\n")
if __name__ == '__main__':
    RunLoadingBar()
#____________python LoadingBar.py