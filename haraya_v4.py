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
        self.HonorificAddress = "."
        
        # Thread 1: AI Agent System
        self.tAIAgent = Thread(target=HarayaAgent, kwargs={"ai_name": self.getAIName(), "user_name": self.getUserName()}, daemon=True)
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
        self.tAIAgent.join() # Wait for the AI Agent System to finish
        
     #_________________________________________________________Setters
    # Run Command: python haraya_v4.py
    def setRunning(self, Running_input: bool):
        self.running = Running_input
    def setAIName(self, AIName_input: str):
        self.ai_name = AIName_input
    def setCommand(self, command_input: str):
        self.command = command_input
    def setAICommand(self, ai_command_input: str):
        self.ai_command = ai_command_input
    def setResponse(self, response_input: str):
        self.response = response_input
    def setUserName(self, user_name_input: str):
        self.user_name = user_name_input
    def setHonorificAddress(self, HonorificAddress_input: str):
        self.HonorificAddress = HonorificAddress_input
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
        return self.HonorificAddress
    
    #_________________________________________________________Methods
    def initialize_face_recognition_system(self):
        response = "Initializing Face Recognition System"
        self.speak(response)
        tFRS = Thread(target=Face_Recognition_System)
        tFRS.start()
        tFRS.join()
        self.runLoadingBar(seconds=0.5, loading_tag="RECOGNIZING FACE...", end_tag="FACE RECOGNIZED!")
        self.initUserName()
        self.initHonorificAddress()
    
    
    
    
    def main(self):
        print("Initializing G.O.D.S.E.Y.E.S")






if __name__ == '__main__':
    haraya_v4 = haraya_v4()
    haraya_v4.main()

#Run Command: python haraya_v4.py
