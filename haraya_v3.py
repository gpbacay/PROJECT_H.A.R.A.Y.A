# Import Necessary Libraries/Modules
# Run Command: python haraya_v3.py
import sys
from threading import Thread
import time
from playsound import playsound
import requests
import speech_recognition as sr
import pywhatkit
import pyttsx3
from face_recognition_system import Face_Recognition_System
from pose_recognition_system import Pose_Recognition_System
import os
import subprocess
import psutil
import wikipedia
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from loading_bar import LoadingBar
import colorama
import pygame
from pygame.locals import *
import pyautogui
from haraya_gui import HarayaUI
from web_data_scraping_system import DataScraper
# import harayaVoiceEngine as harayaVoiceEngine
from AI_Agents.haraya_agent import HarayaAgent

class haraya_v3:
    # Constructor Definition Block
    #Run Command: python haraya_v3.py
    def __init__(self):
        self.running = True
        self.ai_name = "Haraya"
        self.command = "."
        self.command1 = "."
        self.response = "."
        self.MyName = "."
        self.HonorificAddress = "."
        
        # Member Methods Initialization
        self.initHeader
        self.setRunning
        self.setAiName
        self.setCommand
        self.setResponse
        self.setMyName
        self.setHonorificAddress
        
        self.getRunning
        self.getAIName
        self.getCommand
        self.getCommand1
        self.getResponse
        self.getMyName
        self.getHonorificAddress
        
        self.playStartUpSound
        self.playPromptSound
        self.playListeningSound
        self.playShutdownSound
        self.playSearchSound
        self.playErrorSound
        
        self.initMyName
        self.initHonorificAddress
        
        self.speak
        self.listenCommand
        self.waitCommand
        self.addCommand
        
        self.initFaceRecognitionSystem
        self.initPoseRecognitionSystem
        
        self.startUp
        self.Standby
        self.Confirmation
        self.closeProgram
        
        self.harayaDecisionLogic
        self.harayaRecursion
        self.main
        
        # Instantiate the agent.
        self.agent = HarayaAgent(ai_name=self.getAIName(), user_name=self.getMyName())
        self.run_agent_command
        
        #Initialization
        # Attributes Declaration Block
        # Run Command: python haraya_v3.py
        colorama.init(autoreset=True)
        pygame.init()
        self.isSpeaking = HarayaUI.isSpeaking
        self.isWaiting = HarayaUI.isWaiting
        self.runUI = HarayaUI.runUI
        self.tGUI = Thread(target=self.runUI, daemon=True)
        self.tGUI.start()
        
        self.initHeader()
        self.DataScraper = DataScraper
        self.tHeader.join()
        self.initMyName()
        self.initHonorificAddress()
        self.loading_bar = LoadingBar()
        self.runLoadingBar = self.loading_bar.run_loadingbar
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voices[1].id)
        # self.hveSpeak = harayaVoiceEngine.Speak
        # Lists of Command Keywords
        # Run Command: python haraya_v3.py
        self.Standby_HotWords = ["standby",
                                "stand by",
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
                                "sayonara",
                                "It was nice chatting with you",
                                "It was nice chatting to you",
                                "I hope you have a great day!",
                                "I hope you have a good day!",
                                "Have a great day!",
                                "Have a good day!",
                                "Goodbye!"]
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
                            "shutdown",
                            "dismiss"]
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
                            "no thank you",
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
                                    "go to chrome",
                                    "go in chrome", 
                                    "go on chrome",
                                    "google"]
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
                                    "go to youtube", 
                                    "on youtube",
                                    "youtube please",
                                    "youtube"]
        self.WikipediaSearch_HotWords = ["in wikipedia search",
                                        "search in wikipedia", 
                                        "in wikipedia find", 
                                        "find in wikipedia", 
                                        "in wikipedia",
                                        "wikipedia search",
                                        "go on wikipedia", 
                                        "on wikipedia",
                                        "wikipedia"]
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
        
    # AUDIO_EFFECTS_BLOCK/FUNCTION
    # Run Command: python haraya_v3.py
    def playStartUpSound(self):
        mp3_path = u"audioFiles\\startup2.mp3"
        playsound(mp3_path)
    def playPromptSound(self):
        mp3_path = u"audioFiles\\prompt1.mp3"
        playsound(mp3_path)
    def playListeningSound(self):
        mp3_path = u"audioFiles\\listening2.mp3"
        playsound(mp3_path)
    def playShutdownSound(self):
        mp3_path = u"audioFiles\\shutdown.mp3"
        playsound(mp3_path)
    def playSearchSound(self):
        mp3_path = u"audioFiles\\searching.mp3"
        playsound(mp3_path)
    def playErrorSound(self):
        mp3_path = u"audioFiles\\error.mp3"
        playsound(mp3_path)
    # Initialize Header
    # Run Command: python haraya_v3.py
    def initHeader(self):
        
        self.tStartUp = Thread(target=self.playStartUpSound)
        self.tStartUp.start()
        self.HeaderStr = "\t\t\t\tH.A.R.A.Y.A (High-functioning Autonomous Responsive Anthropomorphic Yielding Assistant)\t\t\t\t\n"
        self.Header = colorama.Style.BRIGHT + colorama.Fore.GREEN + self.HeaderStr
        self.tHeader = Thread(target=print, args=(self.Header,))
        self.tHeader.start()
    #_________________________________________________________Setters
    # Run Command: python haraya_v3.py
    def setRunning(self, Running_input: bool):
        self.running = Running_input
    def setAiName(self, AiName_input: str):
        self.ai_name = AiName_input
    def setCommand(self, command_input: str):
        self.command = command_input
    def setCommand1(self, command1_input: str):
        self.command1 = command1_input
    def setResponse(self, response_input: str):
        self.response = response_input
    def setMyName(self, MyName_input: str):
        self.MyName = MyName_input
    def setHonorificAddress(self, HonorificAddress_input: str):
        self.HonorificAddress = HonorificAddress_input
    #_________________________________________________________Getters
    # Run Command: python haraya_v3.py
    def getRunning(self):
        return self.running
    def getAIName(self):
        return self.ai_name
    def getCommand(self):
        return self.command
    def getCommand1(self):
        return self.command1
    def getResponse(self):
        return self.response
    def getMyName(self):
        return self.MyName
    def getHonorificAddress(self):
        return self.HonorificAddress
    # ______________________________________________________________________________User-Defined Functions:
    # Initialize user's name/ retrive user's name from the attendance csv
    # Run Command: python haraya_v3.py
    def initMyName(self):
        MyDatalist = []
        NameList = []
        try:
            with open("attendance.csv", "r+") as attendance:
                MyDatalist = attendance.readlines()
                NameList.append(MyDatalist[-1])
        except Exception as e:
            print(colorama.Fore.LIGHTRED_EX + f"An error occured while initializing MyName: {e}")
            pass
        finally:
            self.setMyName(NameList[-1].replace("'", '').split(",")[0])
    # Initialize appropriate Honorofic Address for user's gender and/or name
    # Run Command: python haraya_v3.py
    def initHonorificAddress(self):
        Male_Names = ["Gianne Bacay", 
                    "Earl Jay Tagud",
                    "Gemmuel Balceda",
                    "Mark Anthony Lagrosa",
                    "Klausmieir Villegas",
                    "CK Zoe Villegas",
                    "Rolyn Morales",
                    "Alexander Villasis",
                    "Bryan Sarpamones"]
        Female_Names = ["Kleinieir Pearl Kandis Bacay", 
                        "Princess Viznar", 
                        "Nichi Bacay",
                        "Roz Waeschet Bacay", 
                        "Jane Rose Bandoy"]
        try:
            Gender_Name = self.getMyName()
            if Gender_Name in Male_Names:
                HonorificAddress = "Sir"
            elif Gender_Name in Female_Names:
                HonorificAddress = "Ma'am"
            else:
                HonorificAddress = "Boss"
        except:
            HonorificAddress = "Master"
        finally:
            self.setHonorificAddress(HonorificAddress_input=HonorificAddress)
    
    #______________________________Register Command to the LLM
    #Run Command: python haraya_v3.py
    def run_agent_command(self):
                command = self.getCommand()
                response = self.agent.get_response(command)
                self.setResponse(response)
    
    def speak(self, text):
        self.isSpeaking(1)
        self.engine.say(text)
        self.engine.runAndWait()
        self.isSpeaking(0)
    # def speak(self, text_input: str):
    #     if f"{self.getAIName()}:" in text_input:
    #         text_input = text_input.replace(f"{self.getAIName()}:","")
    #     if f"{self.getMyName()}:" in text_input:
    #         text_input = text_input.replace(f"{self.getMyName()}:","")
    #     if "`" in text_input:
    #         text_input = text_input.replace("`", "")
    #     if "*" in text_input:
    #         text_input = text_input.replace("*", ",")
    #     tSpeak = Thread(target=self.hveSpeak, args=(text_input,),daemon=True)
    #     tSpeak.start()
    #     time.sleep(1.5)
    #     tSpeaking = Thread(target=self.isSpeaking, args=(1,))
    #     tSpeaking.start()
    #     tSpeak.join()
    #     self.isSpeaking(0)
    # LISTEN_COMMAND_MAIN_FUNCTION
    # Run Command: python haraya_v3.py
    def listenCommand(self):
        command = self.getCommand()
        try:
            with sr.Microphone() as source:
                response = "Listening..."
                print(colorama.Fore.CYAN + response)
                print(colorama.Fore.RED + "\nNote: Toggle [F9] to stop/start listening.\n")
                self.playListeningSound()
                self.recognizer.energy_threshold = 1.0
                self.recognizer.pause_threshold = 0.8
                voice = self.recognizer.listen(source, timeout=20, phrase_time_limit=20)
                command = str(self.recognizer.recognize_google(audio_data=voice))
                command1 = str(self.recognizer.recognize_google(audio_data=voice, show_all=True))
                command = command.lower()
                command1 = command1.lower()
                self.setCommand(command_input=command)
                self.setCommand1(command1_input=command1)
        except Exception as e:
            print(colorama.Fore.LIGHTRED_EX + f"\nAn error occured while listening a command: {e}")
            pass
        finally:
            return command
    
    # WAIT_COMMAND_MAIN_FUNCTION
    # Run Command: python haraya_v3.py
    def waitCommand(self):
        self.isWaiting(True)
        command = self.getCommand()
        try:
            with sr.Microphone() as source:
                response = "Waiting..."
                print(colorama.Fore.CYAN + response)
                print(colorama.Fore.RED + "\nNote: Toggle [F9] to stop/start listening.\n")
                self.playListeningSound()
                self.recognizer.energy_threshold = 1.0
                self.recognizer.pause_threshold = 0.8
                voice = self.recognizer.listen(source, timeout=20, phrase_time_limit=20)
                command = str(self.recognizer.recognize_google(audio_data=voice))
                command1 = str(self.recognizer.recognize_google(audio_data=voice, show_all=True))
                command = command.lower()
                command1 = command1.lower()
                self.setCommand(command_input=command)
                self.setCommand1(command1_input=command1)
        except Exception as e:
            print(colorama.Fore.LIGHTRED_EX + f"An error occured while waiting a command: {e}")
            pass
        finally:
            self.isWaiting(False)
            return command
    # ADD_COMMAND_MAIN_FUNCTION
    # Run Command: python haraya_v3.py
    def addCommand(self, command_input: str):
        command = command_input
        response = self.getResponse()
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
            elif any(hotword not in command for hotword in Interrogative_HotWords):
                response = "Is there anything else I could do for you?"
                print(colorama.Fore.GREEN + response)
                self.speak(response)
            else:
                print(response)
                self.speak(response)
            with sr.Microphone() as source:
                print(colorama.Fore.CYAN + "Listening...")
                print(colorama.Fore.RED + "\nNote: Toggle [F9] to stop/start listening.\n")
                self.playListeningSound()
                self.recognizer.energy_threshold = 1.0
                self.recognizer.pause_threshold = 0.8
                voice = self.recognizer.listen(source, timeout=20, phrase_time_limit=20)
                command = str(self.recognizer.recognize_google(audio_data=voice))
                command1 = str(self.recognizer.recognize_google(audio_data=voice, show_all=True))
                command = command.lower()
                command1 = command1.lower()
                self.setCommand(command_input=command)
                self.setCommand1(command1_input=command1)
        except Exception as e:
            print(colorama.Fore.LIGHTRED_EX + f"An error occured while adding a command: {e}")
            pass
        finally:
            return command
    # initFaceRecognitionSystem_BLOCK/FUNCTION
    # Run Command: python haraya_v3.py
    def initFaceRecognitionSystem(self):
        response = "Initializing Face Recognition System"
        self.speak(response)
        tFRS = Thread(target=Face_Recognition_System)
        tFRS.start()
        tFRS.join()
        self.runLoadingBar(seconds=0.5, loading_tag="RECOGNIZING FACE...", end_tag="FACE RECOGNIZED!")
        self.initMyName()
        self.initHonorificAddress()
    # initPoseRecognitionSystem_BLOCK/FUNCTION
    # Run Command: python haraya_v3.py
    def initPoseRecognitionSystem(self):
        response = "RECOGNIZING POSE..."
        print(colorama.Fore.GREEN + response)
        tPRS = Thread(target=Pose_Recognition_System)
        tPRS.start()
        tLoadBar2 = Thread(target=self.runLoadingBar, kwargs={"seconds": 10, "loading_tag": "INITIALIZING P.R.A.I SYSTEM...", "end_tag": "P.R.A.I SYSTEM INITIALIZED!",},)
        tLoadBar2.start()
        response = "INITIALIZING P.R.A.I SYSTEM..."
        self.speak(response)
    # START_UP_MAIN_FUNCTION
    # Run Command: python haraya_v3.py
    def startUp(self):
        self.initFaceRecognitionSystem()
        try:
            response = f"Hi {self.getHonorificAddress()} {self.getMyName()}, I am {self.getAIName()}, your personal AI assistant! How can I help you?"
            response1 = colorama.Fore.GREEN + "Hi " + self.getHonorificAddress() + " " + colorama.Fore.CYAN + self.getMyName() + colorama.Fore.GREEN + "! I am Haraya, your personal AI assistant! How can I help you?"
        except:
            response = "Hi! How can I help you?"
            pass
        finally:
            print(response1)
            self.setResponse(response)
            self.speak(response)
            return 
    # Standby
    # Run Command: python haraya_v3.py
    def Standby(self):
        while True:
            command = self.waitCommand()
            response = self.getResponse()
            print(colorama.Fore.LIGHTGREEN_EX + command)
            if "hey" in command or any(hotword in command for hotword in self.Haraya_HotWords):
                response = "How can I help you?"
                print(colorama.Fore.GREEN + response)
                self.speak(response)
                break
        return
    # Confirmation
    # Run Command: python haraya_v3.py
    def Confirmation(self):
        command = self.addCommand(self.getCommand())
        response = self.getResponse()
        
        try:
            if any(hotword == command for hotword in self.Yes_HotWords):
                print(colorama.Fore.LIGHTGREEN_EX + command)
                response = "Then, please do tell."
                print(colorama.Fore.GREEN + response)
                self.speak(response)
            elif any(hotword == command for hotword in self.No_HotWords):
                print(colorama.Fore.LIGHTGREEN_EX + command)
                response = "Alright then, signing off!"
                print(colorama.Fore.GREEN + response)
                self.speak(response)
                self.playShutdownSound()
                return self.setRunning(False)
            elif "." == command:
                print(colorama.Fore.LIGHTGREEN_EX + command)
                response = "Hello? Are you still there?"
                print(colorama.Fore.GREEN + response)
                self.speak(response)
                self.Standby()
            else:
                response = "Come again?"
                print(colorama.Fore.GREEN + response)
                self.speak(response)
        except Exception as e:
            self.playErrorSound()
            print(colorama.Fore.LIGHTRED_EX + f"An error occurred while confirming command:", str(e))
        finally:
            self.setCommand(command_input=command)
            return command
    #____________________________________________________________________closeProgram_FUNCTION
    #Run Command: python haraya_v3.py
    def closeProgram(self, program_name: str):
        response = self.response
        try:
            response = "Closing " + program_name + "..."
            response1 = colorama.Fore.GREEN + "Closing " + colorama.Fore.LIGHTRED_EX + program_name + colorama.Fore.GREEN + "..."
            print(response1)
            self.speak(response)
            for process in psutil.process_iter(['pid', 'name']):
                if process.info['name'] == program_name:
                    try:
                        process.terminate()
                        response = program_name + f"\r has been closed."
                        print(colorama.Fore.GREEN + response, end="\r")
                        self.speak(response)
                    except psutil.AccessDenied:
                        self.playErrorSound()
                        response = f"\r Permission denied. Unable to close " + program_name + "."
                        print(colorama.Fore.LIGHTRED_EX + response, end="\r")
                        self.speak(response)
                    except psutil.NoSuchProcess:
                        self.playErrorSound()
                        response = f"\r {program_name} is not running."
                        print(colorama.Fore.LIGHTRED_EX + response, end="\r")
                        self.speak(response)
                    break
                else:
                    print(f"\r {program_name} is not running.", end="\r")
                    pass
        except Exception as e:
            self.playErrorSound()
            print(colorama.Fore.LIGHTRED_EX + f"An error occurred while closing {program_name}:", str(e))
        finally:
            pass
            
            
            
            
            
            
            
            
            
