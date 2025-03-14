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
from AI_Agents.haraya_agent import HarayaAgent
from face_recognition_system import Face_Recognition_System
from pose_recognition_system import Pose_Recognition_System
from web_data_scraping_system import DataScraper
from loading_bar import LoadingBar
from haraya_gui import harayaUI


class haraya_v4:
    def __init__(self):
        HarayaHeading()
        pass

    def main(self):
        print("Initializing G.O.D.S.E.Y.E.S")






if __name__ == '__main__':
    haraya_v3 = haraya_v4()
    haraya_v3.main()

#Run Command: python haraya_v4.py
