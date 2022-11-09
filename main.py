import random
import curses
import os
def guess():
    print("Enter your username!")
    name = input()
    print("Hello",name)

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
            print("Correct!", name ,"Your Score is", score , "!")
            write_score(score,name)
            print("One more round? Yes : No?")
            confirm = input()
            if confirm == "Yes" or confirm == "y" or confirm == "yes":
                x = random.uniform(0, 10)
                x = round(x)
                guess = 12
                score = 10
                continue
        score = score - 1

def clear():
    if (os.name == 'posix'):
        os.system('clear')
    # else screen will be cleared for windows
    else:
        os.system('cls')

def write_score(score,name):
    f = open("score.txt", "a")
    f.write(name)
    f.write("//")
    f.write(str(score))
    f.writelines('\n')
    f.close()

def print_highscore():
    f = open("score.txt", "r")
    array = f.read().split("\n")
    highscore = {}
    for score in array:
        if score == '':
            continue
        highscore[score.split('//')[0]] = score.split('//')[1]
    highscore = sorted(highscore.items(), key=lambda highscore: highscore[1],reverse=True)

    print("         Highscore!           ")
    print("------------------------------")

    for x in highscore:
        print("   ",x[0], " | ",x[1])
    print("------------------------------")

def show_main_menu():
    selected_index = 0
    print_main_menu(selected_index)
    arrow_key = curses.initscr().getch()

    if arrow_key == curses.KEY_UP:
        selected_index = selected_index + 1
        print_main_menu(selected_index)
    elif arrow_key == curses.KEY_DOWN:
        selected_index = selected_index - 1
        print_main_menu(selected_index)
def print_main_menu(index):
    print("     Guessing Game!      ")
    print("-------------------------")
    print("   >   " if index == 0 else "       ", "Highscore      ")
    print("   >   " if index == 1 else "       ", "Play Game      ")
    print("   >   " if index == 2 else "       ", "Exit      ")

if __name__ == '__main__':
    show_main_menu()


