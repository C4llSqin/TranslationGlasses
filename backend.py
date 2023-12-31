### Translation
import googletrans

### Dictation
import pyaudio
import wave
import subprocess
import re

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = int(RATE / 10)

#GPIO.setmode(GPIO.BOARD)

#GPIO.setup(config.LISTEN_PIN, GPIO.IN, GPIO.PUD_DOWN)
#GPIO.add_event_detect(config.LISTEN_PIN, GPIO.BOTH)
#GPIO.setup(config.CHANGE_LANGUGE_PIN, GPIO.IN, GPIO.PUD_DOWN)
#GPIO.add_event_detect(config.LISTEN_PIN, GPIO.BOTH)

#get_state = lambda pin: not(GPIO.input(pin))
#current_task = None

#def register_GPIO_callback(pin: int):
#    def wrap(function):
#        GPIO.add_event_callback(pin, function)
#        return function
#    return wrap
#
#@register_GPIO_callback(config.LISTEN_PIN)
#def listen(pin: int):
#    config.increase_listen_state()
#
#@register_GPIO_callback(config.CHANGE_LANGUGE_PIN)
#def change_langauge(pin: int):
#    if get_state(pin): 
#        config.increment_index()
#        print("Print: We set it to", config.get_current_language_code())

def speak_to_file(callable, fp: str = "DictationAudioFile.wav"):
    audio = pyaudio.PyAudio()

    stream = audio.open(format=FORMAT, channels=CHANNELS,
            rate=RATE, input=True,
            frames_per_buffer=CHUNK)
    frames = []

    try:
        while callable():
            data = stream.read(CHUNK)
            frames.append(data)
    except: pass
    
    stream.stop_stream()
    stream.close()
    audio.terminate()

    f = wave.open(fp, 'wb')
    f.setparams((CHANNELS, 2, RATE, len(frames), "NONE", 'not compressed'))
    f.writeframesraw(b''.join(frames))
    f.close()
    return

def file_to_string(model: str, exec_fp: str, lang: str, fp: str = "DictationAudioFile.wav"):
    p = subprocess.Popen([exec_fp, "-m", f"/home/translationglasses/whisper.cpp/models/ggml-{model}.bin", "-l", lang, fp], stdout=subprocess.PIPE)
    p.wait() # wait for it to finish
    data = p.communicate()[0].decode()
    lines = data.split("\n")
    text = ""
    for line in lines:
        regex = re.match(r"\[..:..:..\.... --> ..:..:..\....]   ", line)
        if regex is not None: text += line[34:]
    return text

def translate(q: str, source: str = "auto", destination: str = "en") -> dict[str, str]:
    translator = googletrans.Translator()
    return translator.translate(q, destination, source).text

def get_ip() -> str:
    term_out = subprocess.check_output(["ifconfig"]).decode()
    wlan_section = term_out[term_out.find("wlan0:"):]
    ip_section = wlan_section[wlan_section.find("inet "):]
    address = ip_section[5:ip_section[5:].find(" ")+5]
    return address

#def dictate_and_translate():
#    dtf.speak_to_file(lambda: config.listen_state == 3)
#    untranslated_text = file_to_string()
#    translated_text = tapi.translate(untranslated_text, source=config.get_current_language_code())
#    return translated_text

# def run_dictate_task():
#     ...

# config.register_listen_callback(run_dictate_task)
# if __name__ == "__main__":
#     while True: time.sleep(1)
