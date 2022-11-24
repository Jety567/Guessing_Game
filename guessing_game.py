import terminal
from Menu import Menu
import random


def _print_game_title(max_range=10, error=""):
    terminal.clear()
    print("          Guessing Game!         ")
    print("---------------------------------")
    if not error == "":
        print(error)
        print("")
    print(f"Guess a number between 1 and {max_range}: ")


class Guessing:
    level = "easy"
    name = "Test"

    def _guess(self):
        range_max = 10
        terminal.clear()
        head = "          Guessing Game!         \n"
        head += "--------------------------------- \n"

        terminal_menu = Menu(["Leicht", "Mittel", "Schwer"], head)
        menu_entry_index = terminal_menu()

        if menu_entry_index == 0:
            range_max = 10
            self.level = "easy"
        elif menu_entry_index == 1:
            range_max = 59
            self.level = "medium"
        elif menu_entry_index == 2:
            range_max = 100
            self.level = "hard"

        x = random.uniform(1, range_max)
        x = round(x)
        guess = 102

        score = 10

        _print_game_title(max_range=range_max)

        while guess != x:
            guess = input()
            if guess == 'End':
                print("Bye!")
                break
            try:
                guess = int(guess)
            except:
                _print_game_title(range_max, "Please type in a number!")
                continue

            if guess < 1 or guess > range_max:
                _print_game_title(range_max, "Number out of Range!")
                continue

            if guess < x:
                _print_game_title(range_max, "Higher")
            elif guess > x:
                _print_game_title(range_max, "Lower")
            else:
                terminal.clear()
                head = "          Guessing Game!         \n"
                head += "---------------------------------\n"
                head += f"Correct! {self.name} Your Score is {score} ! \n\n"
                #write_score(score, name, "guessing_game", self.level)
                terminal_menu = Menu(["New Game", "Back", "Exit"], head)
                menu_entry_index = terminal_menu()
                if menu_entry_index == 0:
                    x = random.uniform(0, 10)
                    x = round(x)
                    guess = 102
                    score = 10
                    _print_game_title()
                    continue
                elif menu_entry_index == 1:
                    return 0
                elif menu_entry_index == 1:
                    return 1
            # todo New Score counting

            score = score - 1

    def start(self):
        return self._guess()

    def set_name(self,name):
        self.name = name
