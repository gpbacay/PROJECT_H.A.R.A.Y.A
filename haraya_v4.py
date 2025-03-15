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

class haraya_v4:
    # python haraya_v4.py
    #________________________ Constructor _________________________
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

    #________________________ Setters _________________________
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

    #________________________ Getters _________________________
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

    #________________________ Methods _________________________
    def initialize_ai_agent(self) -> None: # Initialize AI Agent
        try:
            self.agent = HarayaAgent(ai_name=self.get_ai_name(), user_name=self.get_user_name())
        except Exception as e:
            print(colorama.Fore.LIGHTRED_EX + f"Error initializing AI Agent: {e}")
            self.agent = None

    def register_new_command_to_ai_agent(self, new_command: str) -> str: # Register new command to AI Agent
        response = ""
        try:
            if self.agent is not None: # Check if AI Agent is initialized
                self.set_command(new_command)
                ai_command = self.get_command()
                response = self.agent.get_response(ai_command)
                self.set_response(response)
            else:
                print(colorama.Fore.LIGHTRED_EX + "AI Agent not initialized.")
        except Exception as error:
            print(colorama.Fore.LIGHTRED_EX + f"Error in register_new_command_to_ai_agent: {error}")
        finally:
            return response

    def initialize_honorific_address(self) -> None: # Initialize Honorific Address based on User Name
        male_names = [
            "Gianne Bacay", "Earl Jay Tagud", "Gemmuel Balceda", "Mark Anthony Lagrosa",
            "Klausmieir Villegas", "CK Zoe Villegas", "Alexander Villasis", "Bryan Sarpamones"
        ]
        female_names = [
            "Kleinieir Pearl Kandis Bacay", "Princess Viznar", "Nichi Bacay", "Roz Waeschet Bacay"
        ]
        
        try:
            user_name = self.get_user_name()
            if user_name in male_names:
                honorific_address = "Sir"
            elif user_name in female_names:
                honorific_address = "Ma'am"
            else:
                honorific_address = "Boss"
        except Exception as error:
            print(colorama.Fore.LIGHTRED_EX + f"Error determining honorific address: {error}")
            honorific_address = "Master"
        
        self.set_honorific_address(honorific_address)

    def speak(self, text: str) -> None: # Speak the text
        self.isSpeaking(1)
        self.engine.say(text)
        self.engine.runAndWait()
        self.isSpeaking(0)

    def initialize_face_recognition_system(self) -> None: # Initialize Face Recognition System
        response = "Recognizing Face"
        self.set_response(response)
        self.speak(response)
        self.thread_3.join()
        self.runLoadingBar(seconds=0.5, loading_tag="RECOGNIZING FACE...", end_tag="FACE RECOGNIZED!")
        self.user_profile.init_user_name()
        self.set_user_ame(self.user_profile.get_user_name())
        self.initialize_honorific_address()

    def initialize_pose_recognition_system(self) -> None: # Initialize Pose Recognition System
        response = "RECOGNIZING POSE..."
        self.set_response(response)
        self.speak(response)
        print(colorama.Fore.GREEN + response)
        self.thread_4.start()
        self.thread_5.start()

    def start_up_sequence(self) -> None: # Start-up Sequence
        self.initialize_face_recognition_system()
        try:
            if self.agent is not None:
                response = self.agent.get_response(question=f"Hi {self.get_ai_name()}, My name is {self.get_user_name()}.")
                print(colorama.Fore.GREEN + response)
            else:
                response = f"Hi {self.get_honorific_address()} {self.get_user_name()}, I am {self.get_ai_name()}, your personal AI assistant! How can I help you?"
                print(colorama.Fore.GREEN + response)
        except Exception as e:
            print(colorama.Fore.RED + f"An error occurred during start-up sequence: {e}")
            response = f"Hi {self.get_honorific_address()} {self.get_user_name()}, I am {self.get_ai_name()}, your personal AI assistant! How can I help you?"
            print(colorama.Fore.GREEN + response)
        finally:
            self.set_response(response)
            self.speak(response)

    def listen_command(self) -> str: # Listen for command
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
                ai_command = ai_command.lower()
                self.set_ai_command(ai_command)
        except Exception as e:
            print(colorama.Fore.LIGHTRED_EX + f"\nAn error occurred while listening for a command: {e}")
        finally:
            return command

    def wait_command(self) -> str: # Wait for command
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
                ai_command = ai_command.lower()
                self.set_ai_command(ai_command)
        except Exception as e:
            print(colorama.Fore.LIGHTRED_EX + f"An error occurred while waiting for a command: {e}")
        finally:
            self.isWaiting(False)
            return command

    def register_command(self, command_input: str) -> str: # Register command
        command = command_input
        response = self.get_response()
        interrogatives = ['what', ' what ', 'who', ' who ', 
                                'where', ' where ', 'when', ' when ', 
                                'why', ' why ', 'how', ' how ']
        try:
            if any(hotword in command for hotword in interrogatives):
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
                ai_command = ai_command.lower()
                self.set_ai_command(ai_command)
        except Exception as e:
            print(colorama.Fore.LIGHTRED_EX + f"An error occurred while registering a command: {e}")
        finally:
            return command

    def standby(self) -> None: # Standby Mode
        while True:
            command = self.wait_command()
            if "hey" in command or "haraya" in command:
                response = "How can I help you?"
                print(colorama.Fore.GREEN + response)
                self.speak(response)
                break
        return

    def confirm_command(self) -> str: # Confirm Command
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

    def close_program(self, program_name: str) -> None: # Close a Program
        try:
            response = "Closing " + program_name + "..."
            print(colorama.Fore.GREEN + "Closing " + colorama.Fore.LIGHTRED_EX + program_name + colorama.Fore.GREEN + "...")
            self.speak(response)
            closed = False
            for process in psutil.process_iter(['pid', 'name']):
                if process.info['name'] == program_name:
                    try:
                        process.terminate()
                        response = program_name + " has been closed."
                        print(colorama.Fore.GREEN + response)
                        self.speak(response)
                        closed = True
                    except psutil.AccessDenied:
                        self.sound_system.playErrorSound()
                        response = "Permission denied. Unable to close " + program_name + "."
                        print(colorama.Fore.LIGHTRED_EX + response)
                        self.speak(response)
                    except psutil.NoSuchProcess:
                        self.sound_system.playErrorSound()
                        response = program_name + " is not running."
                        print(colorama.Fore.LIGHTRED_EX + response)
                        self.speak(response)
                    break
            if not closed:
                print(colorama.Fore.GREEN + f"{program_name} is not running.")
        except Exception as e:
            self.sound_system.playErrorSound()
            print(colorama.Fore.LIGHTRED_EX + f"An error occurred while closing {program_name}: {e}")

    def recursive_pipeline(self) -> None: # Recursive Pipeline
        if not self.get_running():
            return
        try:
            previous_command = self.get_command()
            current_command = self.listen_command()
            if previous_command == current_command:
                time.sleep(3)
            else:
                self.agent.update_realtime_data()
                self.register_new_command_to_ai_agent(current_command)
                try:
                    command = current_command
                    print(colorama.Fore.LIGHTGREEN_EX + command)
                    self.agent.update_realtime_data()
                    response = self.agent.get_response(command)
                    self.set_response(response)
                except Exception as e:
                    print(colorama.Fore.LIGHTRED_EX + f"\nError occured while running the AI Agent: {e}")
                    response = "I beg your pardon, I'm afraid I didn't catch that."
                    self.set_response(response)
                    pass
                else:
                    self.set_command(command)
                    self.set_response(response)
                    print(colorama.Fore.YELLOW + response)
                    self.speak(response)
        except requests.exceptions.ConnectionError as ce:
            print(colorama.Fore.LIGHTRED_EX + f"\nA connection error occurred: {ce}")
        except Exception as e:
            print(colorama.Fore.LIGHTRED_EX + f"\nAn error occurred: {e}")
        finally:
            self.recursive_pipeline()

    def main(self): # Main Method
        try:
            self.start_up_sequence()
            self.recursive_pipeline()
            self.close_program(program_name="WindowsTerminal.exe")
        except Exception as e:
            self.sound_system.playErrorSound()
            print(colorama.Fore.LIGHTRED_EX + f"\nAn error occurred while running H.A.R.A.Y.A: {e}")
        finally:
            pygame.quit()
            sys.exit()

if __name__ == '__main__':
    haraya_v4_instance = haraya_v4()
    haraya_v4_instance.main()

#Run Command: python haraya_v4.py

