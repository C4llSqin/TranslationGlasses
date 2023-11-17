import backend
from display import make_oled
from luma.core.virtual import terminal
from PIL import ImageFont
from time import sleep

def make_font(fp: str, size: int):
    return ImageFont.truetype(fp, size)

def make_term() -> terminal:
    oled = make_oled()
    if oled is not None:
        return terminal(oled,
        animate=False)
    else: raise Exception("Oh no!")

def reset_display(term: terminal):
    term.clear()
    term.puts(f"{backend.config.get_current_language_code():>term.width-2}")
    term.flush()

def dictate_and_translate(term: terminal):
    # todo: conditonal to prevent lang switching while translating
    reset_display(term)
    term.println("Listening")
    term.flush()
    text = backend.dictate_and_translate()
    reset_display(term)
    term.println(text)

def main():
    term = make_term()
    reset_display(term)
    sleep(3)
    dictate_and_translate(term)
    sleep(15)

if __name__ == "__main__": main()