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
GPIO.add_event_detect(config.CHANGE_LANGUGE_PIN, GPIO.BOTH)

def register_GPIO_callback(pin: int):
    def wrap(function):
        GPIO.add_event_callback(pin, function)
        return function
    return wrap

@register_GPIO_callback(config.LISTEN_PIN)
def listen(pin: int):
    if not config.is_on_cooldown():
        config.add_button_cooldown()
        config.increase_listen_state()
        print("Print: We Set listen state to ", config.listen_state)

@register_GPIO_callback(config.CHANGE_LANGUGE_PIN)
def change_langauge(pin: int):
    if all([get_state(pin), config.listen_state != 3, not (config.is_on_cooldown())]):
        config.add_button_cooldown()
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
    lang, size = config.get_current_language_code(), term.width-1
    term.puts((" " * size) + lang)
    term.flush()

def dictate_and_translate(term: terminal):
    reset_display(term)
    term.println("Listening")
    term.flush()
    backend.speak_to_file(lambda: config.listen_state == 3)
    reset_display(term)
    term.println("Processing")
    term.flush()
    dictated_text = backend.file_to_string(config.WHISPER_MODEL, config.WHISPER_EXEC, config.get_current_language_code())
    try: text = backend.translate(dictated_text, config.get_current_language_code())
    except: text = "<TRANSLATION ERROR>"
    return text

def display_lines(display: terminal, text: str, interupt_condition = lambda: False):
    len_chars_per_line = display.width - 1
    n_lines = display.height - 1
    len_chars_per_refresh = len_chars_per_line * n_lines
    i = 0
    while True:
        wait_time = time.time() + config.LINE_WAIT_TIME
        reset_display(display)
        for j in range(n_lines):
            disp_text = text[(len_chars_per_refresh*i) + (len_chars_per_line * j):(len_chars_per_refresh*i) + (len_chars_per_line* (j+1)) ]
            display.println(disp_text)
       
        while time.time() <= wait_time:
            if text[(len_chars_per_refresh*i):(len_chars_per_refresh*(i+1))] == "" or interupt_condition():
                reset_display(display)
                return
            time.sleep(0.05)
        i += 1

def main():
    term = make_term()
    last_lang = config.get_current_language_code()
    reset_display(term)
    display_lines(term, backend.get_ip(), lambda: config.listen_state == 3)
    while True:
        while config.listen_state != 3: 
            if last_lang != config.get_current_language_code():
                reset_display(term)
                last_lang = config.get_current_language_code()
            time.sleep(0.05)
        text = dictate_and_translate(term)
        display_lines(term, text, lambda: config.listen_state == 3)

if __name__ == "__main__": main()
