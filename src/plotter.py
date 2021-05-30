import matplotlib.pyplot as plt
from .scraper import *
from .const import *
import numpy as np
from .driver import *
import regex as re
from abc import ABCMeta, abstractmethod


class Plotter(metaclass=ABCMeta):
    def __init__(self, start_year = 1950, end_year = LAST_YEAR):
        self.start = start_year
        self.end = end_year
        self.years = [i for i in range(self.start, self.end + 1)]

    @abstractmethod
    def _F1plot(self):
        pass

    def F1plot(self):
        self._F1plot()


class PolePlotter(Plotter):
    def __init__(self, start_year = 1950, end_year = LAST_YEAR):
        super().__init__(start_year, end_year)
        self.prob = [0 for i in range(start_year, end_year+1)]
        self.drivers = {}

    def get_pole(self):
        """
        Get pole - win relation from start year to end year
        """
        iterator = 0
        for i in range(self.start, self.end+1):
            end_result = 0
            year = PoleScraper(i)
            year.load()
            pole_sitters, winners = year.pole_sitters, year.winners
            for sitter, winner in zip(pole_sitters, winners):
                sitter, winner = re.sub("[\(\[].*?[\)\]]", "", sitter), re.sub("[\(\[].*?[\)\]]", "", winner)
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

    def _F1plot(self):
        plt.bar(self.years, self.prob)
        plt.show()

    def show_drivers(self):
        for i in self.drivers:
            print(self.drivers[i])


class RetiredPlotter(Plotter):
    def __init__(self, start_year=1950, end_year=LAST_YEAR):
        super().__init__(start_year, end_year)
        self.retired = [0 for i in range(start_year, end_year + 1)]

    def get_retired(self):
        iterator = 0
        for i in range(self.start, self.end + 1):
            year = StandingsScraper(i)
            year.load()
            retired = 0
            for j in year.races:
                for k in j:
                    print(k)
                    if k == "RET" or k == "Ret":
                        retired += 1
            self.retired[iterator] = retired
            iterator += 1

    def _F1plot(self):
        plt.bar(self.years, self.retired)
        plt.show()


class DisqualifiedPlotter(Plotter):
    def __init__(self, start_year = 1950, end_year = LAST_YEAR):
        super().__init__(start_year, end_year)
        self.disqualified = [0 for i in range(start_year, end_year + 1)]

    def get_disqualified(self):
        iterator = 0
        for i in range(self.start, self.end + 1):
            year = StandingsScraper(i)
            year.load()
            disqualified = 0
            for j in year.races:
                for k in j:
                    if k == "DSQ":
                        disqualified += 1
            self.disqualified[iterator] = disqualified
            iterator += 1

    def _F1plot(self):
        plt.bar(self.years, self.disqualified)
        plt.show()
