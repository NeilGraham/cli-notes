# ------------------------------- #

import time

def get_input(win):
    key = ''
    while True:
        time.sleep(.01)
        try:
            key = win.getkey()
            if key == os.linesep:
                break
        except Exception as e:
            pass
        if key != '':
            return key
