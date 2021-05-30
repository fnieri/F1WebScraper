from src.plotter import *


def welcome():
    print("Welcome to the F1 Data Scraper")
    print("Which graph would you like to see?")
    print("1: Pole - win relation")
    print("2: Amount of retirements")
    print("3: Amount of disqualifyings")
    number = 0
    while not 1 <= number <= 3:
        try:
            number = input("Enter the number: ")
            number = int(number)
        except TypeError:
            print("Invalid input, please enter again")
            number = 0
        else:
            if 1 <= number <= 3:
                return number
            else:
                print("Invalid number, please enter again")
def main():
    number = welcome()
    if number == 1:
        PolePlotter()
    elif number == 2:
        RetiredPlotter()
    else:
        DisqualifiedPlotter()


if __name__ == "__main__":
    main()