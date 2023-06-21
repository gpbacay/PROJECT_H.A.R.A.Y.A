import subprocess

def run_haraya():
    # Run the Python interpreter in an integrated terminal
    result = subprocess.run(['python', 'haraya.py'], shell=True)

    # Print the output of the command
    print(result.stdout)

if __name__ == '__main__':
    run_haraya()
#Run command: python run_haraya.py
#Make an executable file:_____________pyinstaller --onefile run_haraya.py
#go to start up folder: shell:common startup
