from pocketsphinx import LiveSpeech
import translationAPI
import time

timeline = 5

def ask_to_translate():
    tstart = time.time()
    state = ""
    for phrase in LiveSpeech():
        state += f"{phrase} "
        if tstart + timeline < time.time(): break
    print(translationAPI.translate_to_dest(state))