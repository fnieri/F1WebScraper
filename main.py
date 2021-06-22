from src.plotter import *

class Greeter():
    def __init__(self):
        self.numbers = [1, 2, 3, 4]
        self.start_year = 1950
        self.end_year = 2020


    def mmenu(self):
        mmenu_dict = {}
        print("Welcome to the F1 Data Scraper")
        print("Which graph would you like to see?")
        print(" [ 1 ] : Pole - win relation")
        print(" [ 2 ] : Retirements' data")
        print(" [ 3 ] : Amount of disqualifications")
        print(" [ 4 ] : Change year(s)")
        number = input("Enter the number: ")
        while True:
            try:
                number = int(number)
                mmenu_dict[number]()
            except TypeError:
                print("Invalid input, please enter again")
                number = 0
            except KeyError:
                print(f"Invalid number, enter a number between {self.numbers[0]} and {self.numbers[-1]}")


    def select_years(self):
        print("Do you wish to select more years or 1 year?")
