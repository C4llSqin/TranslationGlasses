from luma.core import cmdline

def make_oled():
    parser = cmdline.create_parser(description='make_oled arguments')
    args = parser.parse_args(None)
    try: return cmdline.create_device(args)
    except: return None