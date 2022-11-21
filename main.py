import random
import socketio
import requests
import os
import sys
import re
from Menu import Menu

import tictactoe

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

exit_menu = None

in_lobby = False

tic = tictactoe.TicTacToe()

socket = socketio.Client()

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


def print_game_title(max_range=10, error=""):
    clear()
    print("          Guessing Game!         ")
    print("---------------------------------")
    if not error == "":
        print(error)
        print("")
    print(f"Guess a number between 1 and {max_range}: ")


def manhatten_distance(list_a, list_b):
    return sum(map(lambda x, y: abs(x - y), list_a, list_b))


def treasure_hunt():
    treasure = (int(random.uniform(1, 10)), int(random.uniform(1, 10)))
    score = 10
    while True:
        location = (int(input("Input the koordinates you want to search for treasure\n x: ")), int(input(" y: ")))
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
    head = "          Guessing Game!         \n"
    head += "--------------------------------- \n"

    terminal_menu = Menu(["Leicht", "Mittel", "Schwer"],head)
    menu_entry_index = terminal_menu()

    if menu_entry_index == 0:
        range_max = 10
        level = "easy"
    elif menu_entry_index == 1:
        range_max = 59
        level = "medium"
    elif menu_entry_index == 2:
        range_max = 100
        level = "hard"

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
            print_game_title(range_max, "Please type in a number!")
            continue

        if (guess < 1 or guess > range_max):
            print_game_title(range_max, "Number out of Range!")
            continue

        if guess < x:
            print_game_title(range_max, "Higher")
        elif guess > x:
            print_game_title(range_max, "Lower")
        else:
            clear()
            head = "          Guessing Game!         \n"
            head += "---------------------------------\n"
            head += f"Correct! {name} Your Score is {score} ! \n\n"
            write_score(score, name, "guessing_game", level)
            terminal_menu = Menu(["New Game", "Back", "Exit"], head)
            menu_entry_index = terminal_menu()
            if menu_entry_index == 0:
                x = random.uniform(0, 10)
                x = round(x)
                guess = 102
                score = 10
                print_game_title()
                continue
            elif menu_entry_index == 1:
                show_main_menu()
            elif menu_entry_index == 1:
                exit_game(EXIT_CODE_NONE)
        # todo New Score counting

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


def write_score(score, name, game, level):
    url = "http://localhost:3000/highscore/" + game + "/" + level
    myobj = {
        "name": name,
        "points": score
    }
    x = requests.post(url, json=myobj)


def print_highscore(game, level):
    clear()
    url = "http://localhost:3000/highscore/" + game + "/" + level
    x = requests.get(url)
    x = x.json()

    head = f"{'Highscore!':^30s} \n"
    head += f"{'-':-^30s}\n"
    for score in x:
        head += "   "
        head += str(score['name']).ljust(10)
        head += "| "
        head += str(score['points']).rjust(2)
        head += "\n"

    head += f"{'-':-^30s} \n\n"

    terminal_menu = Menu(["Back", "Exit"], head)
    menu_entry_index = terminal_menu()
    if menu_entry_index == 0:
        highscore_level(game)
    elif menu_entry_index == 1:
        exit_game(EXIT_CODE_NONE)


def highscore_level(game):
    clear()
    head = f"{'Highscore!':^30s} \n"
    head += f"{'-':-^30s} \n"
    terminal_menu = Menu(["Leicht", "Mittel", "Schwer", "Back", "Exit"], head)
    menu_entry_index = terminal_menu()
    if menu_entry_index == 0:
        print_highscore(game, "easy")
    elif menu_entry_index == 1:
        print_highscore(game, "medium")
    elif menu_entry_index == 2:
        print_highscore(game, "hard")
    elif menu_entry_index == 3:
        show_highscore()
    elif menu_entry_index == 4:
        exit_game(EXIT_CODE_NONE)


