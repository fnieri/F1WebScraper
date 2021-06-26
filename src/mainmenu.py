from .plotter import *
import os
from .errors import *
from .const import *


class MainMenu:
    def __init__(self):
        self.numbers = [1, 2, 3, 4]
        self.start_year = 1950
        self.end_year = 2020
        self.single_year = False

    def mmenu(self):
        numbers = [1, 2, 3, 4]
        mmenu_dict = {1: self.select_years_main}
        self.mmenu_main_print()
        while True:
            try:
                number = input("Enter the number: ")
                number = int(number)
                mmenu_dict[number]()
            except TypeError:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Invalid input, please enter again")
                self.mmenu_main_print()
            except KeyError:
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f"Invalid number, enter a number between {numbers[0]} and {numbers[-1]}")
                self.mmenu_main_print()
            else:
                break

    def mmenu_main_print(self):
        print("Welcome to the F1 Data Scraper")
        print("Which graph would you like to see?")
        print(" [ 1 ] : Pole - win relation")
        print(" [ 2 ] : Retirements' data")
        print(" [ 3 ] : Amount of disqualifications")
        if self.single_year:
            print(f" [ 4 ] : Change year(s) (Current : {self.start_year}")
        else:
            print(f" [ 4 ] : Change year(s) (Current : {self.start_year} - {self.end_year})")


    def select_years_main(self):
        years_dict = {1: self.select_years_main_case1, 2: self.select_years_main_case2}
        self.select_years_main_print()
        while True:
            try:
                number = input("Enter the number: ")
                number = int(number)
                years_dict[number]()
            except TypeError:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Invalid input, please enter again")
                self.select_years_main_print()
            except KeyError:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Invalid number, enter 1 or 2")
                self.select_years_main_print()
            else:
                break

    def select_years_main_case1(self, number):
        stop = False
        year_valid = False
        while not stop:
            if not year_valid:
                try:
                    self.start_year = int(input())
                    self.year_is_correct(self.start_year)
                except TypeError:
                    print("Enter a valid number")
                except InvalidYear:
                    print(f"Enter an year between 1950 and {LAST_YEAR}")
                else:
                    year_valid = True
                    stop = True
        if number == 2:
            self.end_year = self.start_year
        else:
            self.select_years_main_case2()

    def select_years_main_case2(self):
        stop = False
        year_valid = False
        while not stop:
            if not year_valid:
                try:
                    self.end_year = int(input())
                    self.year_is_correct(self.end_year)
                except TypeError:
                    print("Enter a valid number")
                except InvalidYear:
                    print(f"Enter an year between 1950 and {LAST_YEAR}")
                else:
                    year_valid = True
                    stop = True

    def select_years_main_print(self):
        print("Do you wish to select more years or 1 year?")
        print(" [ 1 ] : Multiple years")
        print(" [ 2 ] : Single year")
        print(" [ 3 ] : Go back")


    @staticmethod
    def year_is_correct(year):
        """Check if given year is correct"""
        if 1950 <= year <= LAST_YEAR:
            return True
        else:
            raise InvalidYear
a = MainMenu()
a.mmenu()