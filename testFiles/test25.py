import speech_recognition as sr
import colorama
import pygame
import threading

# Initialize SpeechRecognition recognizer
recognizer = sr.Recognizer()

def Play_Listening_Sound():
    # Define your function to play the listening sound here
    pass

def Listen_command_MainFunction():
    global command
    command = ""
    stop_listening = False

    def stop_listener():
        nonlocal stop_listening
        input("Press Enter to stop listening...\n")
        stop_listening = True

    stop_thread = threading.Thread(target=stop_listener)

    try:
        with sr.Microphone() as source:
            recognizer.pause_threshold = 1.5
            Play_Listening_Sound()

            stop_thread.start()  # Start the thread to listen for the Enter key
            
            while not stop_listening:
                print(colorama.Fore.CYAN + "Listening...")
                voice = recognizer.listen(source)
                text = recognizer.recognize_google(voice, show_all=True)
                if text:
                    print("Command:", text)
                    text = str(text).lower()
            
    except sr.WaitTimeoutError:
        pass
    except KeyboardInterrupt:
        pass
    finally:
        stop_thread.join()  # Wait for the thread to finish before returning

Listen_command_MainFunction()




#_____________________python test25.py