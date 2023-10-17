import translationAPI as tapi
import dictateToFile as dtf
from config import Config, task
import time
import RPi.GPIO as GPIO
import subprocess
import re

config = Config()

GPIO.setmode(GPIO.BOARD)

GPIO.setup(config.LISTEN_PIN, GPIO.IN, GPIO.PUD_DOWN)
GPIO.add_event_detect(config.LISTEN_PIN, GPIO.BOTH)
GPIO.setup(config.CHANGE_LANGUGE_PIN, GPIO.IN, GPIO.PUD_DOWN)
GPIO.add_event_detect(config.LISTEN_PIN, GPIO.BOTH)

get_state = lambda pin: not(GPIO.input(pin))
current_task = None

def register_GPIO_callback(pin: int):
    def wrap(function):
        GPIO.add_event_callback(pin, function)
        return function
    return wrap

@register_GPIO_callback(config.LISTEN_PIN)
def listen(pin: int):
    config.increase_listen_state()

@register_GPIO_callback(config.CHANGE_LANGUGE_PIN)
def change_langauge(pin: int):
    if get_state(pin): 
        config.increment_index()
        print("Print: We set it to", config.get_current_language_code())

def file_to_string(fp: str = "DictationAudioFile.wav"):
    p = subprocess.Popen([config.WHISPER_EXEC, "-m", f"/home/translationglasses/whisper.cpp/models/ggml-{config.WHISPER_MODEL}.bin", "-l", config.get_current_language_code(), fp], stdout=subprocess.PIPE)
    p.wait() # wait for it to finish
    data = p.communicate()[0].decode()
    lines = data.split("\n")
    text = ""
    for line in lines:
        regex = re.match(r"\[..:..:..\.... --> ..:..:..\....]   ", line)
        if regex is not None: text += line[34:]
    return text

def dictate_and_translate():
    dtf.speak_to_file(lambda: config.listen_state == 3)
    untranslated_text = file_to_string()
    translated_text = tapi.translate(untranslated_text, source=config.get_current_language_code())
    return translated_text

def run_dictate_task():
    global current_task
    current_task = task(dictate_and_translate)
    current_task.start()

config.register_listen_callback(listen_task)
if __name__ == "__main__":
    while True: time.sleep(1)