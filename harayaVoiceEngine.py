import os
from google.cloud import texttospeech
import pyaudio

# Set your Google Cloud credentials as you did before
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"nodal-skein-392905-babe98c4288f.json"

def Speak(input_text: str):
    # Initialize the Text-to-Speech client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=input_text)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",#language_code="fil-PH",
        name="en-US-Neural2-G",#name="fil-PH-Wavenet-A",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Open a new stream to play the audio
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        output=True
    )

    # Play the audio by writing the raw data to the stream
    stream.write(response.audio_content)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()

    # Terminate PyAudio
    p.terminate()

if __name__ == '__main__':
    Speak("Initializing Face Recognition System! Hello Gianne P. Bacay, I am Haraya! How can I help you?")

#___________________pip install --upgrade google-cloud-texttospeech
#___________________python harayaVoiceEngine.py

