import colorama
import subprocess
import psutil


def open_chrome():
    response = "As you wish!"
    print(colorama.Fore.GREEN + response)
    speak(response)
    program = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    try:
        subprocess.Popen([program])
        response = "Opening " + colorama.Fore.RED + "Chrome" + colorama.Fore.GREEN + "..."
        response1 = "Opening " + "Chrome..."
        print(colorama.Fore.GREEN + response)
        speak(response1)
    except FileNotFoundError:
        print("Google Chrome not found. Please check your installation.")
    except Exception as e:
        print("An error occurred while trying to open Chrome:", str(e))

def close_chrome():
    response = "Closing " + colorama.Fore.RED + "Chrome" + colorama.Fore.GREEN + "..."
    response1 = "Closing " + "Chrome..."
    print(colorama.Fore.GREEN + response)
    speak(response1)

    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'] == 'chrome.exe':
            try:
                process.kill()
                response = "Chrome has been closed."
                print(colorama.Fore.GREEN + response)
                speak(response)
            except psutil.AccessDenied:
                print("Permission denied. Unable to close Chrome.")
            except psutil.NoSuchProcess:
                print("Chrome is not running.")
            break
    else:
        print("Chrome is not running.")

if __name__ == "__main__":
    colorama.init(autoreset=True)  # Initialize colorama for colored text
    command = input("Enter your command: ").lower()
    if "open" in command or "access" in command:
        print(colorama.Fore.RED + command)
        command = command.replace("open", '').replace("access", '').strip()
        if "chrome" in command:
            open_chrome()
        # Add more conditions for opening other programs based on the user's command
        else:
            print("Command not recognized or program not supported.")
    elif "close it" in command:
        close_chrome()
    else:
        print("Command not recognized.")

#_____________python test23.py