#_______________________________________________________________________________haraya_DECISION LOGIC BLOCK
    #Run Command: python haraya_v3.py
    # takes command, returns reponse
    def harayaDecisionLogic(self, command_input: str, response_input: str):
        try:
            tSetCurrentTime = Thread(target=self.DataScraper.initCurrentTime, args=(self,))
            tSetCurrentTime.start()
            tSetCurrentDate = Thread(target=self.DataScraper.initCurrentDate, args=(self,))
            tSetCurrentDate.start()
            self.initMyName()
            self.initHonorificAddress()
            
            global command, command1, response, response1
            command = str(command_input)
            response = str(response_input)
            self.setCommand(command_input=command)
            self.setResponse(response_input=response)
            
            #______________________________Register Command to the LLM
            #Run Command: python haraya_v3.py
            
            # Start the agent command in its own thread.
            tAgent = Thread(target=self.run_agent_command)
            tAgent.start()
            
            #___________________________________________________VALID COMMANDS CATCHING BLOCKS:
            #Run Command: python haraya_v3.py
            if "run" in command or "activate" in command or "initialize" in command:
                print(colorama.Fore.LIGHTGREEN_EX + command)
                if "face recognition system" in command:
                    self.initFaceRecognitionSystem()
                    try:
                        command = f"Hi! my name is {self.getMyName()}"
                        response = "Haraya's face recognition system was initialized."
                        self.setCommand(command_input=command)
                    except Exception as e:
                        print(colorama.Fore.LIGHTRED_EX + f"Error occured while running the LLM: {e}")
                        response = "I beg your pardon, I'm afraid I didn't catch that."
                        self.speak(response)
                        pass
                    else:
                        self.setResponse(response_input=response)
                        print(colorama.Fore.YELLOW + str(response))
                        self.speak(response)
                elif "pose recognition system" in command or "gods eyes" in command or "post recognition system" in command or "godseyes" in command:
                    self.initPoseRecognitionSystem()
                    response = "Haraya's pose recognition system was initialized."
                    print(response)
                    self.speak(response)
                elif "web data scraping system" in command:
                    self.DataScraper()
                    response = "Haraya's web data scraping system was initialized."
                    print(response)
                    self.speak(response)
                self.setResponse(response_input=response)
            #__________________________________________________________________________________TERMINATION_BLOCK
            #Run Command: python haraya_v3.py
            elif any(hotword == command for hotword in self.Stop_HotWords):
                print(colorama.Fore.LIGHTGREEN_EX + command)
                self.initHonorificAddress()
                response = "As you wish " + self.getHonorificAddress() + ". Signing off..."
                print(colorama.Fore.GREEN + response)
                self.speak(response)
                self.playShutdownSound()
                self.setResponse(response_input=response)
                self.setRunning(False)
            elif any(hotword == command for hotword in self.GoodBye_HotWords):
                print(colorama.Fore.LIGHTGREEN_EX + command)
                response = "Goodbye " + self.getHonorificAddress() + "! Have a great day!"
                print(colorama.Fore.GREEN + response)
                self.speak(response)
                self.playShutdownSound()
                self.setResponse(response_input=response)
                self.setRunning(False)
            #_______________________________________________________________________________________INTERNET_SEARCH_BLOCK
            #Run Command: python haraya_v3.py
            elif any(hotword == command for hotword in self.GoogleSearch_HotWords):
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
                    response = "Searching " + information
                    response1 = colorama.Fore.GREEN + "Searching " + colorama.Fore.CYAN + information
                    print(response1)
                    self.speak(response)
                    self.tStartUp = Thread(target=self.playSearchSound)
                    self.tStartUp.start()
                    for i in range(3):
                        search = information.replace(' ', '+')
                        chrome_service = Service('./chromedriver.exe')
                        browser = webdriver.Chrome(service=chrome_service)
                        browser.get("https://www.google.com/search?q=" + search + "&start" + str(i))
                    response = "Here's what I've found."
                    self.speak(response)
                except Exception as e:
                    self.playErrorSound()
                    response = f"An error occured while searching in Chrome: {e}"
                    print(response)
                    pass
                else:
                    self.setResponse(response_input=response)
                    self.Confirmation()
            elif any(hotword == command for hotword in self.YouTubeSearch_HotWords):
                response = "What would you like to search or play in Youtube?"
                print(colorama.Fore.GREEN + response)
                self.speak(response)
                command = self.listenCommand()
                try:
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
                    response = "Now Playing " + song_title
                    response1 = colorama.Fore.GREEN + "Now Playing " + colorama.Fore.CYAN + song_title
                    print(response1)
                    self.speak(response)
                except Exception as e:
                    self.playErrorSound()
                    response = f"An error occured while playing in Youtube: {e}"
                    print(response)
                    pass
                else:
                    self.setResponse(response_input=response)
                    self.Confirmation()
            elif any(hotword == command for hotword in self.WikipediaSearch_HotWords):
                response = "What would you like to searchin Wikipedia?"
                print(colorama.Fore.GREEN + response)
                self.speak(response)
                command = self.listenCommand()
                try:
                    response = "Searching..."
                    print(colorama.Fore.GREEN + response)
                    self.speak(response)
                    self.tStartUp = Thread(target=self.playSearchSound)
                    self.tStartUp.start()
                    person = command.replace("search in wikipedia", '')
                    person = person.replace("in wikipedia search", '')
                    person = person.replace("haraya", '')
                    person = person.replace("who is", '')
                    info = wikipedia.summary(person, 1)
                    print(info)
                    self.speak(info)
                except Exception as e:
                    self.playErrorSound()
                    response = f"An error occured while searching in Wikipedia: {e}"
                    print(response)
                    pass
                else:
                    self.setResponse(response_input=response)
                    self.Confirmation()
            #____________________________________________________________________________________________________________OPEN/ACCESS_BLOCK
            #Run Command: python haraya_v3.py
            elif any(hotword in command for hotword in self.Open_HotWords):
                print(colorama.Fore.LIGHTGREEN_EX + command)
                program = "program file path"
                self.tStartUp = Thread(target=self.playSearchSound)
                try:
                    if "chrome" in command or "google" in command:
                        response = "As you wish!"
                        print(colorama.Fore.GREEN + response)
                        self.speak(response)
                        program = "C:\Program Files\Google\Chrome\Application\chrome.exe"
                        subprocess.Popen([program])
                        response = "Opening " + "Chrome..."
                        response1 = colorama.Fore.GREEN + "Opening " + colorama.Fore.LIGHTGREEN_EX + "Chrome" + colorama.Fore.GREEN + "..."
                        self.tStartUp.start()
                        print(response1)
                        self.speak(response)
                    elif "aqw game launcher" in command or "aqw" in command:
                        response = "As you wish!"
                        print(colorama.Fore.GREEN + response)
                        self.speak(response)
                        program = "C:\Program Files\Artix Game Launcher\Artix Game Launcher.exe"
                        subprocess.Popen([program])
                        response = "Opening " + "Artix game launcher..."
                        response1 = colorama.Fore.GREEN + "Opening " + colorama.Fore.LIGHTGREEN_EX + "Artix game launcher" + colorama.Fore.GREEN + "..."
                        self.tStartUp.start()
                        print(response1)
                        self.speak(response)
                    elif "genshin impact" in command:
                        response = "As you wish!"
                        print(colorama.Fore.GREEN + response)
                        self.speak(response)
                        program = "C:\Program Files\Genshin Impact\launcher.exe"
                        subprocess.Popen(f'start /b /wait /min /high "Running Genhin Impact as Administrator" "{program}"', shell=True)
                        response = "Opening " + "Genshin Impact..."
                        response1 = colorama.Fore.GREEN + "Opening " + colorama.Fore.LIGHTGREEN_EX + "Genshin Impact" + colorama.Fore.GREEN + "..."
                        self.tStartUp.start()
                        print(response1)
                        self.speak(response)
                    elif "command prompt" in command or "cmd" in command:
                        response = "As you wish!"
                        print(colorama.Fore.GREEN + response)
                        self.speak(response)
                        program = "cmd.exe"
                        subprocess.Popen([program])
                        response = "Opening " + "Command Prompt..."
                        response1 = colorama.Fore.GREEN + "Opening " + colorama.Fore.LIGHTGREEN_EX + "Command Prompt" + colorama.Fore.GREEN + "..."
                        self.tStartUp.start()
                        print(response1)
                        self.speak(response)
                    elif "notepad" in command:
                        response = "As you wish!"
                        print(colorama.Fore.GREEN + response)
                        self.speak(response)
                        program = "notepad.exe"
                        subprocess.Popen([program])
                        response = "Opening " + "Notepad..."
                        response1 = colorama.Fore.GREEN + "Opening " + colorama.Fore.LIGHTGREEN_EX + "Notepad" + colorama.Fore.GREEN + "..."
                        self.tStartUp.start()
                        print(response1)
                        self.speak(response)
                    elif "calculator" in command:
                        response = "As you wish!"
                        print(colorama.Fore.GREEN + response)
                        self.speak(response)
                        program = "calc.exe"
                        subprocess.Popen([program])
                        response = "Opening " + "Calculator..."
                        response1 = colorama.Fore.GREEN + "Opening " + colorama.Fore.LIGHTGREEN_EX + "Calculator" + colorama.Fore.GREEN + "..."
                        self.tStartUp.start()
                        print(response1)
                        self.speak(response)
                    elif "vlc" in command:
                        response = "As you wish!"
                        print(colorama.Fore.GREEN + response)
                        self.speak(response)
                        program = "C:\\Program Files\\VideoLAN\\VLC\\vlc.exe"
                        subprocess.Popen([program])
                        response = "Opening " + "VLC Media Player..."
                        response1 = colorama.Fore.GREEN + "Opening " + colorama.Fore.LIGHTGREEN_EX + "VLC Media Player" + colorama.Fore.GREEN + "..."
                        self.tStartUp.start()
                        print(response1)
                        self.speak(response)
                    elif "visual studio code" in command:
                        response = "As you wish!"
                        print(colorama.Fore.GREEN + response)
                        self.speak(response)
                        program = "C:\\Users\\Gianne Bacay\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
                        subprocess.Popen([program])
                        response = "Opening " + "Visual Studio Code..."
                        response1 = colorama.Fore.GREEN + "Opening " + colorama.Fore.LIGHTGREEN_EX + "Visual Studio Code" + colorama.Fore.GREEN + "..."
                        self.tStartUp.start()
                        print(response1)
                        self.speak(response)
                    elif "messenger" in command:
                        response = "As you wish!"
                        print(colorama.Fore.GREEN + response)
                        self.speak(response)
                        program = "C:\\Users\\Gianne Bacay\\Desktop\\Messenger.exe.lnk"
                        subprocess.Popen(f'start /b /wait /min /high "Running Messenger as Administrator" "{program}"', shell=True)
                        response = "Opening " + "Messenger..."
                        response1 = colorama.Fore.GREEN + "Opening " + colorama.Fore.LIGHTGREEN_EX + "Messenger" + colorama.Fore.GREEN + "..."
                        self.tStartUp.start()
                        print(response1)
                        self.speak(response)
                    elif "downloads" in command or "download" in command:
                        response = "As you wish!"
                        print(colorama.Fore.GREEN + response)
                        self.speak(response)
                        program = "C:\\Users\\Gianne Bacay\\Desktop\\Downloads.lnk"
                        subprocess.Popen(f'start /b /wait /min /high "Running Downloads as Administrator" "{program}"', shell=True)
                        response = "Opening " + "Downloads..."
                        response1 = colorama.Fore.GREEN + "Opening " + colorama.Fore.LIGHTGREEN_EX + "Downloads" + colorama.Fore.GREEN + "..."
                        self.tStartUp.start()
                        print(response1)
                        self.speak(response)
                    elif "videos" in command or "video" in command:
                        response = "As you wish!"
                        print(colorama.Fore.GREEN + response)
                        self.speak(response)
                        program = "C:\\Users\\Gianne Bacay\\Desktop\\Videos.lnk"
                        subprocess.Popen(f'start /b /wait /min /high "Running Videos as Administrator" "{program}"', shell=True)
                        response = "Opening " + "Videos..."
                        response1 = colorama.Fore.GREEN + "Opening " + colorama.Fore.LIGHTGREEN_EX + "Videos" + colorama.Fore.GREEN + "..."
                        self.tStartUp.start()
                        print(response1)
                        self.speak(response)
                    else:
                        try:
                            self.setCommand(command_input=command)
                            response = "I beg your pardon, I'm afraid I didn't catch that."
                        except Exception as e:
                            print(colorama.Fore.LIGHTRED_EX + f"Error occured while running the LLM: {e}")
                            response = "I beg your pardon, I'm afraid I didn't catch that."
                            self.speak(response)
                            pass
                        else:
                            self.setResponse(response_input=response)
                            print(colorama.Fore.YELLOW + str(response))
                            self.speak(response)
                except Exception as e:
                    self.playErrorSound()
                    response = f"An error occur while trying to open the said program: {e}"
                    print(colorama.Fore.LIGHTGREEN_EX + response)
                    self.speak(response)
                    pass
                finally:
                    self.setResponse(response_input=response)
            #_____________________________________________________________________________________________________CLOSE_BLOCK
            #Run Command: python haraya_v3.py
            elif any(hotword in command for hotword in self.Close_HotWords):
                print(colorama.Fore.LIGHTGREEN_EX + command)
                try:
                    if "chrome" in command or "tab" in command:
                        response = self.closeProgram(program_name="chrome.exe")
                    elif "command prompt" in command or "windows terminal" in command:
                        response = self.closeProgram(program_name="WindowsTerminal.exe")
                    elif "messenger" in command:
                        response = self.closeProgram(program_name="Messenger.exe")
                    elif "file explorer" in command or "Windows explorer" in command:
                        response = self.closeProgram(program_name="explorer.exe")
                except Exception as e:
                    self.playErrorSound()
                    response = f"An error occur while trying to close the said program: {e}"
                    print(colorama.Fore.LIGHTGREEN_EX + response)
                    self.speak(response)
                    pass
                finally:
                    self.setResponse(response_input=response)
            #________________________________________________________________________COMPUTER_AUTOMATION_BLOCK
            #Run Command: python haraya_v3.py
            elif "turn off my computer" in command or "shutdown my computer" in command:
                response = "as you wish! shutting down your computer..."
                print(colorama.Fore.GREEN + response)
                self.speak(response)
                os.system("shutdown /s /t 0")
                self.playShutdownSound()
                self.setResponse(response_input=response)
                self.setRunning(False)
            elif "restart my computer" in command:
                response = "as you wish! restarting your computer..."
                print(colorama.Fore.GREEN + response)
                self.speak(response)
                os.system("shutdown /r")
                self.playShutdownSound()
                self.setResponse(response_input=response)
                self.setRunning(False)
            elif "sign off my computer" in command or "signoff my computer" in command:
                response = "as you wish! signing off your computer..."
                print(colorama.Fore.GREEN + response)
                self.speak(response)
                os.system("shutdown /l")
                self.playShutdownSound()
                self.Confirmation()
                response = f"Successfully Signed off {self.getMyName}'s computer."
                self.setResponse(response_input=response)
                self.setRunning(False)
            elif "logout my computer" in command or "log out my computer" in command:
                response = "as you wish! logging out your computer..."
                print(colorama.Fore.GREEN + response)
                self.speak(response)
                os.system("shutdown /l")
                self.playShutdownSound()
                self.Confirmation()
                response = f"Successfully Logged off {self.getMyName}'s computer."
                self.setResponse(response_input=response)
                self.setRunning(False)
            elif "sign out my computer" in command or "signout my computer" in command:
                response = "as you wish! signing out your computer..."
                print(colorama.Fore.GREEN + response)
                self.speak(response)
                os.system("shutdown /l")
                self.playShutdownSound()
                self.Confirmation()
                response = f"Successfully Signed out {self.getMyName}'s computer."
                self.setResponse(response_input=response)
                self.setRunning(False)
            elif "increase" in command and "volume" in command or "volume up" in command:
                response = "Increasing volume..."
                print(colorama.Fore.GREEN + response)
                self.speak(response)
                pyautogui.press("volumeup", 10)
                response = f"Successfully increased the volume of {self.getMyName}'s computer."
                self.setResponse(response_input=response)
            elif "volume" in command and "decrease" in command or "lower" in command:
                response = "Decreasing volume..."
                print(colorama.Fore.GREEN + response)
                self.speak(response)
                pyautogui.press("volumedown", 10)
                response = f"Successfully lowered the volume of {self.getMyName}'s computer."
                self.setResponse(response_input=response)
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
                self.setResponse(response_input=response)
            #________________________________________________________________________Standby_BLOCK
            #Run Command: python haraya_v3.py
            elif any(hotword in command for hotword in self.Standby_HotWords):
                print(colorama.Fore.LIGHTGREEN_EX + command)
                response = "As you wish " + self.getHonorificAddress() + "!"
                print(colorama.Fore.GREEN + response)
                self.speak(response)
                self.Standby()
            #_______________________________________________________NoCommands/NotClearCommands_BLOCK
            #Run Command: python haraya_v3.py
            elif "." == command or " " == command or "" == command  or command == "[]" or command == None:
                print(colorama.Fore.LIGHTGREEN_EX + command)
                response = "Hello? Are you still there?"
                print(colorama.Fore.GREEN + response)
                self.speak(response)
                self.Standby()
            else:
                try:
                    command = self.getCommand()
                    print(colorama.Fore.LIGHTGREEN_EX + command)
                    response = self.agent.get_response(command)
                    self.setResponse(response)
                except Exception as e:
                    print(colorama.Fore.LIGHTRED_EX + f"\nError occured while running the LLM: {e}")
                    response = "I beg your pardon, I'm afraid I didn't catch that."
                    self.setResponse(response)
                    pass
                else:
                    self.setCommand(command_input=command)
                    self.setResponse(response_input=str(response))
                    print(colorama.Fore.YELLOW + str(response))
                    self.speak(str(response))
        except requests.exceptions.ConnectionError as ce:
            print(colorama.Fore.LIGHTRED_EX + f"\nA connection error occurred while running Haraya's Neural Network: \n{ce}")
        except Exception as e:
            self.playErrorSound()
            print(colorama.Fore.LIGHTRED_EX + f"\nError occured while running Haraya's Neural Network: \n{e}")
            pass
        finally:
            self.setCommand(command_input=command)
            self.setResponse(response_input=str(response))
    
    def harayaRecursion(self):
        if not self.getRunning():
            return
        try:
            if self.getCommand() == self.listenCommand():
                time.sleep(3)
            else:
                self.harayaDecisionLogic(command_input=self.getCommand(), response_input=self.getResponse())
        except requests.exceptions.ConnectionError as ce:
            print(colorama.Fore.LIGHTRED_EX + f"\nA connection error occurred while running H.A.R.A.Y.A: \n{ce}")
        except Exception as e:
            print(colorama.Fore.LIGHTRED_EX + f"\nAn error occurred while running H.A.R.A.Y.A: \n{e}")
        finally:
            self.harayaRecursion()
            
    def main(self):
        try:
            #____________________________________________________________________________________________Run_Haraya
            #Run Command: python haraya_v3.py
            self.startUp()
            
            #_________________________Run Haraya Recursively
            self.harayaRecursion()
            #______________________________________________________________________________________________Terminate_Haraya
            #Run Command: python haraya_v3.py
            self.closeProgram(program_name="WindowsTerminal.exe")
        except Exception as e:
            self.playErrorSound()
            print(colorama.Fore.LIGHTRED_EX + f"\nAn error occurred while closing H.A.R.A.Y.A: {e}")
            pass
        finally:
            pygame.quit()
            sys.exit()
        
if __name__ == '__main__':
    haraya_v3 = haraya_v3()
    haraya_v3.main()


#Run Command: python haraya_v3.py