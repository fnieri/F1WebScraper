import os
import sys
from ..Plotters.poleplot import *
import time
from ..sources.colors import *
from ..sources.const import *
from ..sources.errors import *

class MainMenu:
    def __init__(self):
        self.numbers = [1, 2, 3, 4]
        self.start_year, self.end_year = 1950, LAST_YEAR
        self.is_single_year = False

        self.colors = Colors()
        self.pole = PolePlotter(self.start_year, self.end_year)
        self.plotters = [self.pole]

    def go_back_choice(self):
        return

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def main_menu(self):
        """
        Main menu function
        """
        CHOICE_RANGE = [1, 4]
        while True:
            try:
                self.mainmenu_choice_selection()
            
            except (TypeError, ValueError, KeyError) as NotAnInt:
                self.clear_terminal()
                print(self.colors.YELLOW + f"Invalid number, enter a number between {CHOICE_RANGE[0]} and {CHOICE_RANGE[-1]}" + self.colors.ENDC)
            
            else:
                self.clear_terminal()

    def main_menu_print_user_choice(self):
        print("Welcome to the F1 Data Scraper")
        print("Which graph would you like to see? \n")
        print(" [ 1 ] : Pole - win relation \n")
        print(" [ 2 ] : Retirements' data \n")
        print(" [ 3 ] : Amount of disqualifications \n")

        if self.is_single_year:
            print(f" [ 4 ] : Change year(s) (Current : {self.start_year}) \n")
        else:
            print(f" [ 4 ] : Change year(s) (Current : {self.start_year} - {self.end_year}) \n")

    def mainmenu_choice_selection(self):

        mainmenu_choice_dictionary = {1: self.pole_choice_main, 4: self.select_years_main}
        
        self.main_menu_print_user_choice()
        USER_SELECTION = int(input("Enter the number: "))
        
        mainmenu_choice_dictionary[USER_SELECTION]()

    #Pole win relation

    def pole_choice_main(self):
        """
        User pressed 1 in main menu, pole position choice
        """
        self.clear_terminal()
        CHOICE_RANGE = [1, 5]

        while True:

            try:
                self.try_to_execute_pole_choice()
            
            except (KeyError, ValueError, TypeError) as OutOfRange:
                self.clear_terminal()
                print(self.colors.YELLOW + f"Invalid number, enter a number between {CHOICE_RANGE[0]} and {CHOICE_RANGE[-1]}"
                      + self.colors.ENDC)

            else:
                self.clear_terminal()

    def try_to_execute_pole_choice(self):
        USER_CHOSE_1_ON_MAIN_MENU = 0
        GO_BACK = 5
        POLE_GRAPH_PLOT = 1
        pole_choice_dictionary = {1: self.pole.F1plot, 2: self.pole_case_2, 3: self.pole.show_drivers, 4: self.pole_case_4, 5: self.go_back_choice}
        
        self.pole_choice_print(USER_CHOSE_1_ON_MAIN_MENU)
        self.pole_main_print()

        USER_SELECTION = int(input("Enter the number: "))
        self.clear_terminal()

        if USER_SELECTION == GO_BACK:
            return
        self.pole_choice_print(USER_SELECTION)
        if USER_SELECTION == POLE_GRAPH_PLOT:
            pole_choice_dictionary[USER_SELECTION](self.start_year, self.end_year)
        else:
            pole_choice_dictionary[USER_SELECTION]()

        
    def pole_case_2(self):
        """
        Export year to .csv 1 -> 2 in main menu
        """
        self.clear_terminal()
        
        while True:
            
            try:
                self.try_to_select_csv_years_in_menu()
           
            except (AssertionError, TypeError, ValueError):      #Not 1 or 2
                self.clear_terminal()
                print("Enter 1 or 2")
                self.export_print()
           
            else:
                return

    def try_to_select_csv_years_in_menu(self):
        GO_BACK = 3
        self.export_print()
        USER_CHOICE_1 = int(input("Enter the number: "))  
        if USER_CHOICE_1 == GO_BACK:    
            return
        self.export_submenu_pole_case_2(USER_CHOICE_1)   #Go to submenu

    def export_submenu_pole_case_2(self, choice):
        """
        1 -> 2 in main menu to select which year(s) to export to csv
        """
        assert choice == 1 or choice == 2
        if choice == 1:
            while True:

                try:
                    self.clear_terminal()
                    year = int(input("Enter the year you want to scrape (or 0 to go back): "))
                    if year == 0:
                        return
                    self.pole.export_to_csv(year, year)

                except (AssertionError, TypeError, ValueError, InvalidYear):  # Wrong year
                    self.clear_terminal()
                    print("Enter a valid year")
                else:

                    try:
                        self.clear_terminal()
                        prompt = int(input("Enter 1 to open file with the default app for .csv files \n"
                                           "or enter anything to return to main menu: "))
                        if prompt == 1:
                            os.startfile(os.getcwd() + "\src\csv_out\\" + f"{year}_data.csv", "open")
                    except (TypeError, ValueError):
                        self.clear_terminal()
                        return
                    self.clear_terminal()
                    return

        elif choice == 2:
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
                        print("Files have been exported")
                        prompt = int(input("Enter 1 to select an year you want to open with the default app for .csv files \n"
                                           "or enter anything to return to main menu: "))
                        if prompt == 1:
                            stop = False
                            while not stop:
                                year = int(input("Select the year: "))
                                try:
                                    os.startfile(os.getcwd() + "\src\csv_out\\" + f"{year}_data.csv", "open")
                                except (FileNotFoundError, ValueError, TypeError):
                                    self.clear_terminal()
                                    print(f"Invalid year, please enter an year you have exported (current years are {start_year} - {end_year})")
                                else:
                                    input("Enter anything to go back to the main menu")
                                    return

                except (AssertionError, TypeError, ValueError):  # Wrong year, not int, blank
                    self.clear_terminal()
                    print("Enter a valid year")
                except StopIteration:
                    self.clear_terminal()
                    return
                except StopSelection:
                    self.clear_terminal()
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
        self.clear_terminal()
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
                self.clear_terminal()
                print(self.colors.YELLOW + f"Enter an year between 1950 and {LAST_YEAR}" + self.colors.ENDC)
            else:
                print(year_data) #Print an year's data
                try:
                    self.year_stats_print(year)
                    prompt = int(input("Enter the number: "))
                    if prompt == POLE_BACK:
                        self.clear_terminal()
                        year -= 1
                        choice = True
                    elif prompt == POLE_EXIT:
                        self.clear_terminal()
                        return
                    elif prompt == POLE_FORWARD:
                        self.clear_terminal()
                        choice = True
                        year += 1
                except (AssertionError, TypeError, ValueError):  # Not 1 or 2  or 3
                    self.clear_terminal()
                    print("Enter 1 / 2 / 3")

    @staticmethod
    def year_stats_print(year):
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

    #Retirements data

    def retirement_main(self):
        pass

    def retirement_main_print(self):
        print(" [ 1 ] : Retirements per year bar graph")
        print(" [ 2 ] : Percentage of retirements/participants per year")
        print(" [ 3 ] : Percentage of retirements/participants per race in an year")
        print(" [ 4 ] : Export year to .csv ( TBD ) ")


    #Select years prompt

    def select_years_main(self):
        """
        User pressed 4 in main menu
        User is given the option to choose between multiple or single years
        """
        self.clear_terminal()
        while True:

            try:
                self.select_years_choice_print(0)   # Print selections
                self.select_years_main_print()

                NUMBER = int(input("Enter the number: "))
                if NUMBER == 1 or NUMBER == 2:
                    self.clear_terminal()
                    self.select_years_main_case1(NUMBER)  #Number 1 = Multiple years 2 = Single year

                elif NUMBER == 3:
                    self.clear_terminal()
                    return

                else:
                    raise TypeError

            except (ValueError, TypeError):  #Blank string
                self.clear_terminal()
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
        self.clear_terminal()
        self.select_years_choice_print(number)
        while not stop:

            try:
                if number != 2:     #2 = single year
                    self.start_year = int(input("Enter start year (or 0 to go back) : "))
                else:
                    self.start_year = int(input("Enter the year you want to scrape (or 0 to go back) : "))

                if self.start_year == 0:    #User goes back
                    self.clear_terminal()
                    self.start_year = tmp
                    return
                self.year_is_correct(self.start_year)

            except (TypeError, InvalidYear, ValueError):
                self.clear_terminal()
                print(self.colors.YELLOW + f"Enter an year between 1950 and {LAST_YEAR}" + self.colors.ENDC)

            else:

                if number == 2:     #Single year
                    self.clear_terminal()
                    self.is_single_year = True
                    self.end_year = self.start_year
                    stop = True
                    for plotter in self.plotters:
                        plotter.update(self.start_year, self.end_year)

                else:

                    self.clear_terminal()
                    stop = self.select_years_main_case2()   #Check if user wants to change start year before stopping loop
                    if stop:
                        if self.start_year > self.end_year: #Check if years are sorted to avoid problems
                            self.start_year, self.end_year = self.end_year, self.start_year
                            self.clear_terminal()
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
                self.clear_terminal()
                print(self.colors.YELLOW + f"Enter an year between 1950 and {LAST_YEAR}" + self.colors.ENDC)
            else:
                self.clear_terminal()
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

