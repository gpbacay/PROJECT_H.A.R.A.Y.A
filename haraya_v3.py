# Import Necessary Libraries/Modules
# Run Command: python haraya_v3.py
from threading import Thread
import time
from playsound import playsound
import speech_recognition as sr
import pywhatkit
import pyttsx3
from facerec import Face_Recognition_System
from poserec import Pose_Recognition_System
import os
import subprocess
import psutil
import wikipedia
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from loadingBar import LoadingBar
import colorama
import pygame
from pygame.locals import *
import pyautogui
from harayaUI import harayaUI
from PaLM2_LLM import PaLM2_LLM
import harayaVoiceEngine as harayaVoiceEngine

class haraya_v3:
    # Constructor Definition Block
    #Run Command: python haraya_v3.py
    def __init__(self):
        self.command = "."
        self.NameHA = "."
        self.MyName = "."
        self.tStartUp = Thread(target=playsound, args=(u"audioFiles\\prompt1.mp3",))
        self.tStartUp.start()
        colorama.init(autoreset=True)
        self.HeaderStr = "\t\t\t\tH.A.R.A.Y.A (High-functioning Autonomous Responsive Anthropomorphic Yielding Assistant)\t\t\t\t\n"
        self.Header = colorama.Style.BRIGHT + colorama.Fore.GREEN + self.HeaderStr
        self.tHeader = Thread(target=print, args=(self.Header,))
        self.tHeader.start()
        self.PaLM2_LLM = PaLM2_LLM()
        # Attributes Declaration Block
        # Run Command: python haraya_v3.py
        pygame.init()
        self.setIsRandom = harayaUI.setIsRandom
        self.runUI = harayaUI.runUI
        self.tGUI = Thread(target=self.runUI, daemon=True)
        self.tGUI.start()
        self.runLoadingBar = LoadingBar.RunLoadingBar
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voices[2].id)
        self.hveSpeak = harayaVoiceEngine.Speak
        # Lists Attributes Initialization Block
        # Run Command: python haraya_v3.py
        self.Name = []
        self.Name_Honorific_Address = []
        self.NameList = []
        # Lists of Command Keywords
        # Run Command: python haraya_v3.py
        self.Standby_HotWords = ["standby", 
                                "haraya stand by", 
                                "just stand by", "wait", 
                                "wait a sec", 
                                "give me a sec", 
                                "hold for a sec", 
                                "wait for a sec", 
                                "give me a second", 
                                "hold for a second", 
                                "wait for a second", 
                                "give me a minute", 
                                "hold for a minute",
                                "wait for a minute", 
                                "give me an hour", 
                                "hold for an hour", 
                                "wait for an hour", 
                                "just a moment",
                                "just a sec", 
                                "just a minute",
                                "just an hour", 
                                "call you later", 
                                "i'll be back", 
                                "be right back"]
        self.GoodBye_HotWords = ["goodbye", 
                                "good bye", 
                                "haraya goodbye", 
                                "goodbye haraya", 
                                "haraya bye", 
                                "bye haraya", 
                                "bye", 
                                "let's call it a day",
                                "i said goodbye", 
                                "you're good to go", 
                                "you can go", 
                                "you can go now", 
                                "you can go to sleep now", 
                                "i need to go", 
                                "ciao", 
                                "sayonara"]
        self.Stop_HotWords = ["sign off", 
                            "haraya stop",
                            "stop please", 
                            "go to sleep",
                            "go to rest",
                            "just go to sleep",
                            "just go to rest", 
                            "go to sleep haraya", 
                            "stop listening",
                            "terminate yourself",
                            "enough",
                            "that's enough",
                            "I said enough",
                            "I said stop",
                            "you can go to sleep now", 
                            "i told you to go to sleep", 
                            "didn't i told you to go to sleep", 
                            "didn't i told you to sleep", 
                            "i told you to stop", 
                            "didn't i told you to stop",
                            "turn off", 
                            "shutdown"]
        self.Yes_HotWords = ["yes", 
                            "yup",
                            "yes please",
                            "of course yes", 
                            "yes I do",
                            "I do", 
                            "you got it right", 
                            "yes actually", 
                            "actually yes", 
                            "that's a yes", 
                            "I think yes", 
                            "sure", 
                            "yah",
                            "absolutely yes", 
                            "definitely yes",
                            "you got it right", 
                            "I said yes",
                            "affirmative"]
        self.No_HotWords = ["no",
                            "nope", 
                            "no please", 
                            "of course no", 
                            "no I don't", 
                            "I don't think so", 
                            "you got it wrong", 
                            "no actually", 
                            "actually no", 
                            "that's a no", 
                            "I'm not",
                            "I think not", 
                            "none so far", 
                            "I'm not sure",
                            "noh", 
                            "nah",
                            "none", 
                            "that's a no no",
                            "absolutely no", 
                            "definitely no", 
                            "absolutely not",
                            "definitely not",
                            "incorrect",
                            "I said no",
                            "negative"]
        self.Haraya_HotWords = ["haraya",
                                "araya", 
                                "mariah", 
                                "meriah",
                                "hiraya",
                                "raya", 
                                "yaya", 
                                "heraya", 
                                "area", 
                                "ryan", 
                                "aya", 
                                "heria", 
                                "herya", 
                                "halaya"]
        self.GoogleSearch_HotWords = ["in google search",
                                    "search in google", 
                                    "in google navigate",
                                    "navigate in google", 
                                    "in google find", 
                                    "find in google", 
                                    "in google", 
                                    "google search", 
                                    "go on google", 
                                    "go in google", 
                                    "on google",
                                    "search in chrome", 
                                    "go in chrome", 
                                    "go on chrome"]
        self.YouTubeSearch_HotWords = ["in youtube search", 
                                    "search in youtube", 
                                    "in youtube play", 
                                    "play in youtube", 
                                    "in youtube find", 
                                    "find in youtube", 
                                    "in youtube", 
                                    "youtube search",
                                    "go on youtube",
                                    "go in youtube", 
                                    "on youtube"]
        self.WikipediaSearch_HotWords = ["in wikipedia search",
                                        "search in wikipedia", 
                                        "in wikipedia find", 
                                        "find in wikipedia", 
                                        "in wikipedia",
                                        "wikipedia search",
                                        "go on wikipedia", 
                                        "on wikipedia"]
        self.Open_HotWords = ["open", 
                            "access", 
                            "go to", 
                            "go in",
                            "run", 
                            "launch"]
        self.Close_HotWords = ["close", 
                            "terminate", 
                            "go out", 
                            "exit", 
                            "escape",
                            "quit", 
                            "return",
                            "close"]
    # Methods Implementation Block
    # Run Command: python haraya_v3.py
    # def speak(self, text):
    #     self.setIsRandom(1)
    #     self.engine.say(text)
    #     self.engine.runAndWait()
    #     self.setIsRandom(0)
    def speak(self, text_input):
        tSpeak = Thread(target=self.hveSpeak, args=(text_input,))
        tSpeak.start()
        time.sleep(1)
        tSpeaking = Thread(target=self.setIsRandom, args=(1,))
        tSpeaking.start()
        tSpeak.join()
        self.setIsRandom(0)
    # LISTEN_COMMAND_MAIN_FUNCTION
    # Run Command: python haraya_v3.py
    def listenCommand(self):
        command = self.command
        try:
            with sr.Microphone() as source:
                print(colorama.Fore.CYAN + "Listening...")
                print(colorama.Fore.RED + "\nNote: Toggle [F9] to stop/start listening.\n")
                self.playListeningSound()
                self.recognizer.energy_threshold = 1.0
                self.recognizer.pause_threshold = 0.8
                voice = self.recognizer.listen(source)
                command = self.recognizer.recognize_google(voice)
                command = command.lower()
        except:
            pass
        return command
    # ADD_COMMAND_MAIN_FUNCTION
    # Run Command: python haraya_v3.py
    def addCommand(self, command):
        Interrogative_HotWords = ['what', ' what ', 'what ', ' what',
                                'who', ' who ', 'who ', ' who',
                                'where', ' where ', 'where ', ' where',
                                'when', ' when ', 'when ', ' when',
                                'why', ' why ', 'why ', ' why',
                                'how', ' how ', 'how ', ' how']
        try:
            if any(hotword in command for hotword in Interrogative_HotWords):
                response = "Is there anything specific you would like to know or ask?"
                print(colorama.Fore.GREEN + response)
                self.speak(response)
            if (hotword not in command for hotword in Interrogative_HotWords):
                response = "Is there anything else I could do for you?"
                print(colorama.Fore.GREEN + response)
                self.speak(response)
            else:
                response = ''
                print(response)
                self.speak(response)
            with sr.Microphone() as source:
                print(colorama.Fore.CYAN + "Listening...")
                print(colorama.Fore.RED + "\nNote: Toggle [F9] to stop/start listening.\n")
                self.playListeningSound()
                self.recognizer.energy_threshold = 1.0
                self.recognizer.pause_threshold = 0.8
                voice = self.recognizer.listen(source)
                command = self.recognizer.recognize_google(voice)
                command = command.lower()
        except:
            pass
        return command
    # WAIT_COMMAND_MAIN_FUNCTION
    # Run Command: python haraya_v3.py
    def waitCommand(self):
        command = self.command
        try:
            with sr.Microphone() as source:
                print(colorama.Fore.CYAN + "Waiting...")
                print(colorama.Fore.RED + "\nNote: Toggle [F9] to stop/start listening.\n")
                self.recognizer.energy_threshold = 1.0
                self.recognizer.pause_threshold = 0.8
                voice = self.recognizer.listen(source)
                command = self.recognizer.recognize_google(voice)
                command = command.lower()
        except:
            pass
        return command
    # AUDIO_EFFECTS_BLOCK/FUNCTION
    # Run Command: python haraya_v3.py
    def playPromptSound(self):
        mp3_path = u"audioFiles\\prompt1.mp3"
        playsound(mp3_path)
    def playListeningSound(self):
        mp3_path = u"audioFiles\\Listening.mp3"
        playsound(mp3_path)
    def playShutdownSound(self):
        mp3_path = u"audioFiles\\shutdown.mp3"
        playsound(mp3_path)
    def playSearchSound(self):
        mp3_path = u"audioFiles\\searching.mp3"
        playsound(mp3_path)
    # FACE_RECOGNITION_BLOCK/FUNCTION
    # Run Command: python haraya_v3.py
    def getFullName(self):
        with open("attendance.csv", "r+") as attendance:
            MyDatalist = attendance.readlines()
            self.NameList.append(MyDatalist[-1])
            
            MyFullName = self.NameList[-1].replace("'", '').split(",")[0]
            self.Name.append(MyFullName)
            self.MyName = MyFullName
    # Binary-GendeLIGHTGREEN_EX_Honorifics_Selector_BLOCK/FUNCTION
    # Run Command: python haraya_v3.py
    def setHonorificAddress(self):
        Male_Names = ["Gianne Bacay", "Earl Jay Tagud", "Gemmuel Balceda", "Mark Anthony Lagrosa",
                    "Klausmieir Villegas", "CK Zoe Villegas", "Pio Bustamante", "Rolyn Morales",
                    "Alexander Villasis", "Bryan Sarpamones"]
        Female_Names = ["Kleinieir Pearl Kandis Bacay", "Princess Viznar", "Nichi Bacay",
                        "Roz Waeschet Bacay", "Jane Rose Bandoy"]
        try:
            Gender_Name = self.Name[-1]
            if Gender_Name in Male_Names:
                Honorific_Address = "Sir"
            elif Gender_Name in Female_Names:
                Honorific_Address = "Ma'am"
            else:
                Honorific_Address = "Boss"
        except:
            Honorific_Address = "Master"
        self.Name_Honorific_Address.append(Honorific_Address)
    # initializeFaceRecognitionSystem_BLOCK/FUNCTION
    # Run Command: python haraya_v3.py
    def initializeFaceRecognitionSystem(self):
        tFRS = Thread(target=Face_Recognition_System)
        tFRS.start()
        tLoadBar1 = Thread(target=self.runLoadingBar, args=(10, "INITIALIZING FRS", "FRS INITIALIZED!"),)
        tLoadBar1.start()
        response = "Initializing Face Recognition System"
        self.speak(response)
        tFRS.join()
        self.runLoadingBar(0.5, "RECOGNIZING FACE", "FACE RECOGNIZED!")
        self.getFullName()
        self.setHonorificAddress()
    # initializePoseRecognitionSystem_BLOCK/FUNCTION
    # Run Command: python haraya_v3.py
    def initializePoseRecognitionSystem(self):
        response = "Recognizing pose..."
        print(colorama.Fore.GREEN + response)
        tPRS = Thread(target=Pose_Recognition_System)
        tPRS.start()
        tLoadBar2 = Thread(target=self.runLoadingBar, args=(10, "INITIALIZING PRS", "PRS INITIALIZED!"),)
        tLoadBar2.start()
        response = "Initializing Pose Recognition System"
        self.speak(response)
        tPRS.join()
    # START_UP_MAIN_FUNCTION
    # Run Command: python haraya_v3.py
    def harayaStartUp(self):
        try:
            NameHA = self.Name_Honorific_Address[-1]
            MyName = self.Name[-1]
            response = "Hi " + NameHA + " " + colorama.Fore.CYAN + MyName + colorama.Fore.GREEN + "! I am Haraya, how can I help you?"
            response1 = "Hi " + NameHA + " " + MyName + "! I am Haraya, how can I help you?"
        except:
            response = "Hi! How can I help you?"
        print(colorama.Fore.GREEN + response)
        self.speak(response1)
    # STANDBY_SUBFUNCTION
    # Run Command: python haraya_v3.py
    def Standby_SubFunction(self):
        self.playListeningSound()
        while True:
            command = self.waitCommand()
            print(colorama.Fore.LIGHTGREEN_EX + command)
            if "i'm here" in command or any(hotword in command for hotword in self.Haraya_HotWords):
                response = "Yes? How can I help you?"
                print(colorama.Fore.GREEN + response)
                self.speak(response)
                break
        exit(self.harayaNeuralNetwork())
    # CONFIRMATION_SUBFUNCTION
    # Run Command: python haraya_v3.py
    def Confirmation_SubFunction(self, command):
        command = self.addCommand(command)
        
        if any(hotword == command for hotword in self.Yes_HotWords):
            print(colorama.Fore.LIGHTGREEN_EX + command)
            command = command.replace(command, '')
            response = "Then, please do tell."
            print(colorama.Fore.GREEN + response)
            self.speak(response)
            exit(self.harayaNeuralNetwork())
            
        elif any(hotword == command for hotword in self.No_HotWords):
            print(colorama.Fore.LIGHTGREEN_EX + command)
            response = "Alright then, signing off!"
            print(colorama.Fore.GREEN + response)
            self.speak(response)
            exit()
        elif "." == command:
            print(colorama.Fore.LIGHTGREEN_EX + command)
            response = "Hello? Are you still there?"
            print(colorama.Fore.GREEN + response)
            self.speak(response)
            self.Standby_SubFunction()
        else:
            response = "Come again?"
            print(response)
            self.speak(response)
            exit(self.harayaNeuralNetwork())
    #____________________________________________________________________CLOSE_PROGRAM_FUNCTION
    def close_program(self, program_name):
        try:
            response = "Closing " + colorama.Fore.LIGHTGREEN_EX + program_name + colorama.Fore.GREEN + "..."
            response1 = "Closing " + program_name + "..."
            print(colorama.Fore.GREEN + response)
            self.speak(response1)
            for process in psutil.process_iter(['pid', 'name']):
                if process.info['name'] == program_name:
                    try:
                        process.terminate()
                        response = program_name + " has been closed."
                        print(colorama.Fore.GREEN + response)
                        self.speak(response)
                    except psutil.AccessDenied:
                        response = "Permission denied. Unable to close " + program_name + "."
                        print(colorama.Fore.LIGHTRED_EX + response)
                        self.speak(response)
                    except psutil.NoSuchProcess:
                        response = program_name + " is not running."
                        print(colorama.Fore.LIGHTRED_EX + response)
                        self.speak(response)
                    break
                else:
                    print(program_name + " is not running.")
        except Exception as e:
            print("An error occurred:", str(e))
            
            
            
            
            
            
            
            
            
            
            
            
