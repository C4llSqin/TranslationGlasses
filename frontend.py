import backend
from config import Config
from display import make_oled
from luma.core.virtual import terminal
from PIL import ImageFont
import time
import RPi.GPIO as GPIO

config = Config()

GPIO.setmode(GPIO.BOARD)
get_state = lambda pin: not(GPIO.input(pin))

GPIO.setup(config.LISTEN_PIN, GPIO.IN, GPIO.PUD_DOWN)
GPIO.add_event_detect(config.LISTEN_PIN, GPIO.BOTH)
GPIO.setup(config.CHANGE_LANGUGE_PIN, GPIO.IN, GPIO.PUD_DOWN)
GPIO.add_event_detect(config.LISTEN_PIN, GPIO.BOTH)

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
    if get_state(pin) and config.listen_state != 3: 
        config.increment_index()
        print("Print: We set it to", config.get_current_language_code())

def make_font(fp: str, size: int):
    return ImageFont.truetype(fp, size)

def make_term() -> terminal:
    oled = make_oled()
    if oled is not None:
        return terminal(oled,
        font = make_font(config.FONT, config.FONT_SIZE),
        animate = False)
    else: raise Exception("Oh no!")

def reset_display(term: terminal):
    term.clear()
    term.puts(f"{backend.config.get_current_language_code():>term.width-2}")
    term.flush()

def dictate_and_translate(term: terminal):
    reset_display(term)
    term.println("Listening")
    term.flush()
    backend.speak_to_file(lambda: config.listen_state == 3)
    reset_display(term)
    term.println("Processing")
    term.flush()
    dictated_text = backend.file_to_string()
    text = backend.translate(dictated_text, config.get_current_language_code())
    return text

def display_lines(display: terminal, text: str, interupt_condition = lambda: False):
    len_chars_per_refresh = display.width * display.height-1
    i = 0
    while True:
        wait_time = time.time() + config.LINE_WAIT_TIME
        disp_text = text[(len_chars_per_refresh*i):(len_chars_per_refresh*(i+1))]
        reset_display(display)
        display.print(display)
        while time.time() <= wait_time:
            if disp_text == "" or interupt_condition(): return
            time.sleep(0.05)
        i += 1

def main():
    term = make_term()
    last_lang = config.get_current_language_code()
    while True:
        while config.listen_state != 3: 
            if last_lang != config.get_current_language_code():
                reset_display(term)
                last_lang = config.get_current_language_code()
            time.sleep(0.05)
        text = dictate_and_translate()
        display_lines(term, text, config.listen_state == 3)

if __name__ == "__main__": main()