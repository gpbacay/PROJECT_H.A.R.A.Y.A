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
from face_recognition_system import Face_Recognition_System
from pose_recognition_system import Pose_Recognition_System
from web_data_scraping_system import DataScraper
from loading_bar import LoadingBar
from haraya_gui import HarayaUI
from user_profile import UserProfile


class haraya_v4:
    #_________________________________________________________Constructor
    # Run Command: python haraya_v4.py
    def __init__(self, running: bool = True, ai_name: str = "Haraya", command: str = ".",
                response: str = ".", user_name: str = ".") -> None:
        self.running = True
        self.ai_name = "Haraya"
        self.user_name = "."
        self.command = "."
        self.ai_command = "."
        self.response = "."
        self.honorific_address = "."
        
        # Thread 1: AI Agent System
        self.tAIAgent = Thread(target=self.init_agent, daemon=True)
        self.tAIAgent.start()
        
        # Thread 2: GUI System
        self.run_gui = HarayaUI.runUI
        self.isSpeaking = HarayaUI.isSpeaking
        self.isWaiting = HarayaUI.isWaiting
        self.tGUI = Thread(target=self.run_gui, daemon=True)
        self.tGUI.start()
        
        # Main Thread
        HarayaHeading()
        self.sound_system = SoundSystem()
        colorama.init(autoreset=True)
        pygame.init()
        self.loading_bar = LoadingBar()
        self.runLoadingBar = self.loading_bar.run_loadingbar
        
        self.user_profile = UserProfile()
        
        self.tAIAgent.join() # Wait for the AI Agent System to finish
        
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voices[1].id)
        
        self.StartUpSequence()
        
     #_________________________________________________________Setters
    # Run Command: python haraya_v4.py
    def setRunning(self, running_input: bool):
        self.running = running_input
    def setAIName(self, ai_name_input: str):
        self.ai_name = ai_name_input
    def setCommand(self, command_input: str):
        self.command = command_input
    def setAICommand(self, ai_command_input: str):
        self.ai_command = ai_command_input
    def setResponse(self, response_input: str):
        self.response = response_input
    def setUserName(self, user_name_input: str):
        self.user_name = user_name_input
    def setHonorificAddress(self, honorific_address_input: str):
        self.honorific_address = honorific_address_input
    #_________________________________________________________Getters
    # Run Command: python haraya_v4.py
    def getRunning(self):
        return self.running
    def getAIName(self):
        return self.ai_name
    def getCommand(self):
        return self.command
    def getAICommand(self):
        return self.ai_command
    def getResponse(self):
        return self.response
    def getUserName(self):
        return self.user_name
    def getHonorificAddress(self):
        return self.honorific_address
    
    #_________________________________________________________Methods
    # Run Command: python haraya_v4.py
    def init_agent(self) -> None: 
        self.agent = HarayaAgent(ai_name=self.getAIName(), user_name=self.getUserName())
    
    def initHonorificAddress(self) -> None: # Initialize Honorific Address based on the User's Name
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
            Gender_Name = self.getUserName()
            if Gender_Name in Male_Names:
                honorific_address = "Sir"
            elif Gender_Name in Female_Names:
                honorific_address = "Ma'am"
            else:
                honorific_address = "Boss"
        except:
            honorific_address = "Master"
        finally:
            self.setHonorificAddress(honorific_address_input=honorific_address)
            
    def speak(self, text: str) -> None: # Speak the text using pyttsx3
        self.isSpeaking(1)
        self.engine.say(text)
        self.engine.runAndWait()
        self.isSpeaking(0)
        
    def initialize_face_recognition_system(self) -> None: # Initialize the Face Recognition System
        response = "Initializing Face Recognition System"
        self.setResponse(response_input=response)
        self.speak(response)
        tFRS = Thread(target=Face_Recognition_System)
        tFRS.start()
        tFRS.join()
        self.runLoadingBar(seconds=0.5, loading_tag="RECOGNIZING FACE...", end_tag="FACE RECOGNIZED!")
        self.user_profile.init_user_name()
        self.setUserName(user_name_input=self.user_profile.get_user_name())
        self.initHonorificAddress()
    
    def StartUpSequence(self) -> None:
        self.initialize_face_recognition_system()
        try:
            response = self.agent.get_response(question=f"Hi {self.getAIName()}, I am {self.getUserName()}.")
            print(colorama.Fore.GREEN + response)
        except Exception as e:
            print(colorama.Fore.RED + f"An error occurred: {e}")
            response = f"Hi {self.getHonorificAddress()} {self.getUserName()}, I am {self.getAIName()}, your personal AI assistant! How can I help you?"
            response1 = (colorama.Fore.GREEN + "Hi " + self.getHonorificAddress() + " " +
                        colorama.Fore.CYAN + self.getUserName() + colorama.Fore.GREEN +
                        "! I am Haraya, your personal AI assistant! How can I help you?")
            print(response1)
        finally:
            self.setResponse(response)
            self.speak(response)
            return
    
    
    def main(self):
        print("Initializing G.O.D.S.E.Y.E.S")






if __name__ == '__main__':
    haraya_v4 = haraya_v4()
    haraya_v4.main()

#Run Command: python haraya_v4.py
