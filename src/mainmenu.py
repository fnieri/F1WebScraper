import os

from plotters.poleplot import *
import time
from sources.colors import *
from sources.const import *

class MainMenu:
    def __init__(self):
        self.numbers = [1, 2, 3, 4]
        self.start_year = 1950
        self.end_year = LAST_YEAR
        self.single_year = False

        self.colors = Colors()
        self.pole = PolePlotter(self.start_year, self.end_year)
        self.plotters = [self.pole]

    def mmenu(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        numbers = [1, 4]
        mmenu_dict = {1: self.pole_main, 4: self.select_years_main}    #Function dictionary
        while True:
            try:
                self.mmenu_main_print()
                number = int(input("Enter the number: "))
                mmenu_dict[number]()
            except TypeError:       #Other than int
                os.system('cls' if os.name == 'nt' else 'clear')
                print(self.colors.YELLOW + "Invalid input, please enter again" + self.colors.ENDC)
            except KeyError:    # number lower than 1 or bigger than numbers[-1]
                os.system('cls' if os.name == 'nt' else 'clear')
                print(self.colors.YELLOW + f"Invalid number, enter a number between {numbers[0]} and {numbers[-1]}" + self.colors.ENDC)
            except ValueError:  #Nothing inserted
                os.system('cls' if os.name == 'nt' else 'clear')
                print(self.colors.YELLOW + "Invalid input, please enter again" + self.colors.ENDC)
            else:
                os.system('cls' if os.name == 'nt' else 'clear')

    def mmenu_main_print(self):
        print("Welcome to the F1 Data Scraper")
        print("Which graph would you like to see? \n")
        print(" [ 1 ] : Pole - win relation \n")
        print(" [ 2 ] : Retirements' data \n")
        print(" [ 3 ] : Amount of disqualifications \n")
        if self.single_year:
            print(f" [ 4 ] : Change year(s) (Current : {self.start_year}) \n")
        else:
            print(f" [ 4 ] : Change year(s) (Current : {self.start_year} - {self.end_year}) \n")

    #Pole win relation

    def pole_main(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        pole_dict = {1: self.pole.F1plot, 3: self.pole.show_drivers, 4: self.pole_case_4}  # Function dictionary
        numbers = [1, 4]
        while True:
            try:
                self.pole_choice_print(0)
                self.pole_main_print()
                number = int(input("Enter the number: "))
                os.system('cls' if os.name == 'nt' else 'clear')
                self.pole_choice_print(number)
                if number == 1:
                    pole_dict[number](self.start_year, self.end_year)
                else:
                    pole_dict[number]()
            except TypeError:  # Other than int
                os.system('cls' if os.name == 'nt' else 'clear')
                print(self.colors.YELLOW + "Invalid input, please enter again", + self.colors.ENDC)
            except KeyError:  # number lower than 1 or bigger than numbers[-1]
                os.system('cls' if os.name == 'nt' else 'clear')
                print(self.colors.YELLOW + f"Invalid number, enter a number between {numbers[0]} and {numbers[-1]}"
                      + self.colors.ENDC)
            except ValueError:  # Nothing inserted
                os.system('cls' if os.name == 'nt' else 'clear')
                print(self.colors.YELLOW + "Invalid input, please enter again" + self.colors.ENDC)
            else:
                os.system('cls' if os.name == 'nt' else 'clear')
                return

    def pole_case_4(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(self.colors.GREEN + "Current selection =>  [ 4 ] : See an year's stats " + self.colors.ENDC)
        while True:
            try:
                year = int(input(" Enter the year you want to see stats from: "))
                year_data = self.pole.get_year_data(year)
            except AssertionError:
                print(self.colors.YELLOW + f"Enter an year between 1950 and {LAST_YEAR}" + self.colors.ENDC)
            except TypeError:
                #       os.system('cls' if os.name == 'nt' else 'clear')
                print(self.colors.YELLOW + f"Enter an year between 1950 and {LAST_YEAR}" + self.colors.ENDC)
            except ValueError:
                #        os.system('cls' if os.name == 'nt' else 'clear')
                print(self.colors.YELLOW + f"Enter an year between 1950 and {LAST_YEAR}" + self.colors.ENDC)
            else:
                pass

    @staticmethod
    def pole_main_print():
        print(" [ 1 ] : Pole - win relation bar graph ")
        print(" [ 2 ] : Export data to .csv (WIP) ")
        print(" [ 3 ] : See drivers' stats (WIP) ")
        print(" [ 4 ] : See an year's stats ")

    def pole_choice_print(self, number):
        poled = {0: " [ 1 ] : Pole - win relation ", 1: " [ 1 ] : Pole - win relation bar graph ", 2: " [ 2 ] : Export data to .csv (WIP) ",
                 3: " [ 3 ] : See drivers' stats (WIP) ", 4: " [ 4 ] : See an year's stats"}
        print(self.colors.GREEN + f"Current selection => {poled[number]}" + self.colors.ENDC)

    #Select years prompt

    def select_years_main(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        while True:
            try:
                self.select_years_choice_print(0)
                self.select_years_main_print()
                number = int(input("Enter the number: "))
                if number == 1 or number == 2:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    self.select_years_main_case1(number)
                elif number == 3:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    return
                else:
                    raise TypeError
            except TypeError:     #=/= int
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Invalid input, please enter again")
                self.select_years_main_print()
            except ValueError:  #Blank string
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Please enter 1 or 2")
                self.select_years_main_print()
            else:
                pass

    def select_years_main_case1(self, number):
        """
        Deciding start year and year if multiple years were chosen or just the one year if it was chosen
            Param:
                number (int) : Number inserted by user
        """
        stop = False
        tmp = self.start_year   #Save start year if user goes back
        os.system('cls' if os.name == 'nt' else 'clear')
        self.select_years_choice_print(number)
        while not stop:
            try:
                if number != 2:     #2 = single year
                    self.start_year = int(input("Enter start year (or 0 to go back) : "))
                else:
                    self.start_year = int(input("Enter the year you want to scrape (or 0 to go back) : "))
                if self.start_year == 0:    #User goes back
                    os.system('cls' if os.name == 'nt' else 'clear')
                    self.start_year = tmp
                    return
                self.year_is_correct(self.start_year)
            except TypeError:
                os.system('cls' if os.name == 'nt' else 'clear')
                print(self.colors.YELLOW + f"Enter an year between 1950 and {LAST_YEAR}" + self.colors.ENDC)
            except InvalidYear:
                os.system('cls' if os.name == 'nt' else 'clear')
                print(self.colors.YELLOW + f"Enter an year between 1950 and {LAST_YEAR}" + self.colors.ENDC)
            except ValueError:
                os.system('cls' if os.name == 'nt' else 'clear')
                print(self.colors.YELLOW + f"Enter an year between 1950 and {LAST_YEAR}" + self.colors.ENDC)
            else:
                if number == 2:     #Single year
                    os.system('cls' if os.name == 'nt' else 'clear')
                    self.single_year = True
                    self.end_year = self.start_year
                    stop = True
                    for plotter in self.plotters:
                        plotter.update(self.start_year, self.end_year)
                else:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    stop = self.select_years_main_case2()   #Check if user wants to change start year before stopping loop
                    if stop:
                        if self.start_year > self.end_year: #Check if years are sorted to avoid problems
                            self.start_year, self.end_year = self.end_year, self.start_year
                            os.system('cls' if os.name == 'nt' else 'clear')
                        for plotter in self.plotters:
                            plotter.update(self.start_year, self.end_year)

    def select_years_main_case2(self):
        tmp = self.end_year     #Save end year in case user goes back
        while True:
            try:
                self.select_years_choice_print(1)
                self.end_year = int(input("Enter end year (or 0 to change start year): "))
                if self.end_year == 0:  #User goes back
                    self.end_year = tmp
                    return False
                self.year_is_correct(self.end_year)
            except InvalidYear:
                #      os.system('cls' if os.name == 'nt' else 'clear')
                print(self.colors.YELLOW + f"Enter an year between 1950 and {LAST_YEAR}" + self.colors.ENDC)
            except TypeError:
                #       os.system('cls' if os.name == 'nt' else 'clear')
                print(self.colors.YELLOW + f"Enter an year between 1950 and {LAST_YEAR}" + self.colors.ENDC)
            except ValueError:
                #        os.system('cls' if os.name == 'nt' else 'clear')
                print(self.colors.YELLOW + f"Enter an year between 1950 and {LAST_YEAR}" + self.colors.ENDC)
            else:
                os.system('cls' if os.name == 'nt' else 'clear')
                return True

    @staticmethod
    def select_years_main_print():
        print("Do you wish to select more years or 1 year? \n")
        print(" [ 1 ] : Multiple years \n")
        print(" [ 2 ] : Single year \n")
        print(" [ 3 ] : Go back \n")


    def select_years_choice_print(self, number):
        printdict = {0: "[ 4 ] : Change year(s)", 1:  "[ 1 ] : Multiple years", 2: "[ 2 ] : Single year"}
        print(self.colors.GREEN + f"Current selection => {printdict[number]}" + self.colors.ENDC)

    @staticmethod
    def year_is_correct(year):
        """Check if given year is correct"""
        if 1950 <= year <= LAST_YEAR:
            return True
        else:
            raise InvalidYear


a = MainMenu()
a.mmenu()
