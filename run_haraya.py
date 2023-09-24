import subprocess

def run_haraya():
    # Run the Python interpreter in an integrated terminal
    result = subprocess.run(['python', 'haraya_v4.py'], shell=True)

    # Print the output of the command
    print(result.stdout)

if __name__ == '__main__':
    run_haraya()
#Run command: python run_haraya.py
#pip install pyinstaller
#Make an executable file:_____________python -m PyInstaller run_haraya.py --onefile
#go to start up folder: shell:common startup
