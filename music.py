# music.py

import pygame
import sys
import threading
import time

def play_audio_on_repeat(file_path):
    """
    Initializes the Pygame mixer and plays the specified audio file on repeat.
    """
    try:
       
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play(loops=-1)
        print(f"Playing audio: {file_path} on repeat.")
        
        while pygame.mixer.music.get_busy():
            time.sleep(1)
            
    except pygame.error as e:
        print(f"Unable to play the audio file: {e}")
        return

def start_music(file_path):
    """
    Starts the music playback in a separate daemon thread.
    """
    music_thread = threading.Thread(target=play_audio_on_repeat, args=(file_path,), daemon=True)
    music_thread.start()
