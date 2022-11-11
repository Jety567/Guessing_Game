import random
from simple_term_menu import TerminalMenu
import os
import sys
import re

if os.name == 'nt':
    import msvcrt
    import ctypes
    class _CursorInfo(ctypes.Structure):
        _fields_ = [("size", ctypes.c_int),
                    ("visible", ctypes.c_byte)]

name = ""
highscore = {}
keys_dict = {}

# EXIT_CODES
EXIT_CODE_NONE = 0
EXIT_CODE_USER_INTERRUPTION = 1

def hide_cursor():
    if os.name == 'nt':
        ci = _CursorInfo()
        handle = ctypes.windll.kernel32.GetStdHandle(-11)
        ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
        ci.visible = False
        ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
    elif os.name == 'posix':
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()

def show_cursor():
    if os.name == 'nt':
        ci = _CursorInfo()
        handle = ctypes.windll.kernel32.GetStdHandle(-11)
        ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
        ci.visible = True
        ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
    elif os.name == 'posix':
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()


def print_game_title(error = ""):
    clear()
    print("          Guessing Game!         ")
    print("---------------------------------")
    if not error == "":
        print(error)
        print("")
    print("Guess a number between 1 and 10: ")

def guess():
    # todo Schwierigkeiten Low,Medium,High

    x = random.uniform(1, 10)
    x = round(x)
    guess = 12

    score = 10

    print_game_title()

    while guess != x:
        guess = input()
        if guess == 'End':
            print("Bye!")
            break
        try:
            guess = int(guess)
        except:
            print_game_title("Please type in a number!")
            continue

        if (guess < 1 or guess > 10):
            print_game_title("Number out of Range!")
            continue

        if guess < x:
            print_game_title("Higher")
        elif guess > x:
            print_game_title("Lower")
        else:
            clear()
            print("          Guessing Game!         ")
            print("---------------------------------")
            print("Correct!", name, "Your Score is", score, "!")
            print("")
            write_score(score, name)
            terminal_menu = TerminalMenu(["New Game", "Back", "Exit"], accept_keys=("enter", "alt-d", "ctrl-i"))
            menu_entry_index = terminal_menu.show()
            if terminal_menu.chosen_menu_index == 0:
                x = random.uniform(0, 10)
                x = round(x)
                guess = 12
                score = 10
                print_game_title()
                continue
            elif terminal_menu.chosen_menu_index == 1:
                show_main_menu()
            elif terminal_menu.chosen_menu_index == 1:
                exit_game(EXIT_CODE_NONE)
        score = score - 1

def exit_game(exit_code):
    clear()
    show_cursor()
    clear()
    os._exit(exit_code)

def clear():
    if (os.name == 'posix'):
        os.system('clear')
    # else screen will be cleared for windows
    else:
        os.system('cls')

def write_score(score, name):
    f = open("score.txt", "a")
    f.write(name)
    f.write("//")
    f.write(str(score))
    f.writelines('\n')
    f.close()

def print_highscore():
    global highscore
    clear()
    print("\t   Highscore!           ")
    print("------------------------------")
    for x in highscore:
        print("   ", str(x[0]).ljust(10), "| ", str(x[1]).rjust(2))
    print("------------------------------")
    print("")
    
    terminal_menu = TerminalMenu(["Back", "Exit"], accept_keys=("enter", "alt-d", "ctrl-i"))
    menu_entry_index = terminal_menu.show()
    key_enter_high_score(terminal_menu.chosen_menu_index)

def show_highscore():
    f = open("score.txt", "r")
    array = f.read().split("\n")
    global highscore
    highscore = {}
    for score in array:
        if score == '':
            continue
        highscore[score.split('//')[0]] = score.split('//')[1]
    highscore = sorted(highscore.items(), key=lambda highscore: highscore[1], reverse=True)
    print_highscore()

def show_main_menu():
    clear()
    print("          Guessing Game!         ")
    print("---------------------------------")
    print(f"          Welcome {name}!")
    print("")
    terminal_menu = TerminalMenu(["Play Game","Highscore", "Exit"], accept_keys=("enter", "alt-d", "ctrl-i"))
    menu_entry_index = terminal_menu.show()
    key_enter(menu_entry_index)


def key_enter(index):
    clear()
    main(index)

def main(index):
    if index == 0:
        guess()
    if index == 1:
        show_highscore()
    if index == 2:
        exit_game(EXIT_CODE_NONE)

def key_enter_high_score(index):
    if index == 0:
        clear()
        show_main_menu()
    if index == 1:
        exit_game(EXIT_CODE_NONE)


def set_name(err):
    global name
    print("Welcome to guessing Game!")
    print("-------------------------")
    if err == 1:
        print("(Names can only include letters, numbers and \'_\')")
    name = input("Please Enter your User Name : ")
    clear()
    if name == "" or re.search("[\W]", name):
        set_name(1)

def init_guessing_game():
    clear()
    open("score.txt", 'a').close()
    set_name()
    hide_cursor()

if __name__ == '__main__':
    try:
        init_guessing_game()
        show_main_menu()
        exit_game(EXIT_CODE_NONE)
    except KeyboardInterrupt:
        exit_game(EXIT_CODE_USER_INTERRUPTION)
