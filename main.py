import random
import sys
import time

stream = sys.stdout

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

def print_main_menu():
    stream.flush()
    print("     Guessing Game!      ")
    print("-------------------------")
    print(" 1.       Highscore      ")
    print(" 2.       Play Game      ")
    print(" 3.       Exit           ")

if __name__ == '__main__':
    while True:
        print_main_menu()
        print("TEST")
        time.sleep(2)
