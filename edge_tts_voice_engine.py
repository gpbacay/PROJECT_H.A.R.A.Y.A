import asyncio
import edge_tts
import io
from pydub import AudioSegment
import pyaudio

async def speak_text(text: str, voice: str, rate: str = "+0%"):
    # Create a Communicate object with the given text, voice, and rate.
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    
    # Use the stream() method to get audio chunks asynchronously.
    result = [chunk async for chunk in communicate.stream()]
    
    # Combine all audio_data chunks (MP3 bytes) into one bytes object.
    # If a chunk does not have "audio_data", it returns an empty byte string.
    audio_bytes = b"".join(chunk.get("audio_data", b"") for chunk in result)
    
    # Load the MP3 data from memory using pydub.
    audio_file = io.BytesIO(audio_bytes)
    audio_segment = AudioSegment.from_file(audio_file, format="mp3")
    
    # Extract raw PCM data and audio parameters.
    raw_data = audio_segment.raw_data
    sample_rate = audio_segment.frame_rate
    channels = audio_segment.channels
    sample_width = audio_segment.sample_width

    # Initialize PyAudio and open a stream.
    p = pyaudio.PyAudio()
    stream = p.open(
        format=p.get_format_from_width(sample_width),
        channels=channels,
        rate=sample_rate,
        output=True
    )

    # Write the raw PCM data to the audio stream in chunks.
    chunk_size = 1024
    for i in range(0, len(raw_data), chunk_size):
        stream.write(raw_data[i:i+chunk_size])

    # Clean up: close the stream and terminate PyAudio.
    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__ == "__main__":
    text = "Hi Sir Gianne Bacay! I am Haraya! How can I help you?"
    voice = "en-GB-LibbyNeural"  # Change to any supported voice if desired.
    asyncio.run(speak_text(text, voice))



# python edge_tts_voice_engine.py
