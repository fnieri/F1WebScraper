from src.plotter import *

class Greeter():
    def __init__(self):
        self.numbers = [1,2,3]

    def welcome(self):
        print("Welcome to the F1 Data Scraper")
        print("Which graph would you like to see?")
        print("1: Pole - win relation")
        print("2: Amount of retirements")
        print("3: Amount of disqualifications")
        number = 0
        while number not in self.numbers:
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

    def select_year_range(self):
        print("Do you wish to select more years or 1 year?")

    def main(self):
        number = self.welcome()
        if number == 1:
            PolePlotter()
        elif number == 2:
            RetiredPlotter()
        else:
            DisqualifiedPlotter()


#if __name__ == "__main__":
 #   main()