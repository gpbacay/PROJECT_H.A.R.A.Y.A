import os
import sys
from threading import Thread
import time
from playsound import playsound
import requests
import speech_recognition as sr
import pywhatkit
import pyttsx3
import subprocess
import psutil
import wikipedia
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import colorama
import pygame
from pygame.locals import *
import pyautogui

# Custom System Modules
from haraya_heading import HarayaHeading
from sound_system import SoundSystem
from haraya_agent import HarayaAgent
from face_recognition_system import FaceRecognitionSystem
from pose_recognition_system import PoseRecognitionSystem
from web_data_scraping_system import DataScraper
from loading_bar import LoadingBar
from haraya_gui import HarayaUI
from user_profile import UserProfile

class HarayaV4:
    # ------------------------- Constructor -------------------------
    def __init__(self, running: bool = True, ai_name: str = "Haraya", command: str = ".",
                 response: str = ".", user_name: str = ".") -> None:
        self.running = running
        self.ai_name = ai_name
        self.user_name = user_name
        self.command = command
        self.ai_command = "."
        self.response = response
        self.honorific_address = "."
        
        # Main thread initializations
        HarayaHeading()
        self.sound_system = SoundSystem()
        colorama.init(autoreset=True)
        pygame.init()
        self.loading_bar = LoadingBar()
        self.runLoadingBar = self.loading_bar.run_loadingbar
        self.user_profile = UserProfile()

        # Thread 1: Initialize AI Agent System in a separate thread
        self.thread_1 = Thread(target=self.initialize_ai_agent, daemon=True)
        self.thread_1.start()

        # Thread 2: Launch the GUI system concurrently
        self.run_gui = HarayaUI.runUI
        self.isSpeaking = HarayaUI.isSpeaking
        self.isWaiting = HarayaUI.isWaiting
        self.thread_2 = Thread(target=self.run_gui, daemon=True)
        self.thread_2.start()
        
        # Thread 3: Initialize Face Recognition System in a separate thread
        self.thread_3 = Thread(target=FaceRecognitionSystem)
        self.thread_3.start()
        
        # Thread 4: Initialize Pose Recognition System in a separate thread
        self.thread_4 = Thread(target=PoseRecognitionSystem)
        
        # Thread 5: Run Loading Bar for Pose Recognition System
        self.thread_5 = Thread(target=self.runLoadingBar, kwargs={
            "seconds": 10,
            "loading_tag": "INITIALIZING P.R.A.I SYSTEM...",
            "end_tag": "P.R.A.I SYSTEM INITIALIZED!"
        })

        # Ensure the AI Agent is initialized before continuing
        self.thread_1.join()

        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')
        if len(self.voices) > 1:
            self.engine.setProperty('voice', self.voices[1].id)
        
        # --- Hotword Lists as Class Constants ---
        self.STANDBY_HOTWORDS = [
        "standby", "stand by", "haraya stand by", "just stand by", "wait",
        "wait a sec", "give me a sec", "hold for a sec", "wait for a sec",
        "give me a second", "hold for a second", "wait for a second",
        "give me a minute", "hold for a minute", "wait for a minute",
        "give me an hour", "hold for an hour", "wait for an hour",
        "just a moment", "just a sec", "just a minute", "just an hour",
        "call you later", "i'll be back", "be right back"
        ]
        self.GOODBYE_HOTWORDS = [
            "goodbye", "good bye", "haraya goodbye", "goodbye haraya", "haraya bye",
            "bye haraya", "bye", "let's call it a day", "i said goodbye",
            "you're good to go", "you can go", "you can go now", "you can go to sleep now",
            "i need to go", "ciao", "sayonara", "It was nice chatting with you",
            "It was nice chatting to you", "I hope you have a great day!",
            "I hope you have a good day!", "Have a great day!", "Have a good day!", "Goodbye!"
        ]
        self.STOP_HOTWORDS = [
            "sign off", "haraya stop", "stop please", "go to sleep", "go to rest",
            "just go to sleep", "just go to rest", "go to sleep haraya", "stop listening",
            "terminate yourself", "enough", "that's enough", "I said enough",
            "I said stop", "you can go to sleep now", "i told you to go to sleep",
            "didn't i told you to go to sleep", "didn't i told you to sleep", "i told you to stop",
            "didn't i told you to stop", "turn off", "shutdown", "dismiss"
        ]
        self.YES_HOTWORDS = [
            "yes", "yup", "yes please", "of course yes", "yes I do", "I do",
            "you got it right", "yes actually", "actually yes", "that's a yes",
            "I think yes", "sure", "yah", "absolutely yes", "definitely yes",
            "you got it right", "I said yes", "affirmative"
        ]
        self.NO_HOTWORDS = [
            "no", "no thank you", "nope", "no please", "of course no", "no I don't",
            "I don't think so", "you got it wrong", "no actually", "actually no",
            "that's a no", "I'm not", "I think not", "none so far", "I'm not sure",
            "noh", "nah", "none", "that's a no no", "absolutely no", "definitely no",
            "absolutely not", "definitely not", "incorrect", "I said no", "negative"
        ]
        self.GOOGLE_SEARCH_HOTWORDS = [
            "in google search", "search in google", "in google navigate",
            "navigate in google", "in google find", "find in google", "in google",
            "google search", "go on google", "go in google", "on google",
            "search in chrome", "go to chrome", "go in chrome", "go on chrome", "google"
        ]
        self.YOUTUBE_SEARCH_HOTWORDS = [
            "in youtube search", "search in youtube", "in youtube play",
            "play in youtube", "in youtube find", "find in youtube", "in youtube",
            "youtube search", "go on youtube", "go in youtube", "go to youtube",
            "on youtube", "youtube please", "youtube"
        ]
        self.WIKIPEDIA_SEARCH_HOTWORDS = [
            "in wikipedia search", "search in wikipedia", "in wikipedia find",
            "find in wikipedia", "in wikipedia", "wikipedia search", "go on wikipedia",
            "on wikipedia", "wikipedia"
        ]
        self.OPEN_HOTWORDS = ["open", "access", "go to", "go in", "run", "launch"]
        self.CLOSE_HOTWORDS = ["close", "terminate", "go out", "exit", "escape", "quit", "return", "close"]
        self.INTERROGATIVES = ['what', ' what ', 'who', ' who ', 'where', ' where ', 'when', ' when ',
                        'why', ' why ', 'how', ' how ']
        self.MALE_NAMES = [
            "Gianne Bacay", "Earl Jay Tagud", "Gemmuel Balceda", "Mark Anthony Lagrosa",
            "Klausmieir Villegas", "CK Zoe Villegas", "Alexander Villasis", "Bryan Sarpamones"
        ]
        self.FEMALE_NAMES = [
            "Kleinieir Pearl Kandis Bacay", "Princess Viznar", "Nichi Bacay", "Roz Waeschet Bacay"
        ]

    # ------------------------- Setters -------------------------
    def set_running(self, running_input: bool) -> None:
        self.running = running_input

    def set_ai_name(self, ai_name_input: str) -> None:
        self.ai_name = ai_name_input

    def set_command(self, command_input: str) -> None:
        self.command = command_input

    def set_ai_command(self, ai_command_input: str) -> None:
        self.ai_command = ai_command_input

    def set_response(self, response_input: str) -> None:
        self.response = response_input

    def set_user_ame(self, user_name_input: str) -> None:
        self.user_name = user_name_input

    def set_honorific_address(self, honorific_address_input: str) -> None:
        self.honorific_address = honorific_address_input

    # ------------------------- Getters -------------------------
    def get_running(self):
        return self.running

    def get_ai_name(self):
        return self.ai_name

    def get_command(self):
        return self.command

    def get_ai_command(self):
        return self.ai_command

    def get_response(self):
        return self.response

    def get_user_name(self):
        return self.user_name

    def get_honorific_address(self):
        return self.honorific_address

    # ------------------------- Core Methods -------------------------
    def initialize_ai_agent(self) -> None:
        try:
            self.agent = HarayaAgent(ai_name=self.get_ai_name(), user_name=self.get_user_name())
        except Exception as e:
            print(colorama.Fore.LIGHTRED_EX + f"Error initializing AI Agent: {e}")
            self.agent = None

    def register_new_command_to_ai_agent(self, new_command: str) -> str:
        response = ""
        try:
            if self.agent is not None:
                self.set_command(new_command)
                response = self.agent.get_response(self.get_command())
                self.set_response(response)
            else:
                print(colorama.Fore.LIGHTRED_EX + "AI Agent not initialized.")
        except Exception as error:
            print(colorama.Fore.LIGHTRED_EX + f"Error in register_new_command_to_ai_agent: {error}")
        return response

    def initialize_honorific_address(self) -> None:
        try:
            user_name = self.get_user_name()
            if user_name in self.MALE_NAMES:
                honorific_address = "Sir"
            elif user_name in self.FEMALE_NAMES:
                honorific_address = "Ma'am"
            else:
                honorific_address = "Boss"
        except Exception as error:
            print(colorama.Fore.LIGHTRED_EX + f"Error determining honorific address: {error}")
            honorific_address = "Master"
        self.set_honorific_address(honorific_address)

    def speak(self, text: str) -> None:
        self.isSpeaking(1)
        self.engine.say(text)
        self.engine.runAndWait()
        self.isSpeaking(0)

    def initialize_face_recognition_system(self) -> None:
        response = "Recognizing Face"
        self.set_response(response)
        self.speak(response)
        self.thread_3.join()
        self.runLoadingBar(seconds=0.5, loading_tag="RECOGNIZING FACE...", end_tag="FACE RECOGNIZED!")
        self.user_profile.init_user_name()
        self.set_user_ame(self.user_profile.get_user_name())
        self.initialize_honorific_address()

    def initialize_pose_recognition_system(self) -> None:
        response = "RECOGNIZING POSE..."
        self.set_response(response)
        self.speak(response)
        print(colorama.Fore.GREEN + response)
        self.thread_4.start()
        self.thread_5.start()

    def start_up_sequence(self) -> None:
        self.initialize_face_recognition_system()
        try:
            if self.agent is not None:
                response = self.agent.get_response(question=f"Hi {self.get_ai_name()}, My name is {self.get_user_name()}.")
                print(colorama.Fore.YELLOW + response)
            else:
                response = f"Hi {self.get_honorific_address()} {self.get_user_name()}, I am {self.get_ai_name()}, your personal AI assistant! How can I help you?"
                print(colorama.Fore.YELLOW + response)
        except Exception as e:
            print(colorama.Fore.LIGHTRED_EX + f"An error occurred during start-up sequence: {e}")
            response = f"Hi {self.get_honorific_address()} {self.get_user_name()}, I am {self.get_ai_name()}, your personal AI assistant! How can I help you?"
            print(colorama.Fore.YELLOW + response)
        finally:
            self.set_response(response)
            self.speak(response)

    def listen_command(self) -> str:
        command = self.get_command()
        try:
            with sr.Microphone() as source:
                response = "Listening..."
                print(colorama.Fore.CYAN + response)
                print(colorama.Fore.RED + "\nNote: Toggle [F9] to stop/start listening.\n")
                self.sound_system.playListeningSound()
                self.recognizer.energy_threshold = 1.0
                self.recognizer.pause_threshold = 0.8
                voice = self.recognizer.listen(source, timeout=20, phrase_time_limit=20)
                command_text = str(self.recognizer.recognize_google(voice))
                command = command_text.lower()
                self.set_command(command)
                ai_command = str(self.recognizer.recognize_google(audio_data=voice, show_all=True))
                self.set_ai_command(ai_command.lower())
        except Exception as e:
            print(colorama.Fore.LIGHTRED_EX + f"\nAn error occurred while listening for a command: {e}")
        finally:
            return command

    def wait_command(self) -> str:
        self.isWaiting(True)
        command = self.get_command()
        try:
            with sr.Microphone() as source:
                response = "Waiting..."
                print(colorama.Fore.CYAN + response)
                print(colorama.Fore.RED + "\nNote: Toggle [F9] to stop/start listening.\n")
                self.sound_system.playListeningSound()
                self.recognizer.energy_threshold = 1.0
                self.recognizer.pause_threshold = 0.8
                voice = self.recognizer.listen(source, timeout=20, phrase_time_limit=20)
                command_text = str(self.recognizer.recognize_google(voice))
                command = command_text.lower()
                self.set_command(command)
                ai_command = str(self.recognizer.recognize_google(audio_data=voice, show_all=True))
                self.set_ai_command(ai_command.lower())
        except Exception as e:
            print(colorama.Fore.LIGHTRED_EX + f"An error occurred while waiting for a command: {e}")
        finally:
            self.isWaiting(False)
            return command

    def register_command(self, command_input: str) -> str:
        command = command_input
        response = self.get_response()
        try:
            if any(hotword in command for hotword in self.INTERROGATIVES):
                response = "Is there anything specific you would like to know or ask?"
                print(colorama.Fore.GREEN + response)
                self.speak(response)
            else:
                response = "Is there anything else I could do for you?"
                print(colorama.Fore.GREEN + response)
                self.speak(response)
            with sr.Microphone() as source:
                print(colorama.Fore.CYAN + "Listening...")
                print(colorama.Fore.RED + "\nNote: Toggle [F9] to stop/start listening.\n")
                self.sound_system.playListeningSound()
                self.recognizer.energy_threshold = 1.0
                self.recognizer.pause_threshold = 0.8
                voice = self.recognizer.listen(source, timeout=20, phrase_time_limit=20)
                command_text = str(self.recognizer.recognize_google(voice))
                command = command_text.lower()
                self.set_command(command)
                ai_command = str(self.recognizer.recognize_google(audio_data=voice, show_all=True))
                self.set_ai_command(ai_command.lower())
        except Exception as e:
            print(colorama.Fore.LIGHTRED_EX + f"An error occurred while registering a command: {e}")
        finally:
            return command

    def standby(self) -> None:
        while True:
            command = self.wait_command()
            if "hey" in command or "haraya" in command:
                response = "How can I help you?"
                print(colorama.Fore.GREEN + response)
                self.speak(response)
                break
        return

    def confirm_command(self) -> str:
        command = self.register_command(self.get_command())
        try:
            Yes_HotWords = ["yes", "yeah", "yup", "sure"]
            No_HotWords = ["no", "nah", "nope"]
            if command in Yes_HotWords:
                response = "Then, please do tell."
                print(colorama.Fore.GREEN + response)
                self.speak(response)
            elif command in No_HotWords:
                response = "Alright then, signing off!"
                print(colorama.Fore.GREEN + response)
                self.speak(response)
                self.sound_system.playShutdownSound()
                self.set_running(False)
            elif command == ".":
                response = "Hello? Are you still there?"
                print(colorama.Fore.GREEN + response)
                self.speak(response)
                self.standby()
            else:
                response = "Come again?"
                print(colorama.Fore.GREEN + response)
                self.speak(response)
        except Exception as e:
            self.sound_system.playErrorSound()
            print(colorama.Fore.LIGHTRED_EX + f"An error occurred while confirming command: {e}")
        finally:
            self.set_command(command)
            return command

    def close_program(self, program_name: str) -> None:
        try:
            print(colorama.Fore.GREEN + "Closing " + colorama.Fore.LIGHTRED_EX + program_name + colorama.Fore.GREEN + "...")
            self.set_response("Closing " + program_name + "...")
            closed = False
            for process in psutil.process_iter(['pid', 'name']):
                if process.info['name'] == program_name:
                    try:
                        process.terminate()
                        self.set_response(program_name + " has been closed.")
                        print(colorama.Fore.GREEN + self.get_response())
                        closed = True
                    except psutil.AccessDenied:
                        self.sound_system.playErrorSound()
                        self.set_response("Permission denied. Unable to close " + program_name + ".")
                        print(colorama.Fore.RED + self.get_response())
                    except psutil.NoSuchProcess:
                        self.sound_system.playErrorSound()
                        self.set_response(program_name + " is not running.")
                        print(colorama.Fore.RED + self.get_response())
                    break
            if not closed:
                self.set_response(f"{program_name} is not running.")
                print(colorama.Fore.YELLOW + self.get_response())
                self.speak(self.get_response())
        except Exception as e:
            self.sound_system.playErrorSound()
            self.set_response(f"An error occurred while closing {program_name}: {e}")
            print(colorama.Fore.LIGHTRED_EX + self.get_response())

    # ------------------ Decision Logic Method ------------------
    def process_command(self, command_input: str, response_input: str) -> None:
        # Update command and response.
        self.set_command(command_input)
        self.set_response(response_input)
        # Update real-time data
        self.user_profile.init_user_name()
        self.initialize_honorific_address()
        self.agent.update_realtime_data()
        # Lowercase version for matching.
        cmd = self.get_command().lower()

        # --- Decision Logic Blocks ---
        if "run" in cmd or "activate" in cmd or "initialize" in cmd:
            if "face recognition system" in cmd:
                try:
                    self.set_command(f"Hi! my name is {self.get_user_name()}")
                    self.set_response("Haraya's face recognition system was initialized.")
                    print(colorama.Fore.YELLOW + self.get_response())
                    self.speak(self.get_response())
                except Exception as e:
                    self.set_response("I beg your pardon, I'm afraid I didn't catch that.")
                    print(colorama.Fore.LIGHTRED_EX + self.get_response())
                    self.speak(self.get_response())
            elif "pose recognition system" in cmd or "gods eyes" in cmd or "post recognition system" in cmd or "godseyes" in cmd or "god's eyes" in cmd:
                self.set_response("Haraya's pose recognition system was initialized.")
                print(colorama.Fore.YELLOW + self.get_response())
                self.speak(self.get_response())
            elif "web data scraping system" in cmd:
                self.data_scraper.__init__()  # Reinitialize the data scraper.
                self.set_response("Haraya's web data scraping system was initialized.")
                print(colorama.Fore.YELLOW + self.get_response())
                self.speak(self.get_response())
        elif any(hotword == cmd for hotword in self.STOP_HOTWORDS):
            self.initialize_honorific_address()
            self.set_response("As you wish " + self.get_honorific_address() + ". Signing off...")
            print(colorama.Fore.YELLOW + self.get_response())
            self.speak(self.get_response())
            self.sound_system.playShutdownSound()
            self.set_running(False)
        elif any(hotword == cmd for hotword in self.GOODBYE_HOTWORDS):
            self.set_response("Goodbye " + self.get_honorific_address() + "! Have a great day!")
            print(colorama.Fore.YELLOW + self.get_response())
            self.speak(self.get_response())
            self.sound_system.playShutdownSound()
            self.set_running(False)
        elif any(hotword == cmd for hotword in self.GOOGLE_SEARCH_HOTWORDS):
            self.set_response("What would you like to search in Google?")
            print(colorama.Fore.YELLOW + self.get_response())
            self.speak(self.get_response())
            self.set_command(self.listen_command())
            try:
                info = (self.get_command()
                        .replace("search in google", "")
                        .replace("haraya", "")
                        .replace("search", "")
                        .replace("in google", "")
                        .replace("google", "")
                        .replace("can you", "")
                        .replace("help me", "")).strip()
                self.set_response("Searching " + info)
                print(colorama.Fore.YELLOW + self.get_response())
                self.speak(self.get_response())
                Thread(target=self.sound_system.playListeningSound).start()
                for i in range(3):
                    search = info.replace(' ', '+')
                    chrome_service = Service('./chromedriver.exe')
                    browser = webdriver.Chrome(service=chrome_service)
                    browser.get("https://www.google.com/search?q=" + search + "&start" + str(i))
                self.set_response("Here's what I've found.")
                print(colorama.Fore.YELLOW + self.get_response())
                self.speak(self.get_response())
            except Exception as e:
                self.sound_system.playErrorSound()
                self.set_response(f"An error occurred while searching in Chrome: {e}")
                print(colorama.Fore.LIGHTRED_EX + self.get_response())
                self.speak(self.get_response())
        elif any(hotword == cmd for hotword in self.YOUTUBE_SEARCH_HOTWORDS):
            response = "What would you like to search or play in YouTube?"
            self.set_response(response)
            print(colorama.Fore.YELLOW + self.get_response())
            self.speak(self.get_response())
            self.set_command(self.listen_command())
            try:
                self.set_response("Searching...")
                print(colorama.Fore.YELLOW + self.get_response())
                self.speak(self.get_response())
                Thread(target=self.sound_system.playListeningSound).start()
                song_title = (self.get_command()
                            .replace("haraya", "")
                            .replace("play", "")
                            .replace("search", "")
                            .replace("in youtube search", "")
                            .replace("in youtube", "")
                            .replace("search in", "")
                            .replace("play in", "")
                            .replace("in youtube play", "")).strip()
                import pywhatkit
                pywhatkit.playonyt(song_title)
                self.set_response("Now Playing " + song_title)
                print(colorama.Fore.YELLOW + self.get_response())
                self.speak(self.get_response())
            except Exception as e:
                self.sound_system.playErrorSound()
                self.set_response(f"An error occurred while playing in YouTube: {e}")
                print(colorama.Fore.LIGHTRED_EX + self.get_response())
                self.speak(self.get_response())
        elif any(hotword == cmd for hotword in self.WIKIPEDIA_SEARCH_HOTWORDS):
            self.set_response("What would you like to search in Wikipedia?")
            print(colorama.Fore.YELLOW + self.get_response())
            self.speak(self.get_response())
            self.set_command(self.listen_command())
            try:
                self.set_response("Searching...")
                print(colorama.Fore.YELLOW + self.get_response())
                self.speak(self.get_response())
                Thread(target=self.sound_system.playListeningSound).start()
                person = (self.get_command()
                        .replace("search in wikipedia", "")
                        .replace("in wikipedia search", "")
                        .replace("haraya", "")
                        .replace("who is", "")).strip()
                info = wikipedia.summary(person, sentences=1)
                self.set_response(info)
                print(colorama.Fore.YELLOW + self.get_response())
                self.speak(self.get_response())
            except Exception as e:
                self.sound_system.playErrorSound()
                self.set_response(f"An error occurred while searching in Wikipedia: {e}")
                print(colorama.Fore.LIGHTRED_EX + self.get_response())
                self.speak(self.get_response())
        elif any(hotword in cmd for hotword in self.OPEN_HOTWORDS):
            program = "program file path"
            print(colorama.Fore.GREEN + "Opening " + colorama.Fore.LIGHTRED_EX + program + colorama.Fore.GREEN + "...")
            Thread(target=self.sound_system.playSearchSound).start()
            try:
                if "chrome" in cmd or "google" in cmd:
                    self.set_response("As you wish!")
                    print(colorama.Fore.YELLOW + self.get_response())
                    self.speak(self.get_response())
                    program = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
                    subprocess.Popen([program])
                    self.set_response("Opening Chrome...")
                    print(colorama.Fore.YELLOW + self.get_response())
                    self.speak(self.get_response())
                elif "aqw game launcher" in cmd or "aqw" in cmd:
                    self.set_response("As you wish!")
                    print(colorama.Fore.YELLOW + self.get_response())
                    self.speak(self.get_response())
                    program = r"C:\Program Files\Artix Game Launcher\Artix Game Launcher.exe"
                    subprocess.Popen([program])
                    self.set_response("Opening Artix game launcher...")
                    print(colorama.Fore.YELLOW + self.get_response())
                    self.speak(self.get_response())
                elif "obsidian" in cmd:
                    self.set_response("As you wish!")
                    print(colorama.Fore.YELLOW + self.get_response())
                    self.speak(self.get_response())
                    program = r"C:\Users\Gianne Bacay\AppData\Local\Obsidian\Obsidian.exe"
                    subprocess.Popen([program])
                    self.set_response("Opening Obsidian...")
                    print(colorama.Fore.YELLOW + self.get_response())
                    self.speak(self.get_response())
                elif "command prompt" in cmd or "cmd" in cmd:
                    self.set_response("As you wish!")
                    print(colorama.Fore.YELLOW + self.get_response())
                    self.speak(self.get_response())
                    program = "cmd.exe"
                    subprocess.Popen([program])
                    self.set_response("Opening Command Prompt...")
                    print(colorama.Fore.YELLOW + self.get_response())
                    self.speak(self.get_response())
                elif "notepad" in cmd:
                    self.set_response("As you wish!")
                    print(colorama.Fore.YELLOW + self.get_response())
                    self.speak(self.get_response())
                    program = "notepad.exe"
                    subprocess.Popen([program])
                    self.set_response("Opening Notepad...")
                    print(colorama.Fore.YELLOW + self.get_response())
                    self.speak(self.get_response())
                elif "calculator" in cmd:
                    self.set_response("As you wish!")
                    print(colorama.Fore.YELLOW + self.get_response())
                    self.speak(self.get_response())
                    program = "calc.exe"
                    subprocess.Popen([program])
                    self.set_response("Opening Calculator...")
                    print(colorama.Fore.YELLOW + self.get_response())
                    self.speak(self.get_response())
                elif "vlc" in cmd:
                    self.set_response("As you wish!")
                    print(colorama.Fore.YELLOW + self.get_response())
                    self.speak(self.get_response())
                    program = r"C:\Program Files\VideoLAN\VLC\vlc.exe"
                    subprocess.Popen([program])
                    print(colorama.Fore.YELLOW + self.get_response())
                    self.speak(self.get_response())
                    self.set_response("Opening VLC Media Player...")
                elif "visual studio code" in cmd:
                    self.set_response("As you wish!")
                    print(colorama.Fore.YELLOW + self.get_response())
                    self.speak(self.get_response())
                    program = r"C:\Users\Gianne Bacay\AppData\Local\Programs\Microsoft VS Code\Code.exe"
                    subprocess.Popen([program])
                    self.set_response("Opening Visual Studio Code...")
                    print(colorama.Fore.YELLOW + self.get_response())
                    self.speak(self.get_response())
                elif "messenger" in cmd:
                    self.set_response("As you wish!")
                    print(colorama.Fore.YELLOW + self.get_response())
                    self.speak(self.get_response())
                    program = r"C:\Users\Gianne Bacay\Desktop\Messenger.exe.lnk"
                    subprocess.Popen(f'start /b /wait /min /high "Running Messenger as Administrator" "{program}"', shell=True)
                    self.set_response("Opening Messenger...")
                    print(colorama.Fore.YELLOW + self.get_response())
                    self.speak(self.get_response())
                elif "downloads" in cmd or "download" in cmd:
                    self.set_response("As you wish!")
                    print(colorama.Fore.YELLOW + self.get_response())
                    self.speak(self.get_response())
                    program = r"C:\Users\Gianne Bacay\Desktop\Downloads.lnk"
                    subprocess.Popen(f'start /b /wait /min /high "Running Downloads as Administrator" "{program}"', shell=True)
                    self.set_response("Opening Downloads...")
                    print(colorama.Fore.YELLOW + self.get_response())
                    self.speak(self.get_response())
                elif "videos" in cmd or "video" in cmd:
                    self.set_response("As you wish!")
                    print(colorama.Fore.YELLOW + self.get_response())
                    self.speak(self.get_response())
                    program = r"C:\Users\Gianne Bacay\Desktop\Videos.lnk"
                    subprocess.Popen(f'start /b /wait /min /high "Running Videos as Administrator" "{program}"', shell=True)
                    self.set_response("Opening Videos...")
                    print(colorama.Fore.YELLOW + self.get_response())
                    self.speak(self.get_response())
                else:
                    self.set_response("I beg your pardon, I'm afraid I didn't catch that.")
                    print(colorama.Fore.YELLOW + self.get_response())
                    self.speak(self.get_response())
            except Exception as e:
                self.sound_system.playErrorSound()
                self.set_response(f"An error occurred while trying to open the program: {e}")
                print(colorama.Fore.LIGHTRED_EX + self.get_response())
                self.speak(self.get_response())
        elif any(hotword in cmd for hotword in self.CLOSE_HOTWORDS):
            try:
                if "chrome" in cmd or "tab" in cmd:
                    self.set_response(self.close_program("chrome.exe"))
                    print(colorama.Fore.YELLOW + self.get_response())
                    self.speak(self.get_response())
                elif "command prompt" in cmd or "windows terminal" in cmd:
                    self.set_response(self.close_program("WindowsTerminal.exe"))
                    print(colorama.Fore.YELLOW + self.get_response())
                    self.speak(self.get_response())
                elif "messenger" in cmd:
                    self.set_response(self.close_program("Messenger.exe"))
                    print(colorama.Fore.YELLOW + self.get_response())
                    self.speak(self.get_response())
                elif "file explorer" in cmd or "windows explorer" in cmd:
                    self.set_response(self.close_program("explorer.exe"))
                    print(colorama.Fore.YELLOW + self.get_response())
                    self.speak(self.get_response())
            except Exception as e:
                self.sound_system.playErrorSound()
                self.set_response(f"An error occurred while trying to close the program: {e}")
                print(colorama.Fore.LIGHTRED_EX + self.get_response())
                self.speak(self.get_response())
        elif "turn off my computer" in cmd or "shutdown my computer" in cmd:
            self.set_response("As you wish! Shutting down your computer...")
            print(colorama.Fore.YELLOW + self.get_response())
            self.speak(self.get_response())
            os.system("shutdown /s /t 0")
            self.sound_system.playShutdownSound()
            self.set_running(False)
        elif "restart my computer" in cmd:
            self.set_response("As you wish! Restarting your computer...")
            print(colorama.Fore.YELLOW + self.get_response())
            self.speak(self.get_response())
            os.system("shutdown /r")
            self.sound_system.playShutdownSound()
            self.set_running(False)
        elif "sign off my computer" in cmd or "signoff my computer" in cmd:
            self.set_response("As you wish! Signing off your computer...")
            print(colorama.Fore.YELLOW + self.get_response())
            self.speak(self.get_response())
            os.system("shutdown /l")
            self.sound_system.playShutdownSound()
            self.set_response(f"Successfully signed off {self.get_user_name()}'s computer.")
            print(colorama.Fore.YELLOW + self.get_response())
            self.speak(self.get_response())
            self.set_running(False)
        elif "logout my computer" in cmd or "log out my computer" in cmd:
            self.set_response("As you wish! Logging out your computer...")
            print(colorama.Fore.YELLOW + self.get_response())
            self.speak(self.get_response())
            os.system("shutdown /l")
            self.sound_system.playShutdownSound()
            self.set_response(f"Successfully logged off {self.get_user_name()}'s computer.")
            print(colorama.Fore.YELLOW + self.get_response())
            self.speak(self.get_response())
            self.set_running(False)
        elif "sign out my computer" in cmd or "signout my computer" in cmd:
            self.set_response("As you wish! Signing out your computer...")
            print(colorama.Fore.YELLOW + self.get_response())
            self.speak(self.get_response())
            os.system("shutdown /l")
            self.sound_system.playShutdownSound()
            self.set_response(f"Successfully signed out {self.get_user_name()}'s computer.")
            print(colorama.Fore.YELLOW + self.get_response())
            self.speak(self.get_response())
            self.set_running(False)
        elif ("increase" in cmd and "volume" in cmd) or "volume up" in cmd:
            self.set_response("Increasing volume...")
            print(colorama.Fore.YELLOW + self.get_response())
            self.speak(self.get_response())
            pyautogui.press("volumeup", presses=10)
            self.set_response(f"Successfully increased the volume of {self.get_user_name()}'s computer.")
            print(colorama.Fore.YELLOW + self.get_response())
            self.speak(self.get_response())
        elif ("volume" in cmd and "decrease" in cmd) or "lower" in cmd:
            self.set_response("Decreasing volume...")
            print(colorama.Fore.YELLOW + self.get_response())
            self.speak(self.get_response())
            pyautogui.press("volumedown", presses=10)
            self.set_response(f"Successfully lowered the volume of {self.get_user_name()}'s computer.")
            print(colorama.Fore.YELLOW + self.get_response())
            self.speak(self.get_response())
        elif ("battery" in cmd and "status" in cmd) or "level" in cmd or "percentage" in cmd:
            battery = psutil.sensors_battery()
            percentage = battery.percent
            self.set_response(f"The current battery percentage is {percentage}%")
            print(colorama.Fore.YELLOW + self.get_response())
            self.speak(self.get_response())
        elif any(hotword in cmd for hotword in self.STANDBY_HOTWORDS):
            self.set_response("As you wish " + self.get_honorific_address() + "!")
            print(colorama.Fore.YELLOW + self.get_response())
            self.speak(self.get_response())
            self.standby()
        elif cmd in [".", " ", "", "[]", None]:
            self.set_response("Hello? Are you still there?")
            print(colorama.Fore.YELLOW + self.get_response())
            self.speak(self.get_response())
            self.standby()
        else:
            try:
                command = cmd
                self.agent.update_realtime_data()
                response = self.agent.get_response(command)
                self.set_command(command)
                self.set_response(response)
                print(colorama.Fore.LIGHTGREEN_EX + self.get_command())
                print(colorama.Fore.LIGHTMAGENTA_EX + self.get_response())
                self.speak(self.get_response())
            except Exception as e:
                self.set_response("I beg your pardon, I'm afraid I didn't catch that.")
                print(colorama.Fore.LIGHTRED_EX + self.get_response())
                self.speak(self.get_response())

    # ------------------ Iterative Pipeline ------------------
    def iterative_pipeline(self) -> None:
        while self.get_running():
            try:
                previous_command = self.get_command()
                current_command = self.listen_command()
                
                if previous_command == current_command:
                    time.sleep(3)
                else:
                    try:
                        self.process_command(command_input=current_command, response_input=self.get_response())
                    except Exception as e:
                        print(colorama.Fore.LIGHTRED_EX + f"\nError occurred while processing the command: {e}")
                        self.set_response("I beg your pardon, I'm afraid I didn't catch that.")
                        self.speak(self.get_response())
            
            except requests.exceptions.ConnectionError as ce:
                print(colorama.Fore.LIGHTRED_EX + f"\nA connection error occurred: {ce}")
            except Exception as e:
                print(colorama.Fore.LIGHTRED_EX + f"\nAn error occurred: {e}")

    def main(self) -> None:
        try:
            self.start_up_sequence()
            self.iterative_pipeline()
            self.close_program(program_name="WindowsTerminal.exe")
        except Exception as e:
            self.sound_system.playErrorSound()
            print(colorama.Fore.LIGHTRED_EX + f"\nAn error occurred while running H.A.R.A.Y.A: {e}")
        finally:
            pygame.quit()
            sys.exit()

if __name__ == '__main__':
    haraya_v4_instance = HarayaV4()
    haraya_v4_instance.main()

# Run Command: python haraya_v4.py

