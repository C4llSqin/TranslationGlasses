import subprocess
import pyaudio
import wave
import re
from config import Config
import translationAPI as tapi

config = Config()

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = int(RATE / 10)

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


def file_to_string(fp: str = "DictationAudioFile.wav"):
    p = subprocess.Popen([config.WHISPER_EXEC, "-m", f"home/translationglasses/whisper.cpp/models/ggml-{config.WHISPER_MODEL}.bin", "-l", config.get_current_language_code(), fp], stdout=subprocess.PIPE)
    p.wait() # wait for it to finish
    data = p.communicate()[0].decode()
    lines = data.split("\n")
    text = ""
    for line in lines:
        regex = re.match(r"\[..:..:..\.... --> ..:..:..\....]   ", line)
        if regex is not None: text += line[33:]
    return text

if __name__ == "__main__":
    speak_to_file(lambda: True)
    text = file_to_string()
    neotext = tapi.translate(text, config.get_current_language_code())

