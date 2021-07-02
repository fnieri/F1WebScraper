import os
from src.Plotters.poleplot import *
import time
from src.sources.colors import *
from src.sources.const import *


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
        """
        Main menu function
        """
        os.system('cls' if os.name == 'nt' else 'clear')    #Clear cmd
        numbers = [1, 4]
        mmenu_dict = {1: self.pole_main, 4: self.select_years_main}    #Function dictionary
        while True:
            try:
                self.mmenu_main_print()
                number = int(input("Enter the number: "))
                mmenu_dict[number]()
            except (TypeError, ValueError, KeyError):       #Other than int
                os.system('cls' if os.name == 'nt' else 'clear')
                print(self.colors.YELLOW + f"Invalid number, enter a number between {numbers[0]} and {numbers[-1]}" + self.colors.ENDC)
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
        """
        User pressed 1 in main menu, pole position choice
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        pole_dict = {1: self.pole.F1plot, 2: self.pole_case_2, 3: self.pole.show_drivers, 4: self.pole_case_4}  # Function dictionary
        numbers = [1, 4]
        while True:

            try:
                self.pole_choice_print(0)
                self.pole_main_print()
                number = int(input("Enter the number: "))   #Enter menu choice
                os.system('cls' if os.name == 'nt' else 'clear')
                if number == 5: #5 to go back
                    return

                self.pole_choice_print(number)
                if number == 1: #Plot
                    pole_dict[number](self.start_year, self.end_year)
                else:
                    pole_dict[number]()

            except (KeyError, ValueError, TypeError):  # number lower than 1 or bigger than numbers[-1]
                os.system('cls' if os.name == 'nt' else 'clear')
                print(self.colors.YELLOW + f"Invalid number, enter a number between {numbers[0]} and {numbers[-1]}"
                      + self.colors.ENDC)

            else:
                os.system('cls' if os.name == 'nt' else 'clear')

    def pole_case_2(self):
        """
        Export year to .csv 1 -> 2 in main menu
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        while True:
            try:
                self.export_print()
                choice1 = int(input("Enter the number: "))  #Enter to go to submenu
                if choice1 == 3:    #3 is go_back
                    return
                self.export_case(choice1)   #Go to submenu
            except (AssertionError, TypeError, ValueError):      #Not 1 or 2
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Enter 1 or 2")
            else:
                return

    def export_case(self, number):
        """
        1 -> 2 in main menu to select which year(s) to export to csv
        """
        assert number == 1 or number == 2
        if number == 1:
            while True:

                try:
                    year = int(input("Enter the year you want to scrape (or 0 to go back): "))
                    if year == 0:
                        return
                    self.pole.export_to_csv(year, year)

                except (AssertionError, TypeError, ValueError, InvalidYear):  # Wrong year
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("Enter a valid year")
                else:
                    try:
                        input("Enter anything to go back: ")
                    except ValueError:
                        os.system('cls' if os.name == 'nt' else 'clear')
                        return
                    os.system('cls' if os.name == 'nt' else 'clear')
                    return

        elif number == 2:
            while True:

                try:
                    start_year = int(input("Enter the starting year (or 0 to go back): "))
                    if start_year == 0:
                        return
                    self.year_is_correct(start_year)    #Check correctness

                    end_year = int(input("Enter the end year (or 0 to change start year): "))
                    if end_year == 0:
                        raise StopSelection
                    self.year_is_correct(end_year)  #Recheck

                    if end_year < start_year:   #Swap years if end < start
                        start_year, end_year = end_year, start_year

                    diff = end_year - start_year
                    if diff > 10:       #Ask user if he wants to save more than 10 years
                        prompt = int(input(f"Do you wish to select {diff} years? ( 1 : Yes, 2 : No)"))
                        if prompt == 1:
                            self.pole.export_to_csv(start_year, end_year)
                        elif prompt == 2:   #2 = Users wants to go back
                            raise StopIteration

                    else:
                        self.pole.export_to_csv(start_year, end_year)
                        print("Files have been exported, going back")
                        time.sleep(2)

                except (AssertionError, TypeError, ValueError):  # Wrong year, not int, blank
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("Enter a valid year")
                except StopIteration:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    return
                except StopSelection:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    pass

    def export_print(self):
        """
        Print auxiliary for export prompt
        1 -> 2 -> in main menu
        """
        print("Do you wish to export:")
        print(" [ 1 ] : A single year")
        print(" [ 2 ] : Multiple years")
        print(" [ 3 ] : Go back")

    def pole_case_4(self):
        """
        1 -> 4 in main menu
        See an year's pole sitter and winner for every race + pole-win chance
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        choice = False
        year = 1982
        while True:
            try:
                if not choice:
                    self.pole_choice_print(4)
                    year = int(input("Enter the year you want to see stats from (or 0 to go back): "))
                    if year == 0:
                        return
                year_data = self.pole.get_year_data(year)       #Get an year's data
            except (AssertionError, TypeError, ValueError):      #Year is incorrect, not an int, or blank
                os.system('cls' if os.name == 'nt' else 'clear')
                print(self.colors.YELLOW + f"Enter an year between 1950 and {LAST_YEAR}" + self.colors.ENDC)
            else:
                print(year_data) #Print an year's data
                try:
                    self.year_stats_print(year)
                    prompt = int(input("Enter the number: "))
                    if prompt == 1:
                        os.system('cls' if os.name == 'nt' else 'clear')
                        year -= 1
                        choice = True
                    elif prompt == 2:
                        os.system('cls' if os.name == 'nt' else 'clear')
                        return
                    elif prompt == 3:
                        os.system('cls' if os.name == 'nt' else 'clear')
                        choice = True
                        year += 1
                except (AssertionError, TypeError, ValueError):  # Not 1 or 2  or 3
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("Enter 1 or 2")

    @staticmethod
    def year_stats_print( year):
        if year != 1950:
            print(f" [ 1 ] : View previous year ({year - 1})")
        print(" [ 2 ] : Go back")
        if year != LAST_YEAR:
            print(f" [ 3 ] : View next year ({year + 1})")

    @staticmethod
    def pole_main_print():
        """
        Print auxiliary for pole menu
        """
        print(" [ 1 ] : Pole - win relation bar graph ")
        print(" [ 2 ] : Export year(s) to .csv ")
        print(" [ 3 ] : See drivers' stats (WIP) ")
        print(" [ 4 ] : See an year's stats ")
        print(" [ 5 ] : Go back")

    def pole_choice_print(self, number):
        """Print auxiliary for pole choice"""
        poled = {0: " [ 1 ] : Pole - win relation ", 1: " [ 1 ] : Pole - win relation bar graph ", 2: " [ 2 ] : Export data to .csv ",
                 3: " [ 3 ] : See drivers' stats (WIP) ", 4: " [ 4 ] : See an year's stats"}
        print(self.colors.GREEN + f"Current selection => {poled[number]}" + self.colors.ENDC)

    #Export to csv

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

            except (ValueError, TypeError):  #Blank string
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

            except (TypeError, InvalidYear, ValueError):
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
                        for plotter in self.plotters:   #Update plotters with new years range
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
                self.year_is_correct(self.end_year)     #cHECK Year correctness to proceed
            except (InvalidYear, TypeError, ValueError):
                os.system('cls' if os.name == 'nt' else 'clear')
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
