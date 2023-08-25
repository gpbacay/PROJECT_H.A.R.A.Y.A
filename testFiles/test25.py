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

    try:
        with sr.Microphone() as source:
            recognizer.pause_threshold = 1.5
            Play_Listening_Sound()
            
            def stop_listener(voice_input):
                nonlocal stop_listening
                input("Press Enter to stop listening...\n")
                stop_listening = True
                command = recognizer.recognize_google(voice_input, show_all=True)
                if command:                        
                    command = str(command).lower()
                    print("Command:", command)
            
            while stop_listening == False:
                print(colorama.Fore.CYAN + "Listening...")
                voice = recognizer.listen(source)
                stop_thread = threading.Thread(target=stop_listener, args=(voice,))
                stop_thread.start()  # Start the thread to listen for the Enter key
                
                if stop_listening == False:
                    command = recognizer.recognize_google(voice, show_all=True)
                    if command:
                        command = str(command).lower()
                        print("Command:", command)
            
    except sr.WaitTimeoutError:
        pass
    except KeyboardInterrupt:
        pass
    finally:
        stop_thread.join()  # Wait for the thread to finish before returning
    return command

Listen_command_MainFunction()

#_____________________python test25.py