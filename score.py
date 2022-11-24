import requests
import terminal
from Menu import Menu


def write_score(score, name, game, level, offline):
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
