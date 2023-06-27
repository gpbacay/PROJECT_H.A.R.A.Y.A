import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

from embedchain import App 
bot = App()

def run_embedChain(command):
    bot.query(command)

#prompt = "how to cook pizza?"
#run_embedChain(prompt)

import speech_recognition as sr

recognizer = sr.Recognizer()

print("Listening...")
try:
    with sr.Microphone() as source:
        recognizer.pause_threshold = 1.5
        voice = recognizer.listen(source, timeout=10)
except:
    pass
text = recognizer.recognize_google(voice)
print(text)

#__________________python embedChain.py
