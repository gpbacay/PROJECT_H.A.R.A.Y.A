#_____________________________________________Import_Necessary_Libraries/Modules
from threading import Thread
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

import pyautogui
import colorama
from harayaUI import harayaUI
from PaLM2_LLM import getChatResponse

class haraya_v3():
    def __init__(self):
        runUI = harayaUI.runUI
        tGUI = Thread(target=runUI, daemon=True)
        tGUI.start()
        tStartUp = Thread(target=playsound, args=(u"audioFiles\\startUp.mp3",))
        tStartUp.start()
        colorama.init(autoreset=True)
        HeaderStr = "\t\t\t\tH.A.R.A.Y.A (High-functioning Autonomous Responsive Anthropomorphic Yielding Assistant)\t\t\t\t\n"
        Header = colorama.Style.BRIGHT + colorama.Fore.GREEN + HeaderStr
        tHeader = Thread(target=print, args=(Header,))
        tHeader.start()
    #___________________________________________Attributes_Declaration_BLOCK
    global runLoadingBar, setIsRandom, recognizer, engine
    global Name, Name_Honorific_Address, NameList
    global speak, harayaListenCommand, harayaAddCommand, harayaWaitCommand
    global playPromptSound, playListeningSound, playShutdownSound
    global getFullName, getHonorificAddress, initializeFaceRecognitionSystem, initializePoseRecognitionSystem
    global harayaStartUp, harayaNeuralNetwork
    #___________________________________________Attributes_Initialization_BLOCK
    runLoadingBar = LoadingBar.RunLoadingBar
    setIsRandom = harayaUI.setIsRandom
    recognizer = sr.Recognizer()
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[2].id)
    #______________________________________________________LISTS_ATTRIBUTES_INITIALIZATION_BLOCK
    #Run Command: python haraya_v3.py
    Name = []
    Name_Honorific_Address = []
    NameList = []
    #______________________________________________________METHODS_IMPLEMENTATION_BLOCK
    #Run Command: python haraya_v3.py
    def speak(text):
        setIsRandom(1)
        engine.say(text)
        engine.runAndWait()
        setIsRandom(0)
    #______________________________LISTEN_COMMAND_MAIN_FUNCTION
    #Run Command: python haraya_v3.py
    def harayaListenCommand():
        global command
        command = ""
        try:
            with sr.Microphone() as source:
                print(colorama.Fore.CYAN + "Listening...")
                print(colorama.Fore.RED + "\nNote: Toggle [F9] to stop/start listening.\n")
                playListeningSound()
                recognizer.energy_threshold = 1.0
                recognizer.pause_threshold = 0.8
                voice = recognizer.listen(source)
                command = recognizer.recognize_google(voice)
                command = command
                command = command.lower()
        except:
            pass
        return command
    #______________________________ADD_COMMAND_MAIN_FUNCTION
    #Run Command: python haraya_v3.py
    def harayaAddCommand(command):
        command = command
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
                speak(response)
            if (hotword not in command for hotword in Interrogative_HotWords):
                response = "Is there anything else I could do for you?"
                print(colorama.Fore.GREEN + response)
                speak(response)
            else:
                response = ''
                print(response)
                speak(response)
            with sr.Microphone() as source:
                print(colorama.Fore.CYAN + "Listening...")
                print(colorama.Fore.RED + "\nNote: Toggle [F9] to stop/start listening.\n")
                playListeningSound()
                recognizer.energy_threshold = 1.0
                recognizer.pause_threshold = 0.8
                voice = recognizer.listen(source)
                command = recognizer.recognize_google(voice)
                command = command
                command = command.lower()
        except:
            pass
        return command
    #______________________________WAIT_COMMAND_MAIN_FUNCTION
    #Run Command: python haraya_v3.py
    def harayaWaitCommand():
        global command
        command = ""
        try:
            with sr.Microphone() as source:
                print(colorama.Fore.CYAN + "Waiting...")
                print(colorama.Fore.RED + "\nNote: Toggle [F9] to stop/start listening.\n")
                recognizer.energy_threshold = 1.0
                recognizer.pause_threshold = 0.8
                voice = recognizer.listen(source)
                command = recognizer.recognize_google(voice)
                command = command
                command = command.lower()
        except:
            pass
        return command
    #______________________________________________________AUDIO_EFFECTS_BLOCK/FUNCTION
    #Run Command: python haraya_v3.py
    def playPromptSound():
        mp3_path = u"audioFiles\\prompt1.mp3"
        playsound(mp3_path)
        
    def playListeningSound():
        mp3_path = u"audioFiles\\Listening.mp3"
        playsound(mp3_path)
        
    def playShutdownSound():
        mp3_path = u"audioFiles\\shutdown.mp3"
        playsound(mp3_path)
    #______________________________________________________FACE_RECOGNITION_BLOCK/FUNCTION
    #Run Command: python haraya_v3.py
    def getFullName():
        with open("attendance.csv", "r+") as attendance:
            MyDatalist = attendance.readlines()
            NameList.append(MyDatalist[-1])
            
            MyFullName = NameList[-1].replace("'", '').split(",")[0]
            Name.append(MyFullName)
    #_______________________________________Binary-GendeLIGHTGREEN_EX_Honorifics_Selector_BLOCK/FUNCTION
    #Run Command: python haraya_v3.py
    def getHonorificAddress():
        Male_Names = ["Gianne Bacay",
                    "Earl Jay Tagud",
                    "Gemmuel Balceda",
                    "Mark Anthony Lagrosa",
                    "Klausmieir Villegas",
                    "CK Zoe Villegas", 
                    "Pio Bustamante",
                    "Rolyn Morales",
                    "Alexander Villasis",
                    "Bryan Sarpamones"]
        Female_Names = ["Kleinieir Pearl Kandis Bacay",
                        "Princess Viznar",
                        "Nichi Bacay",
                        "Roz Waeschet Bacay",
                        "Jane Rose Bandoy"]
        try:
            Gender_Name = Name[-1]
            if Gender_Name in Male_Names:
                Honorific_Address = "Sir"
            elif Gender_Name in Female_Names:
                Honorific_Address = "Ma'am"
            else:
                Honorific_Address = "Boss"
        except:
            Honorific_Address = "Master"
        Name_Honorific_Address.append(Honorific_Address)
    getHonorificAddress()
    #_____________________________________________initializeFaceRecognitionSystem_BLOCK/FUNCTION
    #Run Command: python haraya_v3.py
    def initializeFaceRecognitionSystem():
        tFRS = Thread(target=Face_Recognition_System)
        tFRS.start()
        tLoadBar1 = Thread(target=runLoadingBar, args=(10, "INITIALIZING FRS", "FRS INITIALIZED!"),)
        tLoadBar1.start()
        response = "Initializing Face Recognition System"
        speak(response)
        tFRS.join()
        runLoadingBar(0.5, "RECOGNIZING FACE", "FACE RECOGNIZED!")
        getFullName()
        getHonorificAddress()
    initializeFaceRecognitionSystem()
    #_____________________________________________initializePoseRecognitionSystem_BLOCK/FUNCTION
    #Run Command: python haraya_v3.py
    def initializePoseRecognitionSystem():
        response = "Recognizing pose..."
        print(colorama.Fore.GREEN + response)
        tPRS = Thread(target=Pose_Recognition_System)
        tPRS.start()
        tLoadBar2 = Thread(target=runLoadingBar, args=(10, "INITIALIZING PRS", "PRS INITIALIZED!"),)
        tLoadBar2.start()
        response = "Initializing Pose Recognition System"
        speak(response)
        tPRS.join()

    #_______________________________________START_UP_MAIN_FUNCTION
    #Run Command: python haraya_v3.py
    def harayaStartUp():
        playPromptSound()
        try:
            NameHA = Name_Honorific_Address[-1]
            MyName = Name[-1]
            response = "Hi " + NameHA + " " + colorama.Fore.CYAN + MyName + colorama.Fore.GREEN + "! How can I help you?"
            response1 = "Hi " + NameHA + " " + MyName + "! How can I help you?"
        except:
            response = "Hi! How can I help you?"
        print(colorama.Fore.GREEN + response)
        speak(response1)
    #_______________________________________________________________________________haraya_CORE_FUNCTION
    #Run Command: python haraya_v3.py
    def harayaNeuralNetwork():
        getFullName()
        getHonorificAddress()
        global NameHA
        NameHA = Name_Honorific_Address[-1]
        MyName = Name[-1]
        #________________________________________________LISTS_OF_COMMAND_KEY_WORDS
        #Run Command: python haraya_v3.py
        Standby_HotWords = ["standby",
                            "haraya stand by",
                            "just stand by",
                            "wait",
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
        GoodBye_HotWords = ["goodbye",
                            "good bye",
                            "haraya goodbye",
                            "goodbye haraya",
                            "haraya bye",
                            "bye haraya",
                            "bye",
                            "let's call it a day",
                            "i said goodbye",
                            "you're good to go",
                            "you can go now",
                            "you can go to sleep now",
                            "i need to go",
                            "ciao",
                            "sayonara"]
        Stop_HotWords = ["sign off",
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
        Yes_HotWords = ["yes",
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
        No_HotWords = ["no",
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
        Haraya_HotWords = ["haraya",
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
        GoogleSearch_HotWords = ["in google search",
                                "search in google",
                                "in google navigate",
                                "navigate in google",
                                "in google find",
                                "find in google",
                                "in google",
                                "google search",
                                "go on google",
                                "on google"]
        YouTubeSearch_HotWords = ["in youtube search",
                                "search in youtube",
                                "in youtube play",
                                "play in youtube",
                                "in youtube find",
                                "find in youtube",
                                "in youtube",
                                "youtube search",
                                "go on youtube",
                                "on youtube"]
        WikipediaSearch_HotWords = ["in wikipedia search",
                                "search in wikipedia",
                                "in wikipedia find",
                                "find in wikipedia",
                                "in wikipedia",
                                "wikipedia search",
                                "go on wikipedia",
                                "on wikipedia"]
        Open_HotWords = ["open",
                        "access",
                        "go to",
                        "go on",
                        "run"]
        Close_HotWords = ["close it",
                        "terminate it",
                        "exit",
                        "escape",
                        "quit",
                        "return",
                        "close"]
        #________________________________________________________________________________________STANDBY_SUBFUNCTION
        #Run Command: python haraya_v3.py
        def Standby_SubFunction():
            playListeningSound()
            while True:
                command = harayaWaitCommand()
                print(colorama.Fore.LIGHTGREEN_EX + command)
                if "i'm here" in command or any(hotword in command for hotword in Haraya_HotWords):
                    response = "Yes? How can I help you?"
                    print(colorama.Fore.GREEN + response)
                    speak(response)
                    break
            exit(harayaNeuralNetwork())
        #_______________________________________________________________________CONFIRMATION_SUBFUNCTION
        #Run Command: python haraya_v3.py
        def Confirmation_SubFunction(command):
            command = harayaAddCommand(command)
            
            if any(hotword == command for hotword in Yes_HotWords):
                print(colorama.Fore.LIGHTGREEN_EX + command)
                command = command.replace(command, '')
                response = "Then, please do tell."
                print(colorama.Fore.GREEN + response)
                speak(response)
                exit(harayaNeuralNetwork())
                
            elif any(hotword == command for hotword in No_HotWords):
                print(colorama.Fore.LIGHTGREEN_EX + command)
                response = "Alright then, signing off!"
                print(colorama.Fore.GREEN + response)
                speak(response)
                exit()
                
            elif '' == command:
                print(colorama.Fore.LIGHTGREEN_EX + command)
                response = "Hello? Are you still there?"
                print(colorama.Fore.GREEN + response)
                speak(response)
                Standby_SubFunction()
            else:
                response = "Come again?"
                print(response)
                speak(response)
                exit(harayaNeuralNetwork())
        #_____________________________________________________COMMAND_ASSIGNMENT_BLOCK (CORE SCRIPT)
        #Run Command: python haraya_v3.py
        command = str(harayaListenCommand())
        tAnnotateCommand = Thread(target=getChatResponse, args=(command,))
        tAnnotateCommand.start()
        #____________________________________________________________________________________POSE_RECOGNITION_BLOCK
        #Run Command: python haraya_v3.py
        if "run" in command or "activate" in command or "initialize" in command:
            if "face recognition system" in command:
                initializeFaceRecognitionSystem()
                NameHA = Name_Honorific_Address[-1]
                MyName = Name[-1]
                response = "Hello " + NameHA + " " + colorama.Fore.CYAN + MyName + colorama.Fore.GREEN + "!"
                response1 = "Hello " + NameHA + " " + MyName + "!"
                print(colorama.Fore.GREEN + response)
                speak(response1)
                Confirmation_SubFunction(command)
            elif "pose recognition system" in command:
                initializePoseRecognitionSystem()
                Confirmation_SubFunction(command)
            return
        #___________________________________________________________________________________________TERMINATION_BLOCK
        #Run Command: python haraya_v3.py
        elif "turn off" in command or any(hotword in command for hotword in Stop_HotWords):
            print(colorama.Fore.LIGHTGREEN_EX + command)
            getHonorificAddress()
            response = "As you wish " + NameHA + ". Signing off..."
            print(colorama.Fore.GREEN + response)
            speak(response)
            playShutdownSound()
            exit()
        elif any(hotword in command for hotword in GoodBye_HotWords):
            print(colorama.Fore.LIGHTGREEN_EX + command)
            response = "Goodbye " + NameHA + "! Have a great day!"
            print(colorama.Fore.GREEN + response)
            speak(response)
            playShutdownSound()
            exit()
            
        elif "turn off my computer" in command:
            print(colorama.Fore.LIGHTGREEN_EX + command)
            response = "As you wish " + NameHA + ". Turning off..."
            print(colorama.Fore.GREEN + response)
            speak(response)
            playShutdownSound()
            exit()
        #_______________________________________________________________________________________INTERNET_SEARCH_BLOCK
        #Run Command: python haraya_v3.py
        elif any(hotword in command for hotword in GoogleSearch_HotWords):
            response = "What would you like to search in Google?"
            print(colorama.Fore.GREEN + response)
            speak(response)
            
            command = ""
            try:
                with sr.Microphone() as source:
                    print(colorama.Fore.CYAN + "Listening...")
                    print(colorama.Fore.RED + "\nNote: Toggle [F9] to stop/start listening.\n")
                    playListeningSound()
                    recognizer.energy_threshold = 1.0
                    recognizer.pause_threshold = 0.8
                    voice = recognizer.listen(source)
                    command = recognizer.recognize_google(voice)
                    command = command.lower()
            except:
                pass
            
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
                response = "Searching " + colorama.Fore.LIGHTGREEN_EX + information
                response1 = "Searching " + information
                print(colorama.Fore.GREEN + response)
                speak(response1)
                for i in range(1):
                    search = information.replace(' ', '+')
                    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
                    browser.get("https://www.google.com/search?q=" + search + "&start" + str(i))
                speak("Here's what I've found.")
                Confirmation_SubFunction(command)
            except:
                playPromptSound()
                exit()
        elif any(hotword in command for hotword in YouTubeSearch_HotWords):
            response = "What would you like to search or play in Youtube?"
            print(colorama.Fore.GREEN + response)
            speak(response)
            
            command = ""
            try:
                with sr.Microphone() as source:
                    print(colorama.Fore.CYAN + "Listening...")
                    print(colorama.Fore.RED + "\nNote: Toggle [F9] to stop/start listening.\n")
                    playListeningSound()
                    recognizer.energy_threshold = 1.0
                    recognizer.pause_threshold = 0.8
                    voice = recognizer.listen(source)
                    command = recognizer.recognize_google(voice)
                    command = command.lower()
            except:
                pass
            
            response = "Searching..."
            print(colorama.Fore.GREEN + response)
            speak(response)
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
            response = "Now Playing " + colorama.Fore.LIGHTGREEN_EX + song_title
            response1 = "Now Playing " + song_title
            print(colorama.Fore.GREEN + response)
            speak(response1)
            Confirmation_SubFunction(command)
        elif any(hotword in command for hotword in WikipediaSearch_HotWords):
            response = "What would you like to searchin Wikipedia?"
            print(colorama.Fore.GREEN + response)
            speak(response)
            
            command = ""
            try:
                with sr.Microphone() as source:
                    print(colorama.Fore.CYAN + "Listening...")
                    print(colorama.Fore.RED + "\nNote: Toggle [F9] to stop/start listening.\n")
                    playListeningSound()
                    recognizer.energy_threshold = 1.0
                    recognizer.pause_threshold = 0.8
                    voice = recognizer.listen(source)
                    command = recognizer.recognize_google(voice)
                    command = command.lower()
            except:
                pass
            
            response = "Searching..."
            print(colorama.Fore.GREEN + response)
            speak(response)
            person = command.replace("search in wikipedia", '')
            person = person.replace("in wikipedia search", '')
            person = person.replace("haraya", '')
            person = person.replace("who is", '')
            info = wikipedia.summary(person, 1)
            print(info)
            speak(info)
            Confirmation_SubFunction(command)
        #__________________________________________________________________________________________________________________OPEN/ACCESS_BLOCK
        #Run Command: python haraya_v3.py
        elif any(hotword in command for hotword in Open_HotWords):
            print(colorama.Fore.LIGHTGREEN_EX + command)
            program = "program file path"
            try:
                if "chrome" in command:
                    response = "As you wish!"
                    print(colorama.Fore.GREEN + response)
                    speak(response)
                    program = "C:\Program Files\Google\Chrome\Application\chrome.exe"
                    subprocess.Popen([program])
                    response = "Opening " + colorama.Fore.LIGHTGREEN_EX + "Chrome" + colorama.Fore.GREEN + "..."
                    response1 = "Opening " + "Chrome..."
                    print(colorama.Fore.GREEN + response)
                    speak(response1)
                    
                elif "aqw game launcher" in command or "aqw" in command:
                    response = "As you wish!"
                    print(colorama.Fore.GREEN + response)
                    speak(response)
                    program = "C:\Program Files\Artix Game Launcher\Artix Game Launcher.exe"
                    subprocess.Popen([program])
                    response = "Opening " + colorama.Fore.LIGHTGREEN_EX + "Artix game launcher" + colorama.Fore.GREEN + "..."
                    response1 = "Opening " + "Artix game launcher..."
                    print(colorama.Fore.GREEN + response)
                    speak(response1)
                    
                elif "genshin impact" in command:
                    response = "As you wish!"
                    print(colorama.Fore.GREEN + response)
                    speak(response)
                    program = "C:\Program Files\Genshin Impact\launcher.exe"
                    subprocess.Popen(f'start /b /wait /min /high "Running Genhin Impact as Administrator" "{program}"', shell=True)
                    response = "Opening " + colorama.Fore.LIGHTGREEN_EX + "Genshin Impact" + colorama.Fore.GREEN + "..."
                    response1 = "Opening " + "Genshin Impact..."
                    print(colorama.Fore.GREEN + response)
                    speak(response1)
                    
                elif "command prompt" in command or "cmd" in command:
                    response = "As you wish!"
                    print(colorama.Fore.GREEN + response)
                    speak(response)
                    program = "cmd.exe"
                    subprocess.Popen([program])
                    response = "Opening " + colorama.Fore.LIGHTGREEN_EX + "Command Prompt" + colorama.Fore.GREEN + "..."
                    response1 = "Opening " + "Command Prompt..."
                    print(colorama.Fore.GREEN + response)
                    speak(response1)
                    
                elif "notepad" in command:
                    response = "As you wish!"
                    print(colorama.Fore.GREEN + response)
                    speak(response)
                    program = "notepad.exe"
                    subprocess.Popen([program])
                    response = "Opening " + colorama.Fore.LIGHTGREEN_EX + "Notepad" + colorama.Fore.GREEN + "..."
                    response1 = "Opening " + "Notepad..."
                    print(colorama.Fore.GREEN + response)
                    speak(response1)
                    
                elif "calculator" in command:
                    response = "As you wish!"
                    print(colorama.Fore.GREEN + response)
                    speak(response)
                    program = "calc.exe"
                    subprocess.Popen([program])
                    response = "Opening " + colorama.Fore.LIGHTGREEN_EX + "Calculator" + colorama.Fore.GREEN + "..."
                    response1 = "Opening " + "Calculator..."
                    print(colorama.Fore.GREEN + response)
                    speak(response1)
                    
                elif "vlc" in command:
                    response = "As you wish!"
                    print(colorama.Fore.GREEN + response)
                    speak(response)
                    program = "C:\\Program Files\\VideoLAN\\VLC\\vlc.exe"
                    subprocess.Popen([program])
                    response = "Opening " + colorama.Fore.LIGHTGREEN_EX + "VLC Media Player" + colorama.Fore.GREEN + "..."
                    response1 = "Opening " + "VLC Media Player..."
                    print(colorama.Fore.GREEN + response)
                    speak(response1)
                    
                elif "visual studio code" in command:
                    response = "As you wish!"
                    print(colorama.Fore.GREEN + response)
                    speak(response)
                    program = "C:\\Users\\Gianne Bacay\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
                    subprocess.Popen([program])
                    response = "Opening " + colorama.Fore.LIGHTGREEN_EX + "Visual Studio Code" + colorama.Fore.GREEN + "..."
                    response1 = "Opening " + "Visual Studio Code..."
                    print(colorama.Fore.GREEN + response)
                    speak(response1)
                    
                elif "messenger" in command:
                    response = "As you wish!"
                    print(colorama.Fore.GREEN + response)
                    speak(response)
                    program = "C:\\Users\\Gianne Bacay\\Desktop\\Messenger.exe.lnk"
                    subprocess.Popen(f'start /b /wait /min /high "Running Messenger as Administrator" "{program}"', shell=True)
                    response = "Opening " + colorama.Fore.LIGHTGREEN_EX + "Messenger" + colorama.Fore.GREEN + "..."
                    response1 = "Opening " + "Messenger..."
                    print(colorama.Fore.GREEN + response)
                    speak(response1)
                    
                elif "downloads" in command or "download" in command:
                    response = "As you wish!"
                    print(colorama.Fore.GREEN + response)
                    speak(response)
                    program = "C:\\Users\\Gianne Bacay\\Desktop\\Downloads.lnk"
                    subprocess.Popen(f'start /b /wait /min /high "Running Downloads as Administrator" "{program}"', shell=True)
                    response = "Opening " + colorama.Fore.LIGHTGREEN_EX + "Downloads" + colorama.Fore.GREEN + "..."
                    response1 = "Opening " + "Downloads..."
                    print(colorama.Fore.GREEN + response)
                    speak(response1)
                    
                elif "videos" in command or "video" in command:
                    response = "As you wish!"
                    print(colorama.Fore.GREEN + response)
                    speak(response)
                    program = "C:\\Users\\Gianne Bacay\\Desktop\\Videos.lnk"
                    subprocess.Popen(f'start /b /wait /min /high "Running Videos as Administrator" "{program}"', shell=True)
                    response = "Opening " + colorama.Fore.LIGHTGREEN_EX + "Videos" + colorama.Fore.GREEN + "..."
                    response1 = "Opening " + "Videos..."
                    print(colorama.Fore.GREEN + response)
                    speak(response1)
            except Exception as e:
                response = f"""An error occurLIGHTGREEN_EX while trying to open the said program: {e}"""
                print(colorama.Fore.LIGHTLIGHTGREEN_EX_EX + response)
                speak(response)
            exit(Confirmation_SubFunction(command))
            
        #_____________________________________________________________________________________________________CLOSE_BLOCK
        #Run Command: python haraya_v3.py
        elif any(hotword in command for hotword in Close_HotWords):
            print(colorama.Fore.LIGHTGREEN_EX + command)
            try:
                if "chrome" in command or "tab" in command:
                    response = "Closing " + colorama.Fore.LIGHTGREEN_EX + "Chrome" + colorama.Fore.GREEN + "..."
                    response1 = "Closing " + "Chrome..."
                    print(colorama.Fore.GREEN + response)
                    speak(response1)
                    for process in psutil.process_iter(['pid', 'name']):
                        if process.info['name'] == 'chrome.exe':
                            try:
                                process.terminate()
                                pyautogui.hotkey("ctrl", "w")
                                response = "Chrome has been closed."
                                print(colorama.Fore.GREEN + response)
                                speak(response)
                            except psutil.AccessDenied:
                                response = "Permission denied. Unable to close Chrome."
                                print(colorama.Fore.LIGHTRED_EX + response)
                                speak(response)
                            except psutil.NoSuchProcess:
                                response = "Chrome is not running."
                                print(colorama.Fore.LIGHTRED_EX + response)
                                speak(response)
                            break
                        else:
                            print("Chrome is not running.")
            except Exception as e:
                response = f"""An error occur while trying to close the said program: {e}"""
                print(colorama.Fore.LIGHTGREEN_EX + response)
                speak(response)
            exit(Confirmation_SubFunction(command))
        
        #________________________________________________________________________COMPUTER_AUTOMATION_BLOCK
        #Run Command: python haraya_v3.py
        elif "shutdown my computer" in command:
            response = "as you wish! shutting down your computer..."
            print(colorama.Fore.GREEN + response)
            speak(response)
            os.system("shutdown /s /t 0")
            playPromptSound()
            exit()
        elif "restart my computer" in command:
            response = "as you wish! restarting your computer..."
            print(colorama.Fore.GREEN + response)
            speak(response)
            os.system("shutdown /r")
            playPromptSound()
            exit()
        elif "sign off my computer" in command or "signoff my computer" in command:
            response = "as you wish! signing off your computer..."
            print(colorama.Fore.GREEN + response)
            speak(response)
            os.system("shutdown /l")
            playPromptSound()
            Confirmation_SubFunction(command)
            
        elif "logout my computer" in command or "log out my computer" in command:
            response = "as you wish! logging out your computer..."
            print(colorama.Fore.GREEN + response)
            speak(response)
            os.system("shutdown /l")
            playPromptSound()
            Confirmation_SubFunction(command)
            
        elif "sign out my computer" in command or "signout my computer" in command:
            response = "as you wish! signing out your computer..."
            print(colorama.Fore.GREEN + response)
            speak(response)
            os.system("shutdown /l")
            playPromptSound()
            Confirmation_SubFunction(command)
            
        elif "increase" in command and "volume" in command or "volume up" in command:
            response = "Increasing volume..."
            print(colorama.Fore.GREEN + response)
            speak(response)
            pyautogui.press("volumeup", 10)
            playPromptSound()
            exit(harayaNeuralNetwork())
            
        elif "volume" in command and "decrease" in command or "lower" in command:
            response = "Decreasing volume..."
            print(colorama.Fore.GREEN + response)
            speak(response)
            pyautogui.press("volumedown", 10)
            playPromptSound()
            exit(harayaNeuralNetwork())
            
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
            speak(response1)
            exit(harayaNeuralNetwork())
        #________________________________________________________________________STANDBY_BLOCK
        #Run Command: python haraya_v3.py
        elif any(hotword in command for hotword in Standby_HotWords):
            response = "Sure, take your time. I'll wait."
            print(colorama.Fore.GREEN + response)
            speak(response)
            Standby_SubFunction()
            
        #_______________________________________________________NoCommands/NotClearCommands_BLOCK
        #Run Command: python haraya_v3.py
        elif "[]" == command or "" == command:
            print(colorama.Fore.LIGHTGREEN_EX + command)
            response = "Hello? Are you still there?"
            print(colorama.Fore.GREEN + response)
            speak(response)
            Standby_SubFunction()
            
        else:
            print(colorama.Fore.LIGHTGREEN_EX + command)
            response = getChatResponse(reply=command, user_name=MyName)
            print(colorama.Fore.YELLOW + str(response))
            speak(response)
            exit(harayaNeuralNetwork())
startUp = haraya_v3()
#______________________________________harayaNeuralNetwork_IN_A_LOOP_BLOCK
while True:
        startUp.harayaStartUp()
        try:
            haraya_v3.harayaNeuralNetwork()
        except Exception as e:
            print(colorama.Fore.LIGHTRED_EX + f"An error occurred while running H.A.R.A.Y.A: {e}")
        continue
#Run Command: python haraya_v3.py