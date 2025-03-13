from playsound import playsound

class SoundSystem:
    """
    A simple sound system to play various audio cues.
    """

    def playStartUpSound(self) -> None:
        """
        Plays the startup sound.
        """
        mp3_path = u"audioFiles\\startup2.mp3"
        playsound(mp3_path)

    def playPromptSound(self) -> None:
        """
        Plays the prompt sound.
        """
        mp3_path = u"audioFiles\\prompt1.mp3"
        playsound(mp3_path)

    def playListeningSound(self) -> None:
        """
        Plays the listening sound.
        """
        mp3_path = u"audioFiles\\listening2.mp3"
        playsound(mp3_path)

    def playShutdownSound(self) -> None:
        """
        Plays the shutdown sound.
        """
        mp3_path = u"audioFiles\\shutdown.mp3"
        playsound(mp3_path)

    def playSearchSound(self) -> None:
        """
        Plays the search sound.
        """
        mp3_path = u"audioFiles\\searching.mp3"
        playsound(mp3_path)

    def playErrorSound(self) -> None:
        """
        Plays the error sound.
        """
        mp3_path = u"audioFiles\\error.mp3"
        playsound(mp3_path)

    # New methods for the loading bar
    def playLoadingBarSound(self) -> None:
        """
        Plays the loading bar sound.
        """
        mp3_path = u"audioFiles\\loadingbar2.mp3"
        playsound(mp3_path)

    def playLoadCompleteSound(self) -> None:
        """
        Plays the sound indicating loading is complete.
        """
        mp3_path = u"audioFiles\\loadcomplete.mp3"
        playsound(mp3_path)


if __name__ == "__main__":
    # Test the SoundSystem class.
    sound_system = SoundSystem()
    print("Playing startup sound...")
    sound_system.playStartUpSound()


# Run Command: python sound_system.py