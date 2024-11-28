# main.py

import threading
import sys
from gui import start_gui
from music import start_music

def main():
    """
    Starts the music and GUI.
    """
    
    audio_file = 'Assets/POL-jazzy-duck-short.wav'  
    
    
    start_music(audio_file)
    
  
    start_gui()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
