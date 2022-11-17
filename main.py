import random
import requests
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
level = "easy"

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


def print_game_title(max_range = 10,error = ""):
    clear()
    print("          Guessing Game!         ")
    print("---------------------------------")
    if not error == "":
        print(error)
        print("")
    print(f"Guess a number between 1 and {max_range}: ")

def manhatten_distance(list_a, list_b):
    return sum( map( lambda x, y: abs(x-y), list_a, list_b))


def treasure_hunt():
    treasure = (int(random.uniform(1, 10)), int(random.uniform(1, 10)))
    score = 10
    while True:
        location = (int (input("Input the koordinates you want to search for treasure\n x: ")), int (input(" y: ")))
        distance = manhatten_distance(treasure, location)
        print(f"You are {distance} steps away from the treasure {treasure}")
        if distance == 0:
            break
        score = (score - 1) if score > 0 else 0
    print(f"gg! your score is: {score} points")
    input()
    show_main_menu()

def guess():
    global level

    range_max = 10
    clear()
    print("          Guessing Game!         ")
    print("---------------------------------")
    terminal_menu = TerminalMenu(["Leicht", "Mittel", "Schwer"], accept_keys=("enter", "alt-d", "ctrl-i"))
    menu_entry_index = terminal_menu.show()

    if menu_entry_index == 0:
        range_max = 10
        level = "easy"
    elif menu_entry_index == 1:
        range_max = 59
        level = "medium"
    elif menu_entry_index == 2:
        range_max = 100
        level = "hard"



    # todo Schwierigkeiten Low,Medium,High

    x = random.uniform(1, range_max)
    x = round(x)
    guess = 102

    score = 10

    print_game_title(max_range=range_max)

    while guess != x:
        guess = input()
        if guess == 'End':
            print("Bye!")
            break
        try:
            guess = int(guess)
        except:
            print_game_title(range_max,"Please type in a number!")
            continue

        if (guess < 1 or guess > range_max):
            print_game_title(range_max,"Number out of Range!")
            continue

        if guess < x:
            print_game_title(range_max,"Higher")
        elif guess > x:
            print_game_title(range_max,"Lower")
        else:
            clear()
            print("          Guessing Game!         ")
            print("---------------------------------")
            print("Correct!", name, "Your Score is", score, "!")
            print("")
            write_score(score, name,"guessing_game",level)
            terminal_menu = TerminalMenu(["New Game", "Back", "Exit"], accept_keys=("enter", "alt-d", "ctrl-i"))
            menu_entry_index = terminal_menu.show()
            if terminal_menu.chosen_menu_index == 0:
                x = random.uniform(0, 10)
                x = round(x)
                guess = 102
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

def write_score(score, name,game,level):
    url = "http://localhost:3000/highscore/" + game + "/" + level
    myobj = {
        "name": name,
        "points": score
    }
    x = requests.post(url, json=myobj)

def print_highscore(game,level):
    clear()
    url = "http://localhost:3000/highscore/" + game + "/" + level
    x = requests.get(url)
    x = x.json()

    print(f"{'Highscore!':^30s}")
    print(f"{'-':-^30s}")
    for score in x:
        print("   ", str(score['name']).ljust(10), "| ", str(score['points']).rjust(2))
    print(f"{'-':-^30s}")
    print("")
    
    terminal_menu = TerminalMenu(["Back", "Exit"], accept_keys=("enter", "alt-d", "ctrl-i"))
    menu_entry_index = terminal_menu.show()
    if menu_entry_index == 0:
        highscore_level(game)
    elif menu_entry_index == 1:
        exit_game(EXIT_CODE_NONE)

def highscore_level(game):
    clear()
    print(f"{'Highscore!':^30s}")
    print(f"{'-':-^30s}")
    terminal_menu = TerminalMenu(["Leicht", "Mittel", "Schwer","Back","Exit"], accept_keys=("enter", "alt-d", "ctrl-i"))
    menu_entry_index = terminal_menu.show()
    if menu_entry_index == 0:
        print_highscore(game,"easy")
    elif menu_entry_index == 1:
        print_highscore(game,"medium")
    elif menu_entry_index == 2:
        print_highscore(game,"hard")
    elif menu_entry_index == 3:
        show_highscore()
    elif menu_entry_index == 4:
        exit_game(EXIT_CODE_NONE)

def show_highscore():
    clear()
    print(f"{'Highscore!':^30s}")
    print(f"{'-':-^30s}")
    terminal_menu = TerminalMenu(["Guessing Game", "Treasure Hunt","Back","Exit"],accept_keys=("enter", "alt-d", "ctrl-i"))
    menu_entry_index = terminal_menu.show()
    if menu_entry_index == 0:
        highscore_level("guessing_game")
    elif menu_entry_index == 1:
        highscore_level("treasure_hunt")
    elif menu_entry_index == 2:
        show_main_menu()
    elif menu_entry_index == 3:
        exit_game(EXIT_CODE_NONE)


def show_main_menu():
    clear()
    print("          Guessing Game!         ")
    print("---------------------------------")
    print(f"          Welcome {name}!")
    print("")
    terminal_menu = TerminalMenu(["Play Guess Game", "Play Treasure Hunt","Highscore", "Exit"], accept_keys=("enter", "alt-d", "ctrl-i"))
    menu_entry_index = terminal_menu.show()
    key_enter(menu_entry_index)


def key_enter(index):
    clear()
    main(index)

def main(index):
    if index == 0:
        guess()
    if index == 1:
        treasure_hunt()
    if index == 2:
        show_highscore()
    if index == 3:
        exit_game(EXIT_CODE_NONE)

def key_enter_high_score(index):
    if index == 0:
        clear()
        show_main_menu()
    if index == 1:
        exit_game(EXIT_CODE_NONE)


def set_name(err = 0):
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
