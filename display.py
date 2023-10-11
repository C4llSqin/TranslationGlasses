from luma.core import cmdline

def make_oled():
    try: return cmdline.create_device()
    except: return None