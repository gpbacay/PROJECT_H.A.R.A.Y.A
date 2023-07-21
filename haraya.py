#Import Libraries/Modules
from threading import Thread
import time
from playsound import playsound
import speech_recognition as sr
import pyttsx3
import pywhatkit

from facerec import Face_Recognition_System
from poserec import Pose_Recognition_System
import os
import subprocess

import wikipedia
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from LoadingBar import LoadingBar 
runLoadingBar = LoadingBar.RunLoadingBar
import pyautogui

tStartUp = Thread(target=playsound, args=(U"startUp.mp3",))
tStartUp.start()
time.sleep(1)
import colorama
colorama.init(autoreset=True)
Header = colorama.Style.BRIGHT + colorama.Fore.GREEN + "\t\t\t\t H.A.R.A.Y.A (High-functioning Autonomous Responsive Anthropomorphic Yielding Assistant) \t\t\t\t\n"
tHeader = Thread(target=print, args=(Header,))
tHeader.start()

from harayaHUD import harayaHUD
runHUD = harayaHUD.runHUD
setIsRandom = harayaHUD.setIsRandom
exitHUD = harayaHUD.exitHUD

tGUI = Thread(target=runHUD, daemon=True)
tGUI.start()
from PaLM2_LLM import run_Bison


#______________________________________________________VOICE_BOX_PRIMARY_BLOCK/FUNCTION
#Run Command: python haraya.py
recognizer = sr.Recognizer()

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(text):
    setIsRandom(1)
    engine.say(text)
    engine.runAndWait()
    setIsRandom(0)
    
#______________________________________________________PLAY_A_SOUND_BLOCK/FUNCTION
#Run Command: python haraya.py
def Play_Prompt_Sound():
    mp3_path = U"prompt1.mp3"
    playsound(mp3_path)
    
def Play_Listening_Sound():
    mp3_path = u"Listening.mp3"
    playsound(mp3_path)
    
def Play_Shutdown_Sound():
    mp3_path = u"shutdown.mp3"
    playsound(mp3_path)
#______________________________________________________CORE_TEMPORARY_MEMORY_BANKS
#Run Command: python haraya.py
Name = []
Name_Honorific_Address = []
NameList = []
Arithmetic_Addition = []
Arithmetic_Subtraction = []
Arithmetic_Multiplication = []
Arithmetic_Division = []
Arithmetic_Modulo = []
Date = []
count = []

#______________________________________________________FACE_RECOGNITION_BLOCK/FUNCTION
#Run Command: python haraya.py
def Locate_MyFullName():
    with open("attendance.csv", "r+") as attendance:
        MyDatalist =  attendance.readlines()
        NameList.append(MyDatalist[-1])
        
        MyFullName = NameList[-1].replace("'", '').split(",")[0]
        Name.append(MyFullName)
        
        
"""
Locate MyFullName from the Face Recognition System
and append it into the Name list in the memory banks.
"""

