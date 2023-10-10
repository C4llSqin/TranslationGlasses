import translationAPI as tapi
import dictateToFile as dtf
from config import Config

import RPi.GPIO as GPIO
import subprocess
import re

config = Config()

GPIO.setmode(GPIO.BOARD)

GPIO.setup(config.LISTEN_PIN, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(config.CHANGE_LANGUGE_PIN, GPIO.IN, GPIO.PUD_DOWN)

get_state = lambda pin: not(GPIO.input(pin))
is_listening = False

def register_GPIO_callback(pin: int):
    def wrap(function):
        GPIO.add_event_callback(pin, function)
        return function
    return wrap

@register_GPIO_callback(config.LISTEN_PIN)
def listen(pin: int):
    global is_listening

@register_GPIO_callback(config.CHANGE_LANGUGE_PIN)
def change_langauge(pin: int):
    if get_state(pin): 
        config.increment_index()
        print("Print: We set it to", config.get_current_language_code())

def file_to_string(fp: str = "DictationAudioFile.wav"):
    p = subprocess.Popen([config.WHISPER_EXEC, "-m", f"../whisper.cpp/models/ggml-{config.WHISPER_MODEL}.bin", "-l", config.get_current_language_code(), fp], stdout=subprocess.PIPE)
    p.wait() # wait for it to finish
    data = p.communicate()[0].decode()
    lines = data.split("\n")
    text = ""
    for line in lines:
        regex = re.match(r"\[..:..:..\.... --> ..:..:..\....]   ", line)
        if regex is not None: text += line[33:]
    return text