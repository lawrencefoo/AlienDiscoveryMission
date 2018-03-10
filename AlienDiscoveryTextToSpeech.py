from gtts import gTTS
import os
import subprocess
import time

tts = gTTS(text='Greetings From Earth', lang='en')
tts.save("greetings.mp3")
for i in range(1,4):
    subprocess.call(["C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe","--play-and-exit","C:\\Users\\fool\\Documents\\Work\\Technical\\EMC\\Trainings\\Piped_Piper\\Project\\greetings.mp3"])
    time.sleep(1)