#_______________________________________________________________________________haraya_NEURAL_NETWORK_FUNCTION
    #Run Command: python haraya_v3.py
    def harayaNeuralNetwork(self):
        global NameHA, MyName, command
        NameHA = str(self.Name_Honorific_Address[-1])
        MyName = self.MyName
        command = str(self.listenCommand())
        tAnnotateCommand = Thread(target=self.PaLM2_LLM.getChatResponse, args=(command, MyName,))
        tAnnotateCommand.start()
        self.getFullName()
        self.setHonorificAddress()
        #______________________________________________________________________________POSE_RECOGNITION_BLOCK
        #Run Command: python haraya_v3.py
        if "run" in command or "activate" in command or "initialize" in command:
            if "face recognition system" in command:
                self.initializeFaceRecognitionSystem()
                response = "Hello " + NameHA + " " + colorama.Fore.CYAN + MyName + colorama.Fore.GREEN + "!"
                response1 = "Hello " + NameHA + " " + MyName + "!"
                print(colorama.Fore.GREEN + response)
                self.speak(response1)
                return self.Confirmation_SubFunction(command)
            elif "pose recognition system" in command:
                self.initializePoseRecognitionSystem()
                return self.Confirmation_SubFunction(command)
            return
        #__________________________________________________________________________________TERMINATION_BLOCK
        #Run Command: python haraya_v3.py
        elif "turn off" in command or any(hotword in command for hotword in self.Stop_HotWords):
            print(colorama.Fore.LIGHTGREEN_EX + command)
            self.setHonorificAddress()
            response = "As you wish " + NameHA + ". Signing off..."
            print(colorama.Fore.GREEN + response)
            self.speak(response)
            return self.playShutdownSound()
        elif any(hotword in command for hotword in self.GoodBye_HotWords):
            print(colorama.Fore.LIGHTGREEN_EX + command)
            response = "Goodbye " + NameHA + "! Have a great day!"
            print(colorama.Fore.GREEN + response)
            self.speak(response)
            return self.playShutdownSound()
            
        elif "turn off my computer" in command:
            print(colorama.Fore.LIGHTGREEN_EX + command)
            response = "As you wish " + NameHA + ". Turning off..."
            print(colorama.Fore.GREEN + response)
            self.speak(response)
            self.tStartUp = Thread(target=self.playSearchSound)
            self.tStartUp.start()
            return
        #_______________________________________________________________________________________INTERNET_SEARCH_BLOCK
        #Run Command: python haraya_v3.py
        elif any(hotword in command for hotword in self.GoogleSearch_HotWords):
            response = "What would you like to search in Google?"
            print(colorama.Fore.GREEN + response)
            self.speak(response)
            command = self.listenCommand()
            try:
                information = command.replace("search in google", '')
                information = information.replace("haraya", '')
                information = information.replace("search", '')
                information = information.replace("in google", '')
                information = information.replace("google", '')
                information = information.replace("can you", '')
                information = information.replace("help me", '')
                search_list = []
                search_list.append(information)
                information = search_list[-1]
                response = "Searching " + colorama.Fore.CYAN + information
                response1 = "Searching " + information
                print(colorama.Fore.GREEN + response)
                self.speak(response1)
                self.tStartUp = Thread(target=self.playSearchSound)
                self.tStartUp.start()
                for i in range(1):
                    search = information.replace(' ', '+')
                    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
                    browser.get("https://www.google.com/search?q=" + search + "&start" + str(i))
                self.speak("Here's what I've found.")
                return self.Confirmation_SubFunction(command)
            except Exception as e:
                self.playPromptSound()
                print(f"An error occured while Searching in Chrome: {e}")
                return
        elif any(hotword in command for hotword in self.YouTubeSearch_HotWords):
            response = "What would you like to search or play in Youtube?"
            print(colorama.Fore.GREEN + response)
            self.speak(response)
            command = self.listenCommand()
            response = "Searching..."
            print(colorama.Fore.GREEN + response)
            self.speak(response)
            self.tStartUp = Thread(target=self.playSearchSound)
            self.tStartUp.start()
            song_title = command.replace("haraya", '')
            song_title = song_title.replace("play", '')
            song_title = song_title.replace("search", '')
            song_title = song_title.replace("in youtube search", '')
            song_title = song_title.replace("in youtube", '')
            song_title = song_title.replace("search in", '')
            song_title = song_title.replace("play in", '')
            song_title = song_title.replace("in youtube play", '')
            song_title = song_title.replace("in youtube search", '')
            song_list = []
            song_list.append(song_title)
            song_title = song_list[-1]
            pywhatkit.playonyt(song_title)
            response = "Now Playing " + colorama.Fore.CYAN + song_title
            response1 = "Now Playing " + song_title
            print(colorama.Fore.GREEN + response)
            self.speak(response1)
            return self.Confirmation_SubFunction(command)
        elif any(hotword in command for hotword in self.WikipediaSearch_HotWords):
            response = "What would you like to searchin Wikipedia?"
            print(colorama.Fore.GREEN + response)
            self.speak(response)
            command = self.listenCommand()
            response = "Searching..."
            print(colorama.Fore.GREEN + response)
            self.speak(response)
            self.playSearchSound()
            person = command.replace("search in wikipedia", '')
            person = person.replace("in wikipedia search", '')
            person = person.replace("haraya", '')
            person = person.replace("who is", '')
            info = wikipedia.summary(person, 1)
            print(info)
            self.speak(info)
            return self.Confirmation_SubFunction(command)
        #____________________________________________________________________________________________________________OPEN/ACCESS_BLOCK
        #Run Command: python haraya_v3.py
        elif any(hotword in command for hotword in self.Open_HotWords):
            print(colorama.Fore.LIGHTGREEN_EX + command)
            program = "program file path"
            try:
                if "chrome" in command:
                    response = "As you wish!"
                    print(colorama.Fore.GREEN + response)
                    self.speak(response)
                    program = "C:\Program Files\Google\Chrome\Application\chrome.exe"
                    subprocess.Popen([program])
                    response = "Opening " + colorama.Fore.LIGHTGREEN_EX + "Chrome" + colorama.Fore.GREEN + "..."
                    response1 = "Opening " + "Chrome..."
                    print(colorama.Fore.GREEN + response)
                    self.speak(response1)
                elif "aqw game launcher" in command or "aqw" in command:
                    response = "As you wish!"
                    print(colorama.Fore.GREEN + response)
                    self.speak(response)
                    program = "C:\Program Files\Artix Game Launcher\Artix Game Launcher.exe"
                    subprocess.Popen([program])
                    response = "Opening " + colorama.Fore.LIGHTGREEN_EX + "Artix game launcher" + colorama.Fore.GREEN + "..."
                    response1 = "Opening " + "Artix game launcher..."
                    print(colorama.Fore.GREEN + response)
                    self.speak(response1)
                elif "genshin impact" in command:
                    response = "As you wish!"
                    print(colorama.Fore.GREEN + response)
                    self.speak(response)
                    program = "C:\Program Files\Genshin Impact\launcher.exe"
                    subprocess.Popen(f'start /b /wait /min /high "Running Genhin Impact as Administrator" "{program}"', shell=True)
                    response = "Opening " + colorama.Fore.LIGHTGREEN_EX + "Genshin Impact" + colorama.Fore.GREEN + "..."
                    response1 = "Opening " + "Genshin Impact..."
                    print(colorama.Fore.GREEN + response)
                    self.speak(response1)
                elif "command prompt" in command or "cmd" in command:
                    response = "As you wish!"
                    print(colorama.Fore.GREEN + response)
                    self.speak(response)
                    program = "cmd.exe"
                    subprocess.Popen([program])
                    response = "Opening " + colorama.Fore.LIGHTGREEN_EX + "Command Prompt" + colorama.Fore.GREEN + "..."
                    response1 = "Opening " + "Command Prompt..."
                    print(colorama.Fore.GREEN + response)
                    self.speak(response1)
                elif "notepad" in command:
                    response = "As you wish!"
                    print(colorama.Fore.GREEN + response)
                    self.speak(response)
                    program = "notepad.exe"
                    subprocess.Popen([program])
                    response = "Opening " + colorama.Fore.LIGHTGREEN_EX + "Notepad" + colorama.Fore.GREEN + "..."
                    response1 = "Opening " + "Notepad..."
                    print(colorama.Fore.GREEN + response)
                    self.speak(response1)
                elif "calculator" in command:
                    response = "As you wish!"
                    print(colorama.Fore.GREEN + response)
                    self.speak(response)
                    program = "calc.exe"
                    subprocess.Popen([program])
                    response = "Opening " + colorama.Fore.LIGHTGREEN_EX + "Calculator" + colorama.Fore.GREEN + "..."
                    response1 = "Opening " + "Calculator..."
                    print(colorama.Fore.GREEN + response)
                    self.speak(response1)
                elif "vlc" in command:
                    response = "As you wish!"
                    print(colorama.Fore.GREEN + response)
                    self.speak(response)
                    program = "C:\\Program Files\\VideoLAN\\VLC\\vlc.exe"
                    subprocess.Popen([program])
                    response = "Opening " + colorama.Fore.LIGHTGREEN_EX + "VLC Media Player" + colorama.Fore.GREEN + "..."
                    response1 = "Opening " + "VLC Media Player..."
                    print(colorama.Fore.GREEN + response)
                    self.speak(response1)
                elif "visual studio code" in command:
                    response = "As you wish!"
                    print(colorama.Fore.GREEN + response)
                    self.speak(response)
                    program = "C:\\Users\\Gianne Bacay\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
                    subprocess.Popen([program])
                    response = "Opening " + colorama.Fore.LIGHTGREEN_EX + "Visual Studio Code" + colorama.Fore.GREEN + "..."
                    response1 = "Opening " + "Visual Studio Code..."
                    print(colorama.Fore.GREEN + response)
                    self.speak(response1)
                elif "messenger" in command:
                    response = "As you wish!"
                    print(colorama.Fore.GREEN + response)
                    self.speak(response)
                    program = "C:\\Users\\Gianne Bacay\\Desktop\\Messenger.exe.lnk"
                    subprocess.Popen(f'start /b /wait /min /high "Running Messenger as Administrator" "{program}"', shell=True)
                    response = "Opening " + colorama.Fore.LIGHTGREEN_EX + "Messenger" + colorama.Fore.GREEN + "..."
                    response1 = "Opening " + "Messenger..."
                    print(colorama.Fore.GREEN + response)
                    self.speak(response1)
                elif "downloads" in command or "download" in command:
                    response = "As you wish!"
                    print(colorama.Fore.GREEN + response)
                    self.speak(response)
                    program = "C:\\Users\\Gianne Bacay\\Desktop\\Downloads.lnk"
                    subprocess.Popen(f'start /b /wait /min /high "Running Downloads as Administrator" "{program}"', shell=True)
                    response = "Opening " + colorama.Fore.LIGHTGREEN_EX + "Downloads" + colorama.Fore.GREEN + "..."
                    response1 = "Opening " + "Downloads..."
                    print(colorama.Fore.GREEN + response)
                    self.speak(response1)
                elif "videos" in command or "video" in command:
                    response = "As you wish!"
                    print(colorama.Fore.GREEN + response)
                    self.speak(response)
                    program = "C:\\Users\\Gianne Bacay\\Desktop\\Videos.lnk"
                    subprocess.Popen(f'start /b /wait /min /high "Running Videos as Administrator" "{program}"', shell=True)
                    response = "Opening " + colorama.Fore.LIGHTGREEN_EX + "Videos" + colorama.Fore.GREEN + "..."
                    response1 = "Opening " + "Videos..."
                    print(colorama.Fore.GREEN + response)
                    self.speak(response1)
            except Exception as e:
                response = f"An error occurLIGHTGREEN_EX while trying to open the said program: {e}"
                print(colorama.Fore.LIGHTLIGHTGREEN_EX_EX + response)
                self.speak(response)
            return self.Confirmation_SubFunction(command)
        #_____________________________________________________________________________________________________CLOSE_BLOCK
        #Run Command: python haraya_v3.py
        elif any(hotword in command for hotword in self.Close_HotWords):
            print(colorama.Fore.LIGHTGREEN_EX + command)
            try:
                if "chrome" in command or "tab" in command:
                    self.close_program(program_name="chrome.exe")
                elif "command prompt" in command or "windows terminal" in command:
                    self.close_program(program_name="WindowsTerminal.exe")
            except Exception as e:
                response = f"An error occur while trying to close the said program: {e}"
                print(colorama.Fore.LIGHTGREEN_EX + response)
                self.speak(response)
            return self.Confirmation_SubFunction(command)
        #________________________________________________________________________COMPUTER_AUTOMATION_BLOCK
        #Run Command: python haraya_v3.py
        elif "shutdown my computer" in command:
            response = "as you wish! shutting down your computer..."
            print(colorama.Fore.GREEN + response)
            self.speak(response)
            os.system("shutdown /s /t 0")
            return self.playPromptSound()
        elif "restart my computer" in command:
            response = "as you wish! restarting your computer..."
            print(colorama.Fore.GREEN + response)
            self.speak(response)
            os.system("shutdown /r")
            return self.playPromptSound()
        elif "sign off my computer" in command or "signoff my computer" in command:
            response = "as you wish! signing off your computer..."
            print(colorama.Fore.GREEN + response)
            self.speak(response)
            os.system("shutdown /l")
            self.playPromptSound()
            return self.Confirmation_SubFunction(command)
        elif "logout my computer" in command or "log out my computer" in command:
            response = "as you wish! logging out your computer..."
            print(colorama.Fore.GREEN + response)
            self.speak(response)
            os.system("shutdown /l")
            self.playPromptSound()
            return self.Confirmation_SubFunction(command)
        elif "sign out my computer" in command or "signout my computer" in command:
            response = "as you wish! signing out your computer..."
            print(colorama.Fore.GREEN + response)
            self.speak(response)
            os.system("shutdown /l")
            self.playPromptSound()
            return self.Confirmation_SubFunction(command)
        elif "increase" in command and "volume" in command or "volume up" in command:
            response = "Increasing volume..."
            print(colorama.Fore.GREEN + response)
            self.speak(response)
            pyautogui.press("volumeup", 10)
            self.playPromptSound()
            return self.harayaNeuralNetwork()
            
        elif "volume" in command and "decrease" in command or "lower" in command:
            response = "Decreasing volume..."
            print(colorama.Fore.GREEN + response)
            self.speak(response)
            pyautogui.press("volumedown", 10)
            self.playPromptSound()
            return self.harayaNeuralNetwork()
        elif "battery" in command and "status" in command or "level" in command or "percentage" in command:
            battery = psutil.sensors_battery()
            percentage = battery.percent
            #isCharging = battery.power_plugged
            if percentage > 50:
                response = f"The current battery percentage is " + colorama.Fore.GREEN + str(percentage) + "%"
            elif percentage <= 50 and percentage > 20:
                response = f"The current battery percentage is " + colorama.Fore.YELLOW + str(percentage) + "%"
            elif percentage <= 20:
                response = f"The current battery percentage is " + colorama.Fore.RED + str(percentage) + "%"
            response1 = f"The current battery percentage is " + str(percentage) + "%"
            print(response)
            self.speak(response1)
            return self.harayaNeuralNetwork()
        #________________________________________________________________________STANDBY_BLOCK
        #Run Command: python haraya_v3.py
        elif any(hotword in command for hotword in self.Standby_HotWords):
            response = "Sure, take your time. I'll wait."
            print(colorama.Fore.GREEN + response)
            self.speak(response)
            return self.Standby_SubFunction()
        #_______________________________________________________NoCommands/NotClearCommands_BLOCK
        #Run Command: python haraya_v3.py
        elif " " == command or "[]" == command or "." == command:
            print(colorama.Fore.LIGHTGREEN_EX + command)
            response = "Hello? Are you still there?"
            print(colorama.Fore.GREEN + response)
            self.speak(response)
            return self.Standby_SubFunction()
        else:
            print(colorama.Fore.LIGHTGREEN_EX + command)
            response = self.PaLM2_LLM.getChatResponse(reply=command, user_name_input=MyName)
            print(colorama.Fore.YELLOW + str(response))
            self.speak(response)
            return self.harayaNeuralNetwork()
# Create an instance of the HarayaV3 class
haraya_v3_instance = haraya_v3()
haraya_v3_instance.setHonorificAddress()
haraya_v3_instance.initializeFaceRecognitionSystem()
#______________________________________harayaNeuralNetwork_IN_A_LOOP_BLOCK
#Run Command: python haraya_v3.py
if __name__ == '__main__':
    pygame.init()
    running = True
    while running:
        haraya_v3_instance.harayaStartUp()
        try:
            haraya_v3_instance.harayaNeuralNetwork()
            haraya_v3_instance.close_program(program_name="WindowsTerminal.exe")
        except Exception as e:
            print(colorama.Fore.LIGHTRED_EX + f"An error occurred while running H.A.R.A.Y.A: \n{e}")
        continue
    pygame.quit()
    exit()
#Run Command: python haraya_v3.py