from gtts import gTTS
from playsound import playsound
import os

text = "Hello Gianne P. Bacay, I am Haraya, your virtual assistant AI"

tts = gTTS(text=text, lang="en", slow=False, tld="co.uk")

tts.save("tts.mp3")

playsound("tts.mp3")

os.remove("tts.mp3")

#___________python test21.py