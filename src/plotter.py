import matplotlib.pyplot as plt
from scraper import *
from const import *
from scraper import *
import numpy as np
from driver import *
import regex as re
class Plotter:
    def __init__(self, start_year = 1950, end_year = LAST_YEAR):
        self.start = start_year
        self.end = end_year
        self.years = [i for i in range(self.start, self.end + 1)]   #List of years
        self.prob = [0 for i in range(start_year, end_year+1)]
        self.drivers = {}

    def get_pole(self):
        """
        Get pole - win relation from start year to end year
        """
        iterator = 0
        for i in range(self.start, self.end+1):
            end_result = 0
            year = Scraper(i)
            year.load_year_pole()
            pole_sitters, winners = year.pole_sitters, year.winners
            for sitter, winner in zip(pole_sitters, winners):
                sitter = re.sub("[\(\[].*?[\)\]]", "", sitter)
                winner = re.sub("[\(\[].*?[\)\]]", "", winner)
                if sitter not in self.drivers:
                    self.drivers[sitter] = Driver(sitter)
                self.drivers[sitter].add_pole()
                if winner not in self.drivers:
                    self.drivers[winner] = Driver(winner)
                self.drivers[winner].add_win()
                if sitter == winner:
                    end_result += 1
            this_year_prob = (end_result / pole_sitters.size) * 100
            self.prob[iterator] = this_year_prob
            iterator += 1

    def plot_poles(self):
        plt.bar(self.years, self.prob)
        plt.show()

    def show_drivers(self):
        for i in self.drivers:
            print(self.drivers[i])

a = Plotter()
a.get_pole()
a.plot_poles()
a.show_drivers()