import math
import sys, tty, termios
import os

if os.name == 'nt':
    import msvcrt
    import ctypes


    class _CursorInfo(ctypes.Structure):
        _fields_ = [("size", ctypes.c_int),
                    ("visible", ctypes.c_byte)]


class TicTacToe:
    board = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
    width = 2
    currentPlayer = 0
    players = ['X', 'O']
    selected = 3
    message = ""

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
        while (1):
            k = self._getch()
            if k != "":
                break
        keycodes = {'\x1b[A': "up", '\x1b[B': "down", '\x1b[C': "right", '\x1b[D': "left", "\n": "select"}
        if k in keycodes.keys():
            return keycodes[k]
        return None

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

    def print_board(self):
        self._clear()
        print("    Tic Tac Toe")
        print("")
        print("   -------------")
        print("   |", self._print_field(0), "|", self._print_field(1), "|", self._print_field(2), "|")
        print("   -------------")
        print("   |", self._print_field(3), "|", self._print_field(4), "|", self._print_field(5), "|")
        print("   -------------")
        print("   |", self._print_field(6), "|", self._print_field(7), "|", self._print_field(8), "|")
        print("   -------------")
        print(f"   Player: {self.players[self.currentPlayer]}")
        print(f"{self.message}")

    def _print_field(self, index):
        if index == self.selected:
            return f"\033[0;30;107m{self.board[index]}\033[0m"
        else:
            return self.board[index]

    def _check_victory(self):
        player = self.players[self.currentPlayer]

        if self.board[0] == player:
            if (self.board[1] == player and self.board[2] == player) or (self.board[3] == player and self.board[6] == player) or (self.board[4] == player and self.board[8] == player):
                return True
        if self.board[4] == player:
            if (self.board[1] == player and self.board[7] == player) or (self.board[3] == player and self.board[5] == player) or (self.board[2] == player and self.board[6] == player):
                return True
        if self.board[8] == player:
            if (self.board[6] == player and self.board[7] == player) or (self.board[2] == player and self.board[5] == player):
                return True

        return False




    def _turn(self):
        if self.board[self.selected] == ' ':
            self.board[self.selected] = self.players[self.currentPlayer]
            return True
        else:
            return False

    def victory(self):
        print("Victory")
        self.board = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        self.currentPlayer = 0

    def start(self):
        while True:
            self.print_board()
            key_pressed = None
            while key_pressed is None:
                key_pressed = self._get_input()
                if (key_pressed == "left") and (self.selected % 3) > 0:
                    self.selected -= 1
                elif (key_pressed == "right") and (self.selected % 3) < 2:
                    self.selected += 1
                elif (key_pressed == "up") and math.floor(self.selected / 3) > 0:
                    self.selected -= 3
                elif (key_pressed == "down") and math.floor(self.selected / 3) < 2:
                    self.selected += 3
                elif key_pressed == "select":
                    if self._turn():
                        if self._check_victory():
                            self.victory()
                            return self.players[self.currentPlayer]
                        if any(x == ' ' for x in self.board):
                            self.currentPlayer = (self.currentPlayer + 1) % 2
                        else:
                            self.victory()
                            return 0


if __name__ == '__main__':
    toe = TicTacToe()

    toe.start()
