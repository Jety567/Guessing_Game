import random
import socketio
import requests
import os
import re
from Menu import Menu
import terminal
import guessing_game

import tictactoe

name = ""
highscore = {}
keys_dict = {}
level = "easy"
offline = False

exit_menu = None

in_lobby = False

tic = tictactoe.TicTacToe()
guessing = guessing_game.Guessing()

socket = socketio.Client()

# EXIT_CODES
EXIT_CODE_NONE = 0
EXIT_CODE_USER_INTERRUPTION = 1

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


def exit_game(exit_code):
    terminal.clear()
    terminal.show_cursor()
    terminal.clear()
    os._exit(exit_code)


def write_score(score, name, game, level):
    if offline:
        return

    url = "http://localhost:3000/highscore/" + game + "/" + level
    myobj = {
        "name": name,
        "points": score
    }
    x = requests.post(url, json=myobj)


def print_highscore(game, level):
    terminal.clear()
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
    terminal.clear()
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
    terminal.clear()
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
    terminal.clear()
    head = "          Guessing Game!         \n"
    head += "---------------------------------\n"
    head += f"          Welcome {name}!\n"
    if offline:
        head += "          You are Offline!\n"
        terminal_menu = Menu(
            ["Play Guess Game", "Play Treasure Hunt", "Play Tic Tac Toe", "Exit"],
            head)
    else:
        terminal_menu = Menu(["Play Guess Game", "Play Treasure Hunt", "Play Tic Tac Toe", "Multiplayer", "Highscore", "Exit"],
                         head)
    menu_entry_index = terminal_menu()
    key_enter(menu_entry_index)


def key_enter(index):
    terminal.clear()
    if offline and index >= 3:
        index += 2
    main(index)


def show_multiplayer():
    terminal.clear()
    head = f"{'Welcome to Multiplayer!':^30s}\n"
    head += f"{'-':-^30s}\n"
    terminal_menu = Menu(["New Game", "Lobby"], head)
    menu_entry_index = terminal_menu()
    select_multiplayer(menu_entry_index)


def select_multiplayer(select, error=""):
    terminal.clear()
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

def join_room():
    socket.emit('')


def main(index):
    if index == 0:
        menu_index = guessing.start()
        if menu_index == 0:
            show_main_menu()
        elif menu_index == 1:
            exit_game(EXIT_CODE_NONE)
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
        terminal.clear()
        show_main_menu()
    if index == 1:
        exit_game(EXIT_CODE_NONE)


def tic_tac_toe():
    terminal.clear()
    global tic
    player = tic.start()
    tic.victory()
    terminal.clear()
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
    terminal.clear()
    if name == "" or re.search("[\W]", name):
        set_name(1)


def init_guessing_game():
    terminal.clear()
    open("score.txt", 'a').close()
    set_name()
    terminal.hide_cursor()


@socket.on('Server:room_created')
def on_message(data):
    terminal.clear()
    room_name = data['name']
    head = f"{f'New Room created! {room_name}':^30s} \n"
    head += f"{'-':-^30s} \n"
    head += "Waiting for Player Joining! \n"
    menu = Menu(['Back', 'Exit'], head)
    select = menu()
    if select == 0:
        socket.emit('Client:leave_room', "Client_" + room_name)
        show_main_menu()
    elif select == 1:
        exit_game(EXIT_CODE_NONE)


@socket.on('Server:room_exits')
def on_message(data):
    terminal.clear()
    select_multiplayer(0, f"Room allready Exits! {data}")


@socket.on('Server:rooms')
def rooms(data):
    global in_lobby
    global exit_menu
    terminal.clear()
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
                terminal.clear()
                show_main_menu()


if __name__ == '__main__':
    try:
        try:
            socket.connect('http://localhost:3000')
        except:
            offline = True

        init_guessing_game()
        guessing.set_name(name)
        show_main_menu()
        socket.wait()
        exit_game(EXIT_CODE_NONE)
    except KeyboardInterrupt:
        exit_game(EXIT_CODE_USER_INTERRUPTION)
