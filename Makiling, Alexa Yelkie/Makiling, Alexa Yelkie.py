# main.py

import sounddevice as sd
import numpy as np
import speech_recognition as sr
import pyttsx3
import pygame
import os
import random


recognizer = sr.Recognizer()
engine = pyttsx3.init()
pygame.mixer.init()


MUSIC_FOLDER = "C:/Users/Admin/Desktop/Alexa Yelkie/Makiling, Alexa Yelkie"


current_song = None
paused = False


def speak(text):
    """Convert text to speech"""
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def listen(duration=5, fs=16000):
    
    print("\n🎤 Listening...")
    try:
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()
        audio_data = sr.AudioData(recording.tobytes(), fs, 2)
        command = recognizer.recognize_google(audio_data)
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        print("⚠️ Sorry, I didn't understand that.")
        return ""
    except sr.RequestError:
        print("⚠️ Could not connect to Google Speech Recognition.")
        return ""

def play_song(filename):
  
    global current_song, paused
    try:
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        current_song = filename
        paused = False
        print(f"🎶 Now playing: {os.path.basename(filename)}")
        speak(f"Now playing {os.path.basename(filename)}")
    except Exception as e:
        print(f"Error playing song: {e}")

def pause_song():
    global paused
    if pygame.mixer.music.get_busy() and not paused:
        pygame.mixer.music.pause()
        paused = True
        print("⏸ Music paused.")
        speak("Music paused.")

def resume_song():
    global paused
    if paused:
        pygame.mixer.music.unpause()
        paused = False
        print("▶️ Music resumed.")
        speak("Music resumed.")

def next_song():
   
    mp3_files = [f for f in os.listdir(MUSIC_FOLDER) if f.lower().endswith(".mp3")]
    if mp3_files:
        song_file = os.path.join(MUSIC_FOLDER, random.choice(mp3_files))
        play_song(song_file)
    else:
        speak("No songs found.")

def find_song(command):
   
    for file in os.listdir(MUSIC_FOLDER):
        if file.lower().endswith(".mp3") and all(word in file.lower() for word in command.split()):
            return os.path.join(MUSIC_FOLDER, file)
    return None

def local_response(command):
   
    if "hello" in command:
        return "Hello! How are you today?"
    elif "your name" in command:
        return "I am Alexa, your voice assistant."

   
    elif "play" in command:
        song_file = find_song(command)
        if song_file:
            play_song(song_file)
        else:
            speak("I could not find that song. Playing a random one.")
            next_song()
        return None
    elif "pause" in command:
        pause_song()
        return None
    elif "resume" in command:
        resume_song()
        return None
    elif "next" in command:
        next_song()
        return None
    elif any(word in command for word in ["bye", "exit", "quit", "stop"]):
        speak("Goodbye! Have a great day.")
        exit()

 
    else:
        responses = [
            "That's interesting! Tell me more.",
            "Hmm, I see. What else would you like to talk about?",
            "I'm always here to listen!"
        ]
        return random.choice(responses)


def main():
  
    mp3_files = [f for f in os.listdir(MUSIC_FOLDER) if f.lower().endswith(".mp3")]
    if not mp3_files:
        speak("Warning: No MP3 files found in your music folder.")
    else:
        print(f"Found {len(mp3_files)} songs in {MUSIC_FOLDER}")

    speak("Hello! I am your chatbot voice assistant. How can I help you?")
    while True:
        user_command = listen()
        if not user_command:
            continue
        reply = local_response(user_command)
        if reply:
            speak(reply)

if __name__ == "__main__":
    main()
