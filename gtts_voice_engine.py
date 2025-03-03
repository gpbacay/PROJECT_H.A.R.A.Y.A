"""
haraya_tts.py
A simple module for speaking text using gTTS, BytesIO, and pygame.
"""

from gtts import gTTS
from io import BytesIO
import pygame

def speak(text, lang='en', slow=False):
    """
    Speaks the given text using gTTS, BytesIO, and pygame.

    Parameters:
        text (str): The text to be spoken.
        lang (str): The language code for the text (e.g., 'en' for English,
                    'fr' for French). gTTS only allows you to choose the language.
        slow (bool): Whether to speak slowly. Defaults to False.
    
    Note:
        gTTS does not support selecting different voices beyond the default
        one provided for the language.
    """
    # Create a gTTS object.
    tts = gTTS(text=text, lang=lang, slow=slow)
    
    # Save speech to an in-memory bytes buffer.
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    
    # Initialize pygame mixer.
    pygame.mixer.init()
    
    # Load the audio from the buffer and play it.
    pygame.mixer.music.load(fp)
    pygame.mixer.music.play()
    
    # Wait for the audio to finish playing.
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(0)

if __name__ == '__main__':
    # Example usage:
    speak("Hello Gianne Bacay, this is Google Text to Speech speaking directly without saving a file. Mabuhay!")




# python gtts_voice_engine.py
