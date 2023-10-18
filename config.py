import json
import threading

class task():
    def __init__(self, f, *args, **kwargs) -> None:
        nargs = (f,) + args
        self.thread = threading.Thread(target=self._run, args=nargs, kwargs=kwargs)
        self.value = None
        self.finished = False
    
    def start(self):
        self.thread.start()

    def _run(self, f, *args, **kwargs):
        self.value = f(*args, **kwargs)
        self.finished = True
    

class Config():
    def __init__(self, fp: str = "config.json") -> None:
        with open(fp) as f: data = json.load(f)
        self.CHANGE_LANGUGE_PIN: int = data["change_language_pin"]
        self.LISTEN_PIN: int = data["listen_pin"]
        self.WHISPER_MODEL: str = data["whisper_model"]
        self.WHISPER_EXEC: str = data["whisper_exec"]
        self.LANGUAGES: list[str] = data["languages"] 
        self.index = 0
        self.change_language_callback = lambda langcode: print(f"CONFIG: SET {langcode}")
        self.listen_callback = lambda state: None
        self.listen_state = 1
    
    def get_current_language_code(self) -> str: return self.LANGUAGES[self.index]

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