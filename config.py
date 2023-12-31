import json
from os.path import exists
import time
#import threading

#class task():
#    def __init__(self, f, *args, **kwargs) -> None:
#        nargs = (f,) + args
#        self.thread = threading.Thread(target=self._run, args=nargs, kwargs=kwargs)
#        self.value = None
#        self.finished = False
#    
#    def start(self):
#        self.thread.start()
#
#    def _run(self, f, *args, **kwargs):
#        self.value = f(*args, **kwargs)
#        self.finished = True
    

class Config():
    def __init__(self, fp: str = "config.json") -> None:
        if not exists(fp):
            with open(fp, 'w') as f:
                json.dump({
                    "change_language_pin": 38,
                    "listen_pin": 40,
                    "whisper_model": "tiny",
                    "whisper_exec": "whisper",
                    "languages": [
                        "en",
                        "de",
                        "es",
                        "fr"
                    ],
                    "font": "font",
                    "font_size": 16,
                    "line_wait_time": 10 # TODO; timings
                }, f)
        with open(fp) as f: data = json.load(f)
        self.CHANGE_LANGUGE_PIN: int = data["change_language_pin"]
        self.LISTEN_PIN: int = data["listen_pin"]
        self.WHISPER_MODEL: str = data["whisper_model"]
        self.WHISPER_EXEC: str = data["whisper_exec"]
        self.LANGUAGES: list[str] = data["languages"]
        self.FONT: str = data["font"]
        self.FONT_SIZE: int = data["font_size"]
        self.LINE_WAIT_TIME: int = data["line_wait_time"] 
        self.index = 0
        self.change_language_callback = lambda langcode: print(f"CONFIG: SET LANG {langcode}")
        self.listen_callback = lambda state: print(f"CONFIG: SET LISTEN {state}")
        self.listen_state = 1
        self.button_cooldown = 0
    
    def get_current_language_code(self) -> str: return self.LANGUAGES[self.index]
    
    def add_button_cooldown(self): self.button_cooldown = time.time() + 0.1

    def is_on_cooldown(self) -> bool: return time.time() < self.button_cooldown

    def set_index(self, index: int): 
        self.index = index
        self.change_language_callback(self.get_current_language_code())
        
    def set_index_by_language_code(self, code: str): 
        if code in self.LANGUAGES: self.index = self.LANGUAGES.index(code)
        self.change_language_callback(self.get_current_language_code())

    def increment_index(self):
        self.index += 1
        if self.index >= len(self.LANGUAGES): self.index = 0
        self.change_language_callback(self.get_current_language_code())
        
    def decrement_index(self):
        self.index -= 1
        if self.index <= -1: self.index = 0
        self.change_language_callback(self.get_current_language_code())
    
    def register_change_language_callback(self, f):
        self.change_language_callback = f
        return f
    
    def register_listen_callback(self, f):
        self.listen_callback = f
        return
    
    def increase_listen_state(self):
        self.listen_state += 1
        if self.listen_state == 3:
            self.listen_callback(self.listen_state)
        if self.listen_state == 4: self.listen_state = 0
