from __future__ import print_function  # Not needed in Python 3
import sys, tty, termios
import os
import terminal

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
    selected = 0
    key_pressed = None

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

    def _get_input(self):
        while (1):
            k = self._getch()
            if k != "":
                break
        keycodes = {'\x1b[A': "prev", '\x1b[B': "next", '\x1b[C': "next", '\x1b[D': "prev", "\n": "select"}
        if k in keycodes.keys():
            return keycodes[k]
        return None

    def __call__(self):
        self.selected = 0
        terminal.hide_cursor()
        while True:
            self._render_menu()
            self.key_pressed = None
            while self.key_pressed is None:
                self.key_pressed = self._get_input()
                if (self.key_pressed == "next") and self.selected < (len(self.opts) - 1):
                    self.selected += 1
                elif (self.key_pressed == "prev") and self.selected > 0:
                    self.selected -= 1
                elif self.key_pressed == "select":
                    print("")
                    return self.selected

    def _render_menu(self):
        terminal.clear()
        print("\r", end="")
        print(self.message)
        for ind, opt in enumerate(self.opts):
            if ind == self.selected:
                print(bcolors.FAIL + " >>  " + bcolors.ENDC, end="")
                print("\033[0;30;107m{}\033[0m".format(opt), end=" ")
            else:
                print("     ", end="")
                print(opt, end=" ")
            print("")

    def set_data(self, data):
        self.opts = data
        self._render_menu()
