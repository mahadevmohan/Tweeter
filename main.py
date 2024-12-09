# main.py

import sys
from gui import start_gui
from music import start_music
import pygame

def main():
    """
    Starts the music and GUI.
    """
    audio_file = 'Assets/POL-jazzy-duck-short.wav'  # Ensure this file exists
    start_music(audio_file)
    start_gui()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        sys.exit(0)
