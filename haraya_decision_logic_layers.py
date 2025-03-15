import os
import requests
import subprocess
import psutil
import pyautogui
import wikipedia
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pygame
import colorama
from threading import Thread

class HarayaDecisionLogic:
    """
    This decision logic layer processes an incoming command (with an initial response)
    and routes it to the appropriate subsystem. It relies entirely on the HarayaV4 instance
    (passed to its constructor) for all functionality (e.g. speaking, listening, state management).
    """
    # Hotword lists defined as class constants
    STANDBY_HOTWORDS = [
        "standby", "stand by", "haraya stand by", "just stand by", "wait",
        "wait a sec", "give me a sec", "hold for a sec", "wait for a sec",
        "give me a second", "hold for a second", "wait for a second",
        "give me a minute", "hold for a minute", "wait for a minute",
        "give me an hour", "hold for an hour", "wait for an hour",
        "just a moment", "just a sec", "just a minute", "just an hour",
        "call you later", "i'll be back", "be right back"
    ]
    GOODBYE_HOTWORDS = [
        "goodbye", "good bye", "haraya goodbye", "goodbye haraya", "haraya bye",
        "bye haraya", "bye", "let's call it a day", "i said goodbye",
        "you're good to go", "you can go", "you can go now", "you can go to sleep now",
        "i need to go", "ciao", "sayonara", "It was nice chatting with you",
        "It was nice chatting to you", "I hope you have a great day!",
        "I hope you have a good day!", "Have a great day!", "Have a good day!", "Goodbye!"
    ]
    STOP_HOTWORDS = [
        "sign off", "haraya stop", "stop please", "go to sleep", "go to rest",
        "just go to sleep", "just go to rest", "go to sleep haraya", "stop listening",
        "terminate yourself", "enough", "that's enough", "I said enough",
        "I said stop", "you can go to sleep now", "i told you to go to sleep",
        "didn't i told you to go to sleep", "didn't i told you to sleep", "i told you to stop",
        "didn't i told you to stop", "turn off", "shutdown", "dismiss"
    ]
    YES_HOTWORDS = [
        "yes", "yup", "yes please", "of course yes", "yes I do", "I do",
        "you got it right", "yes actually", "actually yes", "that's a yes",
        "I think yes", "sure", "yah", "absolutely yes", "definitely yes",
        "you got it right", "I said yes", "affirmative"
    ]
    NO_HOTWORDS = [
        "no", "no thank you", "nope", "no please", "of course no", "no I don't",
        "I don't think so", "you got it wrong", "no actually", "actually no",
        "that's a no", "I'm not", "I think not", "none so far", "I'm not sure",
        "noh", "nah", "none", "that's a no no", "absolutely no", "definitely no",
        "absolutely not", "definitely not", "incorrect", "I said no", "negative"
    ]
    GOOGLE_SEARCH_HOTWORDS = [
        "in google search", "search in google", "in google navigate",
        "navigate in google", "in google find", "find in google", "in google",
        "google search", "go on google", "go in google", "on google",
        "search in chrome", "go to chrome", "go in chrome", "go on chrome", "google"
    ]
    YOUTUBE_SEARCH_HOTWORDS = [
        "in youtube search", "search in youtube", "in youtube play",
        "play in youtube", "in youtube find", "find in youtube", "in youtube",
        "youtube search", "go on youtube", "go in youtube", "go to youtube",
        "on youtube", "youtube please", "youtube"
    ]
    WIKIPEDIA_SEARCH_HOTWORDS = [
        "in wikipedia search", "search in wikipedia", "in wikipedia find",
        "find in wikipedia", "in wikipedia", "wikipedia search", "go on wikipedia",
        "on wikipedia", "wikipedia"
    ]
    OPEN_HOTWORDS = ["open", "access", "go to", "go in", "run", "launch"]
    CLOSE_HOTWORDS = ["close", "terminate", "go out", "exit", "escape", "quit", "return", "close"]

    def __init__(self, haraya_instance):
        # Simply save the HarayaV4 instance; all libraries, subsystems,
        # and state methods are assumed to be initialized in that instance.
        self.haraya = haraya_instance

    def process_command(self, command_input: str, response_input: str) -> None:
        """
        Processes the given command (and initial response) by evaluating a series
        of if/elif statements to determine which action to perform. All actions
        are delegated to methods of the HarayaV4 instance.
        """
        # Update command and response in the HarayaV4 instance.
        self.haraya.set_command(str(command_input))
        self.haraya.set_response(str(response_input))
        # Update real-time data.
        Thread(target=self.haraya.data_scraper.initCurrentTime).start()
        Thread(target=self.haraya.data_scraper.initCurrentDate).start()
        # Update user identity and honorific address.
        self.haraya.user_profile.init_user_name()
        self.haraya.initialize_honorific_address()
        # Optionally, update the agent asynchronously.
        Thread(target=lambda: self.haraya.register_new_command_to_ai_agent(self.haraya.get_command())).start()

        # Get the lowercase command for matching.
        cmd = self.haraya.get_command().lower()

        # --- Decision Logic Blocks ---
        if "run" in cmd or "activate" in cmd or "initialize" in cmd:
            if "face recognition system" in cmd:
                try:
                    self.haraya.set_command(f"Hi! my name is {self.haraya.get_user_name()}")
                    self.haraya.set_response("Haraya's face recognition system was initialized.")
                    self.haraya.speak(self.haraya.get_response())
                except Exception as e:
                    self.haraya.set_response("I beg your pardon, I'm afraid I didn't catch that.")
                    self.haraya.speak(self.haraya.get_response())
            elif "pose recognition system" in cmd or "gods eyes" in cmd or \
                 "post recognition system" in cmd or "godseyes" in cmd:
                self.haraya.set_response("Haraya's pose recognition system was initialized.")
                self.haraya.speak(self.haraya.get_response())
            elif "web data scraping system" in cmd:
                # Reinitialize data scraper.
                self.haraya.data_scraper.__init__()
                self.haraya.set_response("Haraya's web data scraping system was initialized.")
                self.haraya.speak(self.haraya.get_response())

        elif any(hotword == cmd for hotword in self.STOP_HOTWORDS):
            self.haraya.initialize_honorific_address()
            self.haraya.set_response("As you wish " + self.haraya.get_honorific_address() + ". Signing off...")
            self.haraya.speak(self.haraya.get_response())
            self.haraya.sound_system.playShutdownSound()
            self.haraya.set_running(False)
        elif any(hotword == cmd for hotword in self.GOODBYE_HOTWORDS):
            self.haraya.set_response("Goodbye " + self.haraya.get_honorific_address() + "! Have a great day!")
            self.haraya.speak(self.haraya.get_response())
            self.haraya.sound_system.playShutdownSound()
            self.haraya.set_running(False)

        elif any(hotword == cmd for hotword in self.GOOGLE_SEARCH_HOTWORDS):
            self.haraya.set_response("What would you like to search in Google?")
            self.haraya.speak(self.haraya.get_response())
            self.haraya.set_command(self.haraya.listen_command())
            try:
                info = (self.haraya.get_command()
                        .replace("search in google", "")
                        .replace("haraya", "")
                        .replace("search", "")
                        .replace("in google", "")
                        .replace("google", "")
                        .replace("can you", "")
                        .replace("help me", "")).strip()
                self.haraya.set_response("Searching " + info)
                self.haraya.speak(self.haraya.get_response())
                Thread(target=self.haraya.sound_system.playListeningSound).start()
                for i in range(3):
                    search = info.replace(' ', '+')
                    chrome_service = Service('./chromedriver.exe')
                    browser = webdriver.Chrome(service=chrome_service)
                    browser.get("https://www.google.com/search?q=" + search + "&start" + str(i))
                self.haraya.set_response("Here's what I've found.")
                self.haraya.speak(self.haraya.get_response())
            except Exception as e:
                self.haraya.sound_system.playErrorSound()
                self.haraya.set_response(f"An error occurred while searching in Chrome: {e}")

        elif any(hotword == cmd for hotword in self.YOUTUBE_SEARCH_HOTWORDS):
            self.haraya.set_response("What would you like to search or play in YouTube?")
            self.haraya.speak(self.haraya.get_response())
            self.haraya.set_command(self.haraya.listen_command())
            try:
                self.haraya.set_response("Searching...")
                self.haraya.speak(self.haraya.get_response())
                Thread(target=self.haraya.sound_system.playListeningSound).start()
                song_title = (self.haraya.get_command()
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
                self.haraya.set_response("Now Playing " + song_title)
                self.haraya.speak(self.haraya.get_response())
            except Exception as e:
                self.haraya.sound_system.playErrorSound()
                self.haraya.set_response(f"An error occurred while playing in YouTube: {e}")

        elif any(hotword == cmd for hotword in self.WIKIPEDIA_SEARCH_HOTWORDS):
            self.haraya.set_response("What would you like to search in Wikipedia?")
            self.haraya.speak(self.haraya.get_response())
            self.haraya.set_command(self.haraya.listen_command())
            try:
                self.haraya.set_response("Searching...")
                self.haraya.speak(self.haraya.get_response())
                Thread(target=self.haraya.sound_system.playListeningSound).start()
                person = (self.haraya.get_command()
                          .replace("search in wikipedia", "")
                          .replace("in wikipedia search", "")
                          .replace("haraya", "")
                          .replace("who is", "")).strip()
                info = wikipedia.summary(person, sentences=1)
                self.haraya.speak(info)
            except Exception as e:
                self.haraya.sound_system.playErrorSound()
                self.haraya.set_response(f"An error occurred while searching in Wikipedia: {e}")

        elif any(hotword in cmd for hotword in self.OPEN_HOTWORDS):
            Thread(target=self.haraya.sound_system.playListeningSound).start()
            try:
                if "chrome" in cmd or "google" in cmd:
                    self.haraya.set_response("As you wish!")
                    self.haraya.speak(self.haraya.get_response())
                    program = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
                    subprocess.Popen([program])
                    self.haraya.set_response("Opening Chrome...")
                    self.haraya.speak(self.haraya.get_response())
                else:
                    self.haraya.set_response("I beg your pardon, I'm afraid I didn't catch that.")
                    self.haraya.speak(self.haraya.get_response())
            except Exception as e:
                self.haraya.sound_system.playErrorSound()
                self.haraya.set_response(f"An error occurred while trying to open the program: {e}")

        elif any(hotword == cmd for hotword in self.CLOSE_HOTWORDS):
            try:
                if "chrome" in cmd or "tab" in cmd:
                    self.haraya.set_response(self.haraya.close_program("chrome.exe"))
                elif "command prompt" in cmd or "windows terminal" in cmd:
                    self.haraya.set_response(self.haraya.close_program("WindowsTerminal.exe"))
                elif "messenger" in cmd:
                    self.haraya.set_response(self.haraya.close_program("Messenger.exe"))
                elif "file explorer" in cmd or "windows explorer" in cmd:
                    self.haraya.set_response(self.haraya.close_program("explorer.exe"))
            except Exception as e:
                self.haraya.sound_system.playErrorSound()
                self.haraya.set_response(f"An error occurred while trying to close the program: {e}")

        elif "turn off my computer" in cmd or "shutdown my computer" in cmd:
            self.haraya.set_response("As you wish! Shutting down your computer...")
            self.haraya.speak(self.haraya.get_response())
            os.system("shutdown /s /t 0")
            self.haraya.sound_system.playShutdownSound()
            self.haraya.set_running(False)
        elif "restart my computer" in cmd:
            self.haraya.set_response("As you wish! Restarting your computer...")
            self.haraya.speak(self.haraya.get_response())
            os.system("shutdown /r")
            self.haraya.sound_system.playShutdownSound()
            self.haraya.set_running(False)
        elif "sign off my computer" in cmd or "signoff my computer" in cmd:
            self.haraya.set_response("As you wish! Signing off your computer...")
            self.haraya.speak(self.haraya.get_response())
            os.system("shutdown /l")
            self.haraya.sound_system.playShutdownSound()
            self.haraya.set_response(f"Successfully signed off {self.haraya.get_user_name()}'s computer.")
            self.haraya.set_running(False)
        elif "logout my computer" in cmd or "log out my computer" in cmd:
            self.haraya.set_response("As you wish! Logging out your computer...")
            self.haraya.speak(self.haraya.get_response())
            os.system("shutdown /l")
            self.haraya.sound_system.playShutdownSound()
            self.haraya.set_response(f"Successfully logged off {self.haraya.get_user_name()}'s computer.")
            self.haraya.set_running(False)
        elif "sign out my computer" in cmd or "signout my computer" in cmd:
            self.haraya.set_response("As you wish! Signing out your computer...")
            self.haraya.speak(self.haraya.get_response())
            os.system("shutdown /l")
            self.haraya.sound_system.playShutdownSound()
            self.haraya.set_response(f"Successfully signed out {self.haraya.get_user_name()}'s computer.")
            self.haraya.set_running(False)
        elif ("increase" in cmd and "volume" in cmd) or "volume up" in cmd:
            self.haraya.set_response("Increasing volume...")
            self.haraya.speak(self.haraya.get_response())
            pyautogui.press("volumeup", presses=10)
            self.haraya.set_response(f"Successfully increased the volume of {self.haraya.get_user_name()}'s computer.")
        elif ("volume" in cmd and "decrease" in cmd) or "lower" in cmd:
            self.haraya.set_response("Decreasing volume...")
            self.haraya.speak(self.haraya.get_response())
            pyautogui.press("volumedown", presses=10)
            self.haraya.set_response(f"Successfully lowered the volume of {self.haraya.get_user_name()}'s computer.")
        elif ("battery" in cmd and "status" in cmd) or "level" in cmd or "percentage" in cmd:
            battery = psutil.sensors_battery()
            percentage = battery.percent
            self.haraya.set_response(f"The current battery percentage is {percentage}%")
            self.haraya.speak(self.haraya.get_response())
        elif any(hotword == cmd for hotword in self.STANDBY_HOTWORDS):
            self.haraya.set_response("As you wish " + self.haraya.get_honorific_address() + "!")
            self.haraya.speak(self.haraya.get_response())
            self.haraya.standby()
        elif cmd in [".", " ", "", "[]", None]:
            self.haraya.set_response("Hello? Are you still there?")
            self.haraya.speak(self.haraya.get_response())
            self.haraya.standby()
        else:
            try:
                command = cmd
                self.agent.update_realtime_data()
                response = self.agent.get_response(command)
                self.haraya.set_response(response)
            except Exception as e:
                response = "I beg your pardon, I'm afraid I didn't catch that."
                self.haraya.set_response(response)
            else:
                self.haraya.set_command(command)
                self.haraya.set_response(response)
                self.haraya.speak(self.haraya.get_response())

    # Note: This module contains no recursive loop; it is intended to be called from HarayaV4.
    
# ---------------------- Main Entry Point ----------------------
if __name__ == '__main__':
    # For standalone testing only – this module is normally invoked by HarayaV4.
    from haraya_v4 import HarayaV4
    haraya_instance = HarayaV4()
    decision_logic = HarayaDecisionLogic(haraya_instance)
    decision_logic.process_command("what is the battery status", "initial response")


# Run Command: python haraya_decision_logic_layers.py
