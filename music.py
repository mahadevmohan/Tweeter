# music.py

import pygame
import threading

# Initialize Pygame mixer once at module load
pygame.mixer.init()

# Load points sound (preferably WAV for better compatibility)
points_sound_file = 'Assets/points.mp3'  # Ensure this file exists and is in WAV format
try:
    points_sound = pygame.mixer.Sound(points_sound_file)
except pygame.error as e:
    print(f"Unable to load points sound file: {e}")
    points_sound = None

def play_background_music(file_path):
    """
    Plays the background music on loop.
    """
    try:
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play(loops=-1)  # loops=-1 means infinite loop
        print(f"Playing background music: {file_path} on repeat.")
    except pygame.error as e:
        print(f"Unable to play the background music file: {e}")

def start_music(file_path):
    """
    Starts the background music playback in a separate daemon thread.
    """
    music_thread = threading.Thread(target=play_background_music, args=(file_path,), daemon=True)
    music_thread.start()

def play_points_sound():
    """
    Plays the points sound once.
    """
    if points_sound:
        points_sound.play()
        print("Playing points sound.")
    else:
        print("Points sound not available.")

def stop_points_sound():
    """
    Stops the points sound playback.
    """
    if points_sound:
        points_sound.stop()
        print("Stopped points sound.")
