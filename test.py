import pyaudio
import time
import datetime
import threading
import wave
import pyttsx3
import re

if __name__ == "__main__":
    rate=input()
    file=open("config.txt","w")
    file.write("rate:"+rate)