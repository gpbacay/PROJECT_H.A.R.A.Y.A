import os
from google.cloud import texttospeech
import pyaudio
import wave

# Set your Google Cloud credentials as you did before
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"Resources\\nodal-skein-392905-babe98c4288f.json"

# Initialize the Text-to-Speech client
client = texttospeech.TextToSpeechClient()

def Speak(input_text: str):
    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=input_text)

    # Build the voice request, select the language code ("en-GB") and the ssml
    # voice gender ("neutral")
    #___________________python harayaVoiceEngine.py
    voice = texttospeech.VoiceSelectionParams(
        language_code="fil-PH", #fil-PH, en-AU, en-GB
        name="fil-PH-Neural2-A",#fil-PH-Neural2-A, en-AU-Polyglot-1, en-GB-Neural2-F(female),en-GB-News-K(male)
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, 
        voice=voice, 
        audio_config=audio_config
    )

    # Save the audio content as a temporary WAV file
    temp_wav = "temp.wav"
    with open(temp_wav, "wb") as wav_file:
        wav_file.write(response.audio_content)

    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Open the temporary WAV file
    wf = wave.open(temp_wav, 'rb')

    # Open a new stream to play the audio
    stream = p.open(
        format=p.get_format_from_width(wf.getsampwidth()),
        channels=wf.getnchannels(),
        rate=wf.getframerate(),
        output=True
    )

    # Play the audio by writing the raw data to the stream
    data = wf.readframes(1024)
    while data:
        stream.write(data)
        data = wf.readframes(1024)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()

    # Terminate PyAudio
    p.terminate()

    # Close the WAV file
    wf.close()

    # Delete the temporary WAV file
    os.remove(temp_wav)

if __name__ == '__main__':
    Speak("Mabuhay GDSC UIC! Maraming salamat sa opportunidad, Ako ay may lobo lumipad sa langit di ko na nakita pumutok na pala sayang ang pera ko pambili ng lobo sa pagkain sana nabusog pa ako.")

#___________________pip install --upgrade google-cloud-texttospeech
#___________________python harayaVoiceEngine.py

