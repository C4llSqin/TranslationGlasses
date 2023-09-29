import pyaudio
import wave
import subprocess
import re

FORMAT = pyaudio.paInt16

CHANNELS = 1
RATE = 16000
CHUNK = int(RATE / 10)

def speak_to_bytes(callable, fp: str = "DictationAudioFile.wav", verbose: bool = False):
    if verbose:
        print("Init Speaking")

    audio = pyaudio.PyAudio()

    stream = audio.open(format=FORMAT, channels=CHANNELS,
            rate=RATE, input=True,
            frames_per_buffer=CHUNK)
    print("recording...")
    frames = []

    try:
        while callable():
            data = stream.read(CHUNK)
            frames.append(data)
    except: pass
    print("Stoping...")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    f = wave.open(fp, 'wb')
    f.setparams((CHANNELS, 2, RATE, len(frames), "NONE", 'not compressed'))
    f.writeframesraw(b''.join(frames))
    f.close()
    return

def file_to_string(fp: str = "DictationAudioFile.wav", lang: str = "en", model: str = "ggml-base.bin"):
    p = subprocess.Popen(["Whisper", "-m", f"~/whisper.cpp/models/{model}", "-l", lang, fp])
    p.wait()
    data = p.communicate()[0].decode
    lines = data.split("\n")
    text = ""
    for line in lines:
        regex = re.match(line, r"\[..:..:..\.... --> ..:..:..\....]   ")
        if regex is not None: text += line[36:]
    return text

if __name__ == "__main__":
    speak_to_bytes(lambda: True, verbose=True)
    print(f"Got: {file_to_string()}")
