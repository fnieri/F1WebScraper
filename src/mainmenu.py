import os
from const import *
from errors import *
from plotter import *
import time
from colors import *


class MainMenu:
    colors = Colors()

    def __init__(self):
        self.numbers = [1, 2, 3, 4]
        self.start_year = 1950
        self.end_year = LAST_YEAR
        self.single_year = False
        self.colors = Colors()
        self.pole = PolePlotter(self.start_year, self.end_year)


    def mmenu(self):
        os.system('cls' if os.name == 'nt' else 'clear')
     #   self.mmenu_main_print()
        numbers = [1, 2, 3, 4]
        mmenu_dict = {1: self.pole_main, 4: self.select_years_main}    #Function dictionary
        while True:
            try:
                self.mmenu_main_print()
                number = int(input("Enter the number: "))
                mmenu_dict[number]()
            except TypeError:       #Other than int
                os.system('cls' if os.name == 'nt' else 'clear')
                print(self.colors.YELLOW + "Invalid input, please enter again", + self.colors.ENDC)
      #          self.mmenu_main_print()
            except KeyError:    # number lower than 1 or bigger than numbers[-1]
                os.system('cls' if os.name == 'nt' else 'clear')
                print( self.colors.YELLOW + f"Invalid number, enter a number between {numbers[0]} and {numbers[-1]}" + self.colors.ENDC)
       #         self.mmenu_main_print()
            except ValueError:  #Nothing inserted
                os.system('cls' if os.name == 'nt' else 'clear')
                print(self.colors.YELLOW + "Invalid input, please enter again" + self.colors.ENDC)
        #        self.mmenu_main_print()
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
        #   self.mmenu_main_print()
        numbers = [1, 2, 3]
        pole_dict = {1: self.pole.F1plot, 3: self.pole.show_drivers}  # Function dictionary
        while True:
            try:
                self.pole_main_print()
                number = int(input("Enter the number: "))
                pole_dict[number]()
            except TypeError:  # Other than int
                os.system('cls' if os.name == 'nt' else 'clear')
                print(self.colors.YELLOW + "Invalid input, please enter again", + self.colors.ENDC)
            #          self.mmenu_main_print()
            except KeyError:  # number lower than 1 or bigger than numbers[-1]
                os.system('cls' if os.name == 'nt' else 'clear')
                print(
                    self.colors.YELLOW + f"Invalid number, enter a number between {numbers[0]} and {numbers[-1]}" + self.colors.ENDC)
            #         self.mmenu_main_print()
            except ValueError:  # Nothing inserted
                os.system('cls' if os.name == 'nt' else 'clear')
                print(self.colors.YELLOW + "Invalid input, please enter again" + self.colors.ENDC)
            #        self.mmenu_main_print()
            else:
                return

    def pole_main_print(self):
        print(" [ 1 ] : Pole - win relation bar graph ")
        print(" [ 2 ] : Export data to .csv (WIP) ")
        print(" [ 3 ] : See drivers' stats (WIP) " )


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
                else:
                    return
            except TypeError:     #=/= int
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Invalid input, please enter again")
                self.select_years_main_print()
#            except KeyError:
 #               os.system('cls' if os.name == 'nt' else 'clear')
  #              print("Invalid number, enter 1 or 2")
   #             self.select_years_main_print()
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
        self.select_years_choice_print(number)
        while not stop:
            try:
                if number != 2:     #2 = single year
                    self.start_year = int(input("Enter start year (or 0 to go back) :"))
                else:
                    self.start_year = int(input("Enter the year you want to scrape (or 0 to go back) : "))
                if self.start_year == 0:    #User goes back
                    self.start_year = tmp
                    return
                self.year_is_correct(self.start_year)
            except TypeError:
       #         os.system('cls' if os.name == 'nt' else 'clear')
                print(self.colors.YELLOW + f"Enter an year between 1950 and {LAST_YEAR}" + self.colors.ENDC)
            except InvalidYear:
        #        os.system('cls' if os.name == 'nt' else 'clear')
                print(self.colors.YELLOW + f"Enter an year between 1950 and {LAST_YEAR}" + self.colors.ENDC)
            except ValueError:
       #         os.system('cls' if os.name == 'nt' else 'clear')
                print(self.colors.YELLOW + f"Enter an year between 1950 and {LAST_YEAR}" + self.colors.ENDC)
            else:
                if number == 2:     #Single year
                    os.system('cls' if os.name == 'nt' else 'clear')
                    self.single_year = True
                    self.end_year = self.start_year
                    stop = True
                else:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    stop = self.select_years_main_case2()   #Check if user wants to change start year before stopping loop
                    if stop:
                        if self.start_year > self.end_year: #Check if years are sorted to avoid problems
                            self.start_year, self.end_year = self.end_year, self.start_year

    def select_years_main_case2(self):
        tmp = self.end_year #Save end year in case user goes back
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

    def select_years_main_print(self):
        print("Do you wish to select more years or 1 year? \n")
        print(" [ 1 ] : Multiple years \n")
        print(" [ 2 ] : Single year \n")
        print(" [ 3 ] : Go back \n")

    def select_years_choice_print(self, number):
        printdict = {0: "[ 4 ] : Change year(s)",1:  "[ 1 ] : Multiple years", 2: "[ 2 ] : Single year"}
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