#_______________________________________Binary-Gendered_Honorifics_Selector_BLOCK/FUNCTION
#Run Command: python haraya.py
def Locate_NameHA():
    Male_Names = ["Gianne Bacay",
                "Earl Jay Tagud",
                "Gemmuel Balceda",
                "Mark Anthony Lagrosa",
                "Klausmieir Villegas",
                "CK Zoe Villegas", 
                "Pio Bustamante",
                "Rolyn Morales",
                "Alexander Villasis"]

    Female_Names = ["Kleinieir Pearl Kandis Bacay",
                    "Princess Viznar",
                    "Nichi Bacay",
                    "Roz Waeschet Bacay",
                    "Killy Obligation",
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
Locate_NameHA()

#_____________________________________________INITIALIZE_FACE_RECOGNITION_SYSTEM_BLOCK/FUNCTION
#Run Command: python haraya.py
def Initialize_Face_Recognition_System():
    tFRS = Thread(target=Face_Recognition_System)
    tFRS.start()
    tLoadBar1 = Thread(target=runLoadingBar, args=(10, "INITIALIZING FRS", "FRS INITIALIZED!"),)
    tLoadBar1.start()
    response = "Initializing Face Recognition System"
    speak(response)
    tFRS.join()
    runLoadingBar(0.5, "RECOGNIZING FACE", "FACE RECOGNIZED!")
    Locate_MyFullName()
    Locate_NameHA()
Initialize_Face_Recognition_System()
    
#_____________________________________________INITIALIZE_POSE_RECOGNITION_SYSTEM_BLOCK/FUNCTION
#Run Command: python haraya.py
def Initialize_Pose_Recognition_System():
    response = "Recognizing pose..."
    print(colorama.Fore.GREEN + response)
    Pose_Recognition_System()
    Play_Prompt_Sound()


#_______________________________________START_UP_MAIN_FUNCTION
#Run Command: python haraya.py
def Start_Up_command_MainFunction():
    Play_Prompt_Sound()
    try:
        NameHA = Name_Honorific_Address[-1]
        MyName = Name[-1]
        response = "Hi " + NameHA + " " + colorama.Fore.CYAN + MyName + colorama.Fore.GREEN + "! How can I help you?"
        response1 = "Hi " + NameHA + " " + MyName + "! How can I help you?"
    except:
        response = "Hi! How can I help you?"
    print(colorama.Fore.GREEN + response)
    speak(response1)


#______________________________LISTEN_COMMAND_MAIN_FUNCTION
#Run Command: python haraya.py
def Listen_command_MainFunction():
    global command
    command = ""
    try:
        with sr.Microphone() as source:
            print(colorama.Fore.CYAN + "Listening...")
            Play_Listening_Sound()
            recognizer.energy_threshold = 1.0
            recognizer.pause_threshold = 0.8
            #voice = recognizer.record(source)
            voice = recognizer.listen(source, timeout=7, phrase_time_limit=7)
            command = recognizer.recognize_google(voice, show_all=True)
            command = command.lower()
            command = str(command)
    except:
        pass
    return command


#______________________________ADD_COMMAND_MAIN_FUNCTION
#Run Command: python haraya.py
def Add_command_MainFunction(command):
    command = str(command)
    Interrogative_words = ['what', ' what ', 'what ', ' what',
                        'who', ' who ', 'who ', ' who',
                        'where', ' where ', 'where ', ' where',
                        'when', ' when ', 'when ', ' when',
                        'why', ' why ', 'why ', ' why',
                        'how', ' how ', 'how ', ' how']
    try:
        if str(command) in Interrogative_words:
            response = "Is there anything specific you would like to know or ask?"
            print(colorama.Fore.GREEN + response)
            speak(response)
        elif str(command) not in Interrogative_words:
            response = "Is there anything else I could do for you?"
            print(colorama.Fore.GREEN + response)
            speak(response)
        else:
            response = ''
            print(response)
            speak(response)
        with sr.Microphone() as source:
            print(colorama.Fore.CYAN + "Listening...")
            Play_Listening_Sound()
            recognizer.energy_threshold = 1.0
            recognizer.pause_threshold = 0.8
            #voice = recognizer.record(source)
            voice = recognizer.listen(source, timeout=7, phrase_time_limit=7)
            command = recognizer.recognize_google(voice, show_all=True)
            command = command.lower()
            command = str(command)
    except:
        pass
    return command


#______________________________WAIT_COMMAND_MAIN_FUNCTION
#Run Command: python haraya.py
def Wait_command_MainFunction():
    global command
    command = ""
    
    try:
        with sr.Microphone() as source:
            print(colorama.Fore.CYAN + "Waiting...")
            recognizer.energy_threshold = 1.0
            recognizer.pause_threshold = 0.8
            #voice = recognizer.record(source)
            voice = recognizer.listen(source, timeout=7, phrase_time_limit=7)
            command = recognizer.recognize_google(voice, show_all=True)
            command = command.lower()
            command = str(command)
    except:
        pass
    return command


#_______________________________________________________________________________haraya_CORE_FUNCTION
#Run Command: python haraya.py
def run_haraya():
    Locate_MyFullName()
    Locate_NameHA()
    global NameHA
    NameHA = Name_Honorific_Address[-1]
    MyName = Name[-1]


    #________________________________________________LISTS_OF_COMMAND_KEY_WORDS
    #Run Command: python haraya.py
    Standby_KeyWords = ["standby",
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

    GoodBye_KeyWords = ["goodbye",
                        " goodbye ",
                        "goodbye ",
                        " goodbye",
                        "good bye",
                        "haraya goodbye",
                        "goodbye haraya",
                        "haraya bye",
                        "bye haraya",
                        "bye",
                        " bye ",
                        "bye ",
                        " bye",
                        "let's call it a day",
                        "i said goodbye",
                        "you're good to go",
                        "you can go now",
                        "you can go to sleep now",
                        "i need to go"]

    Stop_KeyWords = ["sign off",
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

    Yes_KeyWords = ["yes",
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
                    "I said yes"]
    
    RunFaceRecog_KeyWords = ["run face recognition system",
                            "run face rec again",
                            "recognize my face again",
                            "face recognition again",
                            "run face recognition system again",
                            "run face recognition",
                            "run the face recognition system",
                            "run the video face recognition system",
                            "run video face recognition system",
                            "run the video face recognition system",
                            "run video face recognition system",
                            "run the live face recognition system",
                            "run live face recognition system",
                            "face recognition system with smart attendance system",
                            "run the video face recognition system with smart attendance system",
                            "run video face recognition system with smart attendance system",
                            "run the live face recognition system with smart attendance system",
                            "run live face recognition system with smart attendance system"]
    
    InitializeFaceRecog_KeyWords = ["initialize face recognition system",
                            "initialize face recognition",
                            "initialize the face recognition system",
                            "initialize face recognition system again",
                            "initialize the video face recognition system",
                            "initialize video face recognition system",
                            "initialize the video face recognition system",
                            "initialize video face recognition system",
                            "initialize the live face recognition system",
                            "initialize live face recognition system",
                            "initialize recognition system with smart attendance system",
                            "initialize the video face recognition system with smart attendance system",
                            "initialize video face recognition system with smart attendance system",
                            "initialize the live face recognition system with smart attendance system",
                            "initialize live face recognition system with smart attendance system"]
    
    ActivateFaceRecog_KeyWords = ["activate face recognition system",
                            "activate face recognition",
                            "activate the face recognition system",
                            "activate the video face recognition system",
                            "activate video face recognition system",
                            "activate the video face recognition system",
                            "activate face recognition system again",
                            "activate video face recognition system",
                            "activate the live face recognition system",
                            "activate live face recognition system",
                            "activate recognition system with smart attendance system",
                            "activate the video face recognition system with smart attendance system",
                            "activate video face recognition system with smart attendance system",
                            "activate the live face recognition system with smart attendance system",
                            "activate live face recognition system with smart attendance system"]
    
    RunPoseRecog_KeyWords = ["run pose recognition system",
                            "run pose recognition",
                            "run the pose recognition system",
                            "run the video pose recognition system",
                            "run video pose recognition system",
                            "run the video pose recognition system",
                            "run video pose recognition system",
                            "run the live pose recognition system",
                            "run live pose recognition system"]
    
    InitializePoseRecog_KeyWords = ["initialize pose recognition system",
                            "initialize pose recognition",
                            "initialize the pose recognition system",
                            "initialize the video pose recognition system",
                            "initialize video pose recognition system",
                            "initialize the video pose recognition system",
                            "initialize video pose recognition system",
                            "initialize the live pose recognition system",
                            "initialize live pose recognition system"]
    
    ActivatePoseRecog_KeyWords = ["activate pose recognition system",
                            "activate pose recognition",
                            "activate the pose recognition system",
                            "activate the video pose recognition system",
                            "activate video pose recognition system",
                            "activate the video pose recognition system",
                            "activate video pose recognition system",
                            "activate the live pose recognition system",
                            "activate live pose recognition system"]
    
    Haraya_KeyWords = ["haraya",
                    "araya",
                    "mariah",
                    "hiraya",
                    "raya",
                    "heraya",
                    "area",
                    "ryan",
                    "aya",
                    "heria",
                    "herya",
                    "halaya"]
    
    Repeat_KeyWords = ["repeat after me",
                    "haraya repeat after me",
                    "repeat after me haraya",
                    "say what i'm going to say",
                    "haraya say what i'm going to say",
                    "speak after me",
                    "mimic me",
                    "copy what I say"]

    #_______________________________________________________________________STANDBY_SUBFUNCTION
    #Run Command: python haraya.py
    def Standby_SubFunction():
        while True:
            command = Wait_command_MainFunction()
            if 'haraya' in str(command) or str(command) in Haraya_KeyWords:
                Play_Prompt_Sound()
                response = "Yes? How can I help you?"
                print(colorama.Fore.GREEN + response)
                speak(response)
                exit(run_haraya())

    #_______________________________________________________________________CONFIRMATION_SUBFUNCTION
    #Run Command: python haraya.py
    def Confirmation_SubFunction(command):
        command = Add_command_MainFunction(str(command))
        
        if str(command) in Yes_KeyWords:
            print(colorama.Fore.RED + str(command))
            command = command.replace(command, '')
            response = "Then, please do tell."
            print(colorama.Fore.GREEN + response)
            speak(response)
            exit(run_haraya())

        elif '' == str(command):
            print(colorama.Fore.RED + str(command))
            response = "Hello? Are you still there?"
            print(colorama.Fore.GREEN + response)
            speak(response)
            Standby_SubFunction()
        else:
            response = "Come again?"
            print(response)
            speak(response)
            exit(run_haraya())

    #_______________________________________________________________________REPEAT_SUBFUNCTION
    #Run Command: python haraya.py
    def Repeat_SubFunction():
        global command
        command = ""
        
        try:
            with sr.Microphone() as source:
                response = "Understood, I'm listening..."
                print(colorama.Fore.GREEN + response)
                speak(response)
                Play_Listening_Sound()
                recognizer.energy_threshold = 1.0
                recognizer.pause_threshold = 0.8
                #voice = recognizer.record(source)
                voice = recognizer.listen(source, timeout=7, phrase_time_limit=7)
                command = recognizer.recognize_google(voice, show_all=True)
                command = command.lower()
                command = str(command)
        except:
            pass
        print(colorama.Fore.RED + str(command))
        speak(command)
        time.sleep(5)
        Confirmation_SubFunction(command)

    #_____________________________________________________COMMAND_ASSIGNMENT_BLOCK (CORE SCRIPT)
    #Run Command: python haraya.py

    command = str(Listen_command_MainFunction())

    #______________________________________________________FACE_RECOGNITION_BLOCK
    #Run Command: python haraya.py
    if str(command) in RunFaceRecog_KeyWords or str(command) in InitializeFaceRecog_KeyWords or str(command) in ActivateFaceRecog_KeyWords:
        if "run" in str(command):
            response = "Running Face Recognition System..."
        elif "initialize" in str(command):
            response = "Initializing Face Recognition System..."
        elif "activate" in str(command):
            response = "Activating Face Recognition System..."
        else:
            response = "Running Face Recognition System..."
        print(colorama.Fore.GREEN + response)
        speak(response)
        Initialize_Face_Recognition_System()
        NameHA = Name_Honorific_Address[-1]
        MyName = Name[-1]
        response = "Hello " + NameHA + " " + colorama.Fore.CYAN + MyName + colorama.Fore.GREEN + "!"
        response1 = "Hello " + NameHA + " " + MyName + "!"
        print(colorama.Fore.GREEN + response)
        speak(response1)
        Confirmation_SubFunction(command)
        
    #______________________________________________________POSE_RECOGNITION_BLOCK
    #Run Command: python haraya.py
    if str(command) in RunPoseRecog_KeyWords or str(command) in InitializePoseRecog_KeyWords or str(command) in ActivatePoseRecog_KeyWords:
        if "run" in str(command):
            response = "Running Pose Recognition System..."
        elif "initialize" in str(command):
            response = "Initializing Pose Recognition System..."
        elif "activate" in str(command):
            response = "Activating Pose Recognition System..."
        else:
            response = "Running Pose Recognition System..."
        print(colorama.Fore.GREEN + response)
        speak(response)
        Initialize_Pose_Recognition_System()
        Confirmation_SubFunction(command)

    #________________________________________________________________REPEAT_BLOCK
    #Run Command: python haraya.py
    elif str(command) in Repeat_KeyWords:
        Repeat_SubFunction()

    #________________________________________________________________TERMINATION_BLOCK
    #Run Command: python haraya.py
    elif str(command) in Stop_KeyWords:
        print(colorama.Fore.RED + str(command))
        Locate_NameHA()
        response = "As you wish " + NameHA + ". Signing off..."
        print(colorama.Fore.GREEN + response)
        speak(response)
        exitHUD()
        Play_Shutdown_Sound()
        exit()

    elif str(command) in GoodBye_KeyWords:
        print(colorama.Fore.RED + str(command))
        response = "Goodbye " + NameHA + "! Have a great day!"
        print(colorama.Fore.GREEN + response)
        speak(response)
        exitHUD()
        Play_Shutdown_Sound()
        exit()
        
    elif "turn off my computer" in str(command):
        print(colorama.Fore.RED + str(command))
        response = "As you wish " + NameHA + ". Turning off..."
        print(colorama.Fore.GREEN + response)
        speak(response)
        exitHUD()
        Play_Shutdown_Sound()
        exit()

    #_______________________________________________________________________________________INTERNET_SEARCH_BLOCK
    #Run Command: python haraya.py
    elif "in google" in str(command) or "in google search" in str(command):
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
            response = "Searching" + colorama.Fore.RED + information
            response1 = "Searching" + information
            print(colorama.Fore.GREEN + response)
            speak(response1)
            for i in range(1):
                search = information.replace(' ', '+')
                browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
                browser.get("https://www.google.com/search?q=" + search + "&start" + str(i))
            speak("Here's what I've found.")
            Confirmation_SubFunction(command)
        except:
            Play_Prompt_Sound()
            exitHUD()
            exit()

    elif "in youtube" in str(command) or "play" in str(command):
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
        response = "Now Playing" + colorama.Fore.RED + song_title
        response1 = "Now Playing" + song_title
        print(colorama.Fore.GREEN + response)
        speak(response1)
        Confirmation_SubFunction(command)

    elif "search in wikipedia" in str(command) or "in wikipedia search" in str(command):
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

    #________________________________________________________________________________________________OPEN/ACCESS_BLOCK
    #Run Command: python haraya.py
    elif "open" in str(command) or "access" in str(command):
        print(colorama.Fore.RED + str(command))
        command = command.replace("open", '')
        command = command.replace("access", '')
        try:
            if "chrome" in str(command):
                response = "As you wish!"
                print(colorama.Fore.GREEN + response)
                speak(response)
                program = "C:\Program Files\Google\Chrome\Application\chrome.exe"
                subprocess.Popen([program])
                response = "Opening " + colorama.Fore.RED + "Chrome..."
                response1 = "Opening " + "Chrome..."
                print(colorama.Fore.GREEN + response)
                speak(response1)
                
            elif "aqw game launcher" in str(command) or "aqw" in str(command):
                response = "As you wish!"
                print(colorama.Fore.GREEN + response)
                speak(response)
                program = "C:\Program Files\Artix Game Launcher\Artix Game Launcher.exe"
                subprocess.Popen([program])
                response = "Opening " + colorama.Fore.RED + "Artix game launcher..."
                response1 = "Opening " + "Artix game launcher..."
                print(colorama.Fore.GREEN + response)
                speak(response1)
                
            elif "genshin impact" in str(command):
                response = "As you wish!"
                print(colorama.Fore.GREEN + response)
                speak(response)
                program = "C:\Program Files\Genshin Impact\launcher.exe"
                subprocess.Popen(f'start /b /wait /min /high "Running Genhin Impact as Administrator" "{program}"', shell=True)
                response = "Opening " + colorama.Fore.RED + "Genshin Impact..."
                response1 = "Opening " + "Genshin Impact..."
                print(colorama.Fore.GREEN + response)
                speak(response1)
                
            elif "command prompt" in str(command) or "cmd" in str(command):
                response = "As you wish!"
                print(colorama.Fore.GREEN + response)
                speak(response)
                program = "cmd.exe"
                subprocess.Popen([program])
                response = "Opening " + colorama.Fore.RED + "Command Prompt..."
                response1 = "Opening " + "Command Prompt..."
                print(colorama.Fore.GREEN + response)
                speak(response1)
                
            elif "notepad" in str(command):
                response = "As you wish!"
                print(colorama.Fore.GREEN + response)
                speak(response)
                program = "notepad.exe"
                subprocess.Popen([program])
                response = "Opening " + colorama.Fore.RED + "Notepad..."
                response1 = "Opening " + "Notepad..."
                print(colorama.Fore.GREEN + response)
                speak(response1)
                
            elif "calculator" in str(command):
                response = "As you wish!"
                print(colorama.Fore.GREEN + response)
                speak(response)
                program = "calc.exe"
                subprocess.Popen([program])
                response = "Opening " + colorama.Fore.RED + "Calculator..."
                response1 = "Opening " + "Calculator..."
                print(colorama.Fore.GREEN + response)
                speak(response1)
                
            elif "vlc" in str(command):
                response = "As you wish!"
                print(colorama.Fore.GREEN + response)
                speak(response)
                program = "C:\\Program Files\\VideoLAN\\VLC\\vlc.exe"
                subprocess.Popen([program])
                response = "Opening " + colorama.Fore.RED + "VLC Media Player..."
                response1 = "Opening " + "VLC Media Player..."
                print(colorama.Fore.GREEN + response)
                speak(response1)
                
            elif "visual studio code" in str(command):
                response = "As you wish!"
                print(colorama.Fore.GREEN + response)
                speak(response)
                program = "C:\\Users\\Gianne Bacay\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
                subprocess.Popen([program])
                response = "Opening " + colorama.Fore.RED + "Visual Studio Code..."
                response1 = "Opening " + "Visual Studio Code..."
                print(colorama.Fore.GREEN + response)
                speak(response1)
                
            elif "messenger" in str(command):
                response = "As you wish!"
                print(colorama.Fore.GREEN + response)
                speak(response)
                program = "C:\\Users\\Gianne Bacay\\Desktop\\Messenger.exe.lnk"
                subprocess.Popen(f'start /b /wait /min /high "Running Messenger as Administrator" "{program}"', shell=True)
                response = "Opening " + colorama.Fore.RED + "Messenger..."
                response1 = "Opening " + "Messenger..."
                print(colorama.Fore.GREEN + response)
                speak(response1)
                
            elif "downloads" in str(command) or "download" in str(command):
                response = "As you wish!"
                print(colorama.Fore.GREEN + response)
                speak(response)
                program = "C:\\Users\\Gianne Bacay\\Desktop\\Downloads.lnk"
                subprocess.Popen(f'start /b /wait /min /high "Running Downloads as Administrator" "{program}"', shell=True)
                response = "Opening " + colorama.Fore.RED + "Downloads..."
                response1 = "Opening " + "Downloads..."
                print(colorama.Fore.GREEN + response)
                speak(response1)
                
            elif "videos" in str(command) or "video" in str(command):
                response = "As you wish!"
                print(colorama.Fore.GREEN + response)
                speak(response)
                program = "C:\\Users\\Gianne Bacay\\Desktop\\Videos.lnk"
                subprocess.Popen(f'start /b /wait /min /high "Running Videos as Administrator" "{program}"', shell=True)
                response = "Opening " + colorama.Fore.RED + "Videos..."
                response1 = "Opening " + "Videos..."
                print(colorama.Fore.GREEN + response)
                speak(response1)
                
        except:
            response = """Access denied! An error occured while accessing."""
            print(colorama.Fore.LIGHTRED_EX + response)
            speak(response)
        exit(Confirmation_SubFunction(command))
        
        
    #________________________________________________________________________COMPUTER_AUTOMATION_BLOCK
    #Run Command: python haraya.py
    elif "shutdown my computer" in str(command):
        response = "as you wish! shutting down your computer..."
        print(colorama.Fore.GREEN + response)
        speak(response)
        os.system("shutdown /s /t 0")
        Play_Prompt_Sound()
        exitHUD()
        exit()

    elif "restart my computer" in str(command):
        response = "as you wish! restarting your computer..."
        print(colorama.Fore.GREEN + response)
        speak(response)
        os.system("shutdown /r")
        Play_Prompt_Sound()
        exitHUD()
        exit()

    elif "sign off my computer" in str(command) or "signoff my computer" in str(command):
        response = "as you wish! signing off your computer..."
        print(colorama.Fore.GREEN + response)
        speak(response)
        os.system("shutdown /l")
        Play_Prompt_Sound()
        Confirmation_SubFunction(command)
        
    elif "logout my computer" in str(command) or "log out my computer" in str(command):
        response = "as you wish! logging out your computer..."
        print(colorama.Fore.GREEN + response)
        speak(response)
        os.system("shutdown /l")
        Play_Prompt_Sound()
        Confirmation_SubFunction(command)
        
    elif "sign out my computer" in str(command) or "signout my computer" in str(command):
        response = "as you wish! signing out your computer..."
        print(colorama.Fore.GREEN + response)
        speak(response)
        os.system("shutdown /l")
        Play_Prompt_Sound()
        Confirmation_SubFunction(command)
        
    elif "increase" in str(command) and "volume" in str(command) or "volume up" in str(command):
        response = "Increasing volume..."
        print(colorama.Fore.GREEN + response)
        speak(response)
        pyautogui.press("volumeup", 10)
        Play_Prompt_Sound()
        exit(run_haraya())
        
    elif "decrease" in str(command) and "volume" in str(command) or "lower down the volume" in str(command) or "lower the volume" in str(command):
        response = "Decreasing volume..."
        print(colorama.Fore.GREEN + response)
        speak(response)
        pyautogui.press("volumedown", 10)
        Play_Prompt_Sound()
        exit(run_haraya())
        
    #________________________________________________________________________STANDBY_BLOCK
    #Run Command: python haraya.py
    elif str(command) in Standby_KeyWords:
        response = "Understood! Take your time. I'll wait."
        print(colorama.Fore.GREEN + response)
        speak(response)
        Standby_SubFunction()
        
    #_______________________________________________________NoCommands/NotClearCommands_BLOCK
    #Run Command: python haraya.py
    elif "[]" == str(command) or "" == str(command):
        time.sleep(3)
        print(colorama.Fore.RED + str(command))
        response = "Hello? Are you still there?"
        print(colorama.Fore.GREEN + response)
        speak(response)
        Play_Listening_Sound()
        Standby_SubFunction()
        
    else:
        print(colorama.Fore.RED + str(command))
        response = run_Bison(reply=command, user_name=MyName)
        print(colorama.Fore.YELLOW + response)
        speak(response)
        exit(run_haraya())
    exitHUD()
    Play_Shutdown_Sound()
    exit()

#______________________________________RUN_haraya_IN_A_LOOP_BLOCK
while True:
    Start_Up_command_MainFunction()
    run_haraya()
    
#Run Command: python haraya.py
