import pyaudio
from pocketsphinx import AudioFile

FORMAT = pyaudio.paInt16

CHANNELS = 1
RATE = 16000
CHUNK = int(RATE / 10)

def speak_to_bytes(callable, verbose: bool = False):
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
    
    stream.stop_stream()
    stream.close()
    audio.terminate()

    f = open("DictationAudioFile.raw", 'wb')
    f.write(b''.join(frames))
    f.close()
    return

if __name__ == "__main__":
    speak_to_bytes(lambda: True, True)
    for phrase in AudioFile("DictationAudioFile.raw"): print(phrase)

