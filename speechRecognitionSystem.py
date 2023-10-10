# speechRecognitionSystem
import speech_recognition as sr
import colorama



class speechRecognitionSystem:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        colorama.init(autoreset=True)
        
    def listenCommand(self):
        global command
        command = ""
        try:
            with sr.Microphone() as source:
                print(colorama.Fore.CYAN + "Listening...")
                print(colorama.Fore.RED + "\nNote: Toggle [F9] to stop/start listening.\n")
                self.recognizer.energy_threshold = 1.0
                self.recognizer.pause_threshold = 0.8
                voice = self.recognizer.listen(source)
                command = self.recognizer.recognize_google(voice)
                command = command.lower()
        except Exception as e:
            print(e)
            pass
        return command
    
sRS = speechRecognitionSystem()

while True:
    command = sRS.listenCommand()
    if command:
        print(command)

# python speechRecognitionSystem.py
