import random
import keyboard
import os
import sys
import re

if os.name == 'nt':
    import msvcrt
    import ctypes


    class _CursorInfo(ctypes.Structure):
        _fields_ = [("size", ctypes.c_int),
                    ("visible", ctypes.c_byte)]

selected_index = 0
menu_size = 3
name = ""
highscore = {}

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

def guess():
    print("Enter your username!")
    name = input()
    print("Hello", name)

    print("Print Highscore? Yes : No")
    confirm = input()
    if confirm == "Yes" or confirm == "y" or confirm == "yes":
        print_highscore()

    x = random.uniform(1, 10)
    x = round(x)
    guess = 12

    score = 10

    while guess != x:
        print("Guess a number between 1 and 10:")
        guess = input()
        if guess == 'End':
            print("Bye!")
            break
        try:
            guess = int(guess)
        except:
            print("Please type in a number!")
            continue

        if (guess < 1 or guess > 10):
            print("Number out of Range!")
            continue

        if guess < x:
            print("Higher")
        elif guess > x:
            print("Lower")
        else:
            print("Correct!", name, "Your Score is", score, "!")
            write_score(score, name)
            print("One more round? Yes : No?")
            confirm = input()
            if confirm == "Yes" or confirm == "y" or confirm == "yes":
                x = random.uniform(0, 10)
                x = round(x)
                guess = 12
                score = 10
                continue
        score = score - 1

def exit_game(exit_code):
    clear()
    show_cursor()
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

def print_highscore(index):
    global highscore
    clear()
    print("\t   Highscore!           ")
    print("------------------------------")
    for x in highscore:
        print("   ", str(x[0]).ljust(10), "| ", str(x[1]).rjust(2))
    print("------------------------------")
    print("")
    print("   >>>   " if index == 0 else "        ", "Back        ")
    print("   >>>   " if index == 1 else "        ", "Exit Game   ")

def show_highscore():
    f = open("score.txt", "r")
    array = f.read().split("\n")
    global highscore
    global selected_index
    global menu_size
    highscore = {}
    for score in array:
        if score == '':
            continue
        highscore[score.split('//')[0]] = score.split('//')[1]
    highscore = sorted(highscore.items(), key=lambda highscore: highscore[1], reverse=True)

    selected_index = 0
    menu_size = 2

    print_highscore(selected_index)

    keyboard.add_hotkey('up', lambda: key_up(print_highscore))
    keyboard.add_hotkey('down', lambda: key_down(print_highscore))

def show_main_menu():
    print_main_menu(selected_index)

    keyboard.add_hotkey('up', lambda: key_up(print_main_menu))
    keyboard.add_hotkey('down', lambda: key_down(print_main_menu))
    keyboard.add_hotkey('enter', lambda: key_enter())

    keyboard.wait()

def print_main_menu(index):
    print("          Guessing Game!         ")
    print("---------------------------------")
    print(f"          Welcome {name}!")
    print("")
    print("   >>>   " if index == 0 else "        ", "Highscore      ")
    print("   >>>   " if index == 1 else "        ", "Play Game      ")
    print("   >>>   " if index == 2 else "        ", "Exit      ")

def key_up(func):
    global selected_index
    global menu_size
    selected_index = (selected_index - 1) % menu_size
    clear()
    func(selected_index)

def key_down(func):
    global selected_index
    global menu_size
    selected_index = (selected_index + 1) % menu_size
    clear()
    func(selected_index)

def key_enter():
    global selected_index
    clear()
    keyboard.remove_all_hotkeys()
    main(selected_index)

def main(index):
    if index == 0:
        show_highscore()
    if index == 1:
        guess()
    if index == 2:
        exit_game(EXIT_CODE_NONE)

def set_name():
    global name

    print("Welcome to guessing Game!")
    print("-------------------------")
    name = input("Please Enter your User Name : ")
    clear()
    if name == "" or re.search("[\W]", name) is not None:
        set_name()

def init_guessing_game():
    clear()
    open("score.txt", 'a').close()
    set_name()
    hide_cursor()

if __name__ == '__main__':
    try:
        init_guessing_game()
        show_main_menu()
        exit_game(0)
    except KeyboardInterrupt:
        exit_game(EXIT_CODE_USER_INTERRUPTION)
