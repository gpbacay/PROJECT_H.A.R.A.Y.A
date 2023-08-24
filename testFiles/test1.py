import speech_recognition as sr

recognizer = sr.Recognizer()

print("Listening...")
try:
    with sr.Microphone() as source:
        recognizer.pause_threshold = 1.5
        voice = recognizer.listen(source, timeout=5, phrase_time_limit=5)
except:
    pass
text = recognizer.recognize_google(voice)
print(text)

#________________python test1.py