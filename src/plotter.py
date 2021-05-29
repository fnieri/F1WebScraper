import matplotlib.pyplot as plt
from scraper import *
from const import *
from scraper import *
import numpy as np
class Plotter:
    def __init__(self, start_year = 1950, end_year = LAST_YEAR):
        self.start = start_year
        self.end = end_year
        self.years = [i for i in range(self.start, self.end + 1)]
        self.prob = [0 for i in range(start_year, end_year+1)]

    def get_results(self):
        for i in range(self.start, self.end):
            iterator = 0
            end_result = 0
            year = Scraper(i)
            print(i)
            year.load_year()
            year.get_pole()
            year.get_winners()
            pole_sitters = year.pole_sitters
            winners = year.winners

            for sitter, winner in zip(pole_sitters, winners):
                if sitter == winner:
                    end_result += 1

            this_year_prob = (end_result / pole_sitters.size) * 100
            self.prob[iterator] = this_year_prob
            iterator += 1

    def plot(self):
        plt.plot(self.years, self.prob, "r")

a = Plotter()
a.get_results()
a.plot()
