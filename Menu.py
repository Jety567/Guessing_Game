from __future__ import print_function # Not needed in Python 3
import sys, tty, termios
import os

if os.name == 'nt':
    import msvcrt
    import ctypes
    class _CursorInfo(ctypes.Structure):
        _fields_ = [("size", ctypes.c_int),
                    ("visible", ctypes.c_byte)]
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Menu:
    opts = []
    message = ""

    def __init__(self, options, message=None):
        self.opts = options
        if not message == None:
            self.message = message

    def _getch(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setcbreak(sys.stdin.fileno())
            ch = ""
            for _ in range(3):
                ch += sys.stdin.read(1)
                if not ch.startswith('\x1b'):
                    break
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    def _clear(self):
        if (os.name == 'posix'):
            os.system('clear')
        else:
            os.system('cls')

    def _hide_cursor(self):
        if os.name == 'nt':
            ci = _CursorInfo()
            handle = ctypes.windll.kernel32.GetStdHandle(-11)
            ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
            ci.visible = False
            ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
        elif os.name == 'posix':
            sys.stdout.write("\033[?25l")
            sys.stdout.flush()

    def _get_input(self):
        while(1):
            k = self._getch()
            if k!="":
                break
        keycodes = {'\x1b[A': "prev", '\x1b[B': "next", '\x1b[C': "next", '\x1b[D': "prev", "\n": "select"}
        if k in keycodes.keys():
            return keycodes[k]
        return None

    def __call__(self):
        selected = 0
        self._hide_cursor()
        while True:
            # Infinite loop broken by return
            self._clear()
            print("\r", end="")
            print(f"{f'{self.message}':^30s}")
            print(f"{'-':-^30s}")
            for ind, opt in enumerate(self.opts):
                if ind == selected:
                    print(bcolors.FAIL + "> " + bcolors.ENDC,end="")
                    print("\033[0;30;107m{}\033[0m".format(opt), end=" ")
                else:
                    print("  ", end="")
                    print(opt, end=" ")
                print("")

            key_pressed = None
            while key_pressed == None:
                # Looping until valid key pressed
                key_pressed = self._get_input()
                if (key_pressed == "next") and selected < (len(self.opts) - 1):
                    selected += 1
                elif (key_pressed == "prev") and selected > 0:
                    selected -= 1
                elif key_pressed == "select":
                    print("")
                    return self.opts[selected]


if __name__ == '__main__':
    exit_menu = Menu(['Yes', 'No'], "Exit?")
    if exit_menu() == 'Yes':
        sys.exit()