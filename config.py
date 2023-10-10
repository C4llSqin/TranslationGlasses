import json
import threading

def run_in_new_thread(f, *args, **kwargs):
    thread = threading.Thread(target=f, args=args, kwargs=kwargs, daemon=True)
    thread.start()
    return thread

class Config():
    def __init__(self, fp: str = "config.json") -> None:
        with open(fp) as f: data = json.load(f)
        self.CHANGE_LANGUGE_PIN: int = data["change_language_pin"]
        self.LISTEN_PIN: int = data["listen_pin"]
        self.WHISPER_MODEL: str = data["whisper_model"]
        self.WHISPER_EXEC: str = data["whisper_exec"]
        self.LANGUAGES: list[str] = data["languages"] 
        self.index = 0
        self.change_language_callback = lambda langcode: print(f"CONFING: SET {langcode}")
        self.listen_callback = lambda state: None

    def changes_language(self, f):
        def wrap(*args, **kwargs):
            ret = f(*args, **kwargs)
            self.change_language_callback(self.get_current_language_code())
            # run_in_new_thread(self.change_language_callback(), self.get_current_language_code())
            return ret
        return wrap

    def get_current_language_code(self) -> str: return self.LANGUAGES[self.index]

    @changes_language
    def set_index(self, index: int): self.index = index

    @changes_language
    def set_index_by_language_code(self, code: str): 
        if code in self.LANGUAGES: self.index = self.LANGUAGES.index(code)

    @changes_language
    def increment_index(self):
        self.index += 1
        if self.index >= len(self.LANGUAGES): self.index = 0
    
    @changes_language
    def decrement_index(self):
        self.index -= 1
        if self.index <= -1: self.index = 0
    
    def register_change_language_callback(self, f):
        self.change_language_callback = f
        return f
    
    def register_listen_callback(self, f):
        self.listen_callback = f
        return