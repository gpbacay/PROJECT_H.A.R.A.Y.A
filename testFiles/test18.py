from pydub import AudioSegment
from pydub.playback import play

# Load the audio file
audio = AudioSegment.from_file("sound.wav", format="wav")

# Increase the playback speed by 2x
faster_audio = audio.speedup(playback_speed=2)

# Play the faster audio
play(faster_audio)


#_____________test18.py