def show_highscore():
    clear()
    head = f"{'Highscore!':^30s} \n"
    head += f"{'-':-^30s} \n"
    terminal_menu = Menu(["Guessing Game", "Treasure Hunt", "Back", "Exit"], head)
    menu_entry_index = terminal_menu()
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
    head = "          Guessing Game!         \n"
    head += "---------------------------------\n"
    head += f"          Welcome {name}!\n"
    terminal_menu = Menu(["Play Guess Game", "Play Treasure Hunt", "Tic Tac Toe", "Multiplayer", "Highscore", "Exit"], head)
    menu_entry_index = terminal_menu()
    key_enter(menu_entry_index)


def key_enter(index):
    clear()
    main(index)


def show_multiplayer():
    clear()
    head = f"{'Welcome to Multiplayer!':^30s}"
    head += f"{'-':-^30s}"
    terminal_menu = Menu(["New Game", "Lobby"], head)
    menu_entry_index = terminal_menu()
    select_multiplayer(menu_entry_index)


def select_multiplayer(select, error=""):
    clear()
    if select == 0:
        print(f"{'Welcome to Multiplayer!':^30s}")
        print(f"{'-':-^30s}")
        print("")
        if error != "":
            print(error)
        room_name = input("Enter the name of your Room: ")
        socket.emit('Client:new_room', {"room_name": room_name, "name": name})

    elif select == 1:
        global in_lobby
        socket.emit('Client:get_rooms')
        in_lobby = True


def main(index):
    if index == 0:
        guess()
    if index == 1:
        treasure_hunt()
    if index == 2:
        tic_tac_toe()
    if index == 3:
        show_multiplayer()
    if index == 4:
        show_highscore()
    if index == 5:
        exit_game(EXIT_CODE_NONE)


def key_enter_high_score(index):
    if index == 0:
        clear()
        show_main_menu()
    if index == 1:
        exit_game(EXIT_CODE_NONE)

def tic_tac_toe():
    clear()
    global tic
    player = tic.start()
    tic.victory()
    clear()
    head = "   Tic Tac Toe \n"
    if player == 0:
        head += "No one won!"
    else:
        head += f"   Player {player} wins!"

    head += "\n--------------------\n"
    terminal_menu = Menu(["New Game", "Back", "Exit"], head)
    menu_entry_index = terminal_menu()
    if menu_entry_index == 0:
        tic_tac_toe()
    elif menu_entry_index == 1:
        show_main_menu()
    elif menu_entry_index == 2:
        exit_game(EXIT_CODE_NONE)


def set_name(err=0):
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


@socket.on('Server:room_created')
def on_message(data):
    clear()
    room_name = data['name']
    head = f"{f'New Room created! {room_name}':^30s} \n"
    head += f"{'-':-^30s} \n"
    head += "Waiting for Player Joining! \n"
    menu = Menu(['Back','Exit'],head)
    select = menu()
    if select == 0:
        socket.emit('Client:leave_room', "Client_" + room_name)
        show_main_menu()
    elif select == 1:
        exit_game(EXIT_CODE_NONE)


@socket.on('Server:room_exits')
def on_message(data):
    clear()
    select_multiplayer(0, f"Room allready Exits! {data}")


@socket.on('Server:rooms')
def rooms(data):
    global in_lobby
    global exit_menu
    clear()
    head = "   Multiplayer Lobby!           \n"
    head += "--------------------------------\n"
    head += "   Please choice your Room?     \n"
    if in_lobby:
        data.append('Back')
        data.append('Exit')
        if exit_menu is not None:
            exit_menu.set_data(data)
        else:
            exit_menu = Menu(data, head)
            select = exit_menu()
            if select == len(data) - 1:
                exit_game(EXIT_CODE_NONE)
            elif select == len(data) - 2:
                clear()
                show_main_menu()


if __name__ == '__main__':
    try:
        socket.connect('http://localhost:3000')
        init_guessing_game()
        show_main_menu()
        socket.wait()
        exit_game(EXIT_CODE_NONE)
    except KeyboardInterrupt:
        exit_game(EXIT_CODE_USER_INTERRUPTION)
