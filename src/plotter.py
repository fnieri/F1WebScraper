import matplotlib.pyplot as plt
from scraper import *
from const import *
import numpy as np
from driver import *
import regex as re
from abc import ABCMeta, abstractmethod


class Plotter(metaclass=ABCMeta):
    """Metaclass representing general Plotter"""
    def __init__(self, start_year = 1950, end_year = LAST_YEAR):
        self.start = start_year
        self.end = end_year
        self.years = [i for i in range(self.start, self.end + 1)]

    @abstractmethod
    def _F1plot(self):
        pass

    def F1plot(self):
        self._F1plot()

    @abstractmethod
    def _get_data(self):
        pass

    def get_data(self):
        self._get_data()


class PolePlotter(Plotter):
    """Class representing a Pole Plotter, plotting year - win mean for start_year - end_year"""
    def __init__(self, start_year = 1950, end_year = LAST_YEAR):
        super().__init__(start_year, end_year)
        self.prob = [0 for i in range(start_year, end_year+1)]
        self.drivers = {}

    def _get_data(self):
        """Get pole - win relation from start year to end year"""
        for iterator, pole_year in enumerate(range(self.start, self.end+1)):
            end_result = 0
            year = PoleScraper(pole_year)  #Scrape data from year
            year.load()     #Load year
            print(f"Scraping year {pole_year}", pole_year.url)
            pole_sitters, winners = year.pole_sitters_array, year.winners_array  #Get numpy arrays for sitters and winners
            for sitter, winner in zip(pole_sitters, winners):
                sitter, winner = re.sub("[\(\[].*?[\)\]]", "", sitter), re.sub("[\(\[].*?[\)\]]", "", winner)
                # Remove source brackets
                if sitter not in self.drivers:  #Add driver and/or winner if not in dictionary
                    self.drivers[sitter] = Driver(sitter)
                self.drivers[sitter].add_pole()
                self.drivers[sitter].add_year(pole_year)
                if winner not in self.drivers:
                    self.drivers[winner] = Driver(winner)
                self.drivers[winner].add_win()
                self.drivers[winner].add_year(pole_year)
                if sitter in winner:        #In the early days
                    end_result += 1
            this_year_prob = (end_result / pole_sitters.size) * 100
            self.prob[iterator] = this_year_prob    #Add probability of the year

    def _F1plot(self):
        """Bar plot for years and probability"""
        self.get_data()
        plt.bar(self.years, self.prob)
        plt.show()

    def show_drivers(self):
        for i in self.drivers:
            print(self.drivers[i])


class RetiredPlotter(Plotter):
    def __init__(self, start_year=1950, end_year=LAST_YEAR):
        super().__init__(start_year, end_year)
        self.retired = [0 for _ in range(self.start, self.end + 1)]
        self.ret_mean = [0 for _ in range(self.start, self.end + 1)]

    def _get_data(self):
        """Get retired data"""
        for iterator, year in enumerate(range(self.start, self.end + 1)):
            this_year_mean = []
            retired, retired_total, participants = 0, 0, 0
            year2scrape = StandingsScraper(year)
            year2scrape.load()
            print(f"Scraping year {year}", year2scrape.url)

            for race in year2scrape.races:
                for result in race:
                    if "RET" in str(result) or "Ret" in str(result):
                        retired += 1
                    if str(result) != "nan":    #Nan means driver didn't participate
                        participants += 1
                if participants != 0:   #In 2020 there are about 15 empty rows
                    this_race_percent = (retired/participants) * 100
                    this_year_mean.append(this_race_percent)
                    retired_total += retired
                retired, participants = 0, 0
            self.ret_mean[iterator] = sum(this_year_mean)/len(this_year_mean)
            self.retired[iterator] = retired_total

    def _F1plot(self):
        self.get_data()
       # plt.bar(self.years, self.retired)
        plt.bar(self.years, self.ret_mean)
        plt.show()


class DisqualifiedPlotter(Plotter):
    def __init__(self, start_year = 1950, end_year = LAST_YEAR):
        super().__init__(start_year, end_year)
        self.disqualified = [0 for i in range(start_year, end_year + 1)]

    def _get_data(self):
        for iterator, disq_year in enumerate(range(self.start, self.end + 1)):

            year = StandingsScraper(disq_year)  #Scrape data from year
            year.load()     #Load year values
            print(f"Scraping year {disq_year}", disq_year.url)
            disqualified = 0
            for races in year.races:    #Iterate over each race
                for race in races:
                    if "DSQ" in str(race) or str(race) == "DSQ":
                        disqualified += 1
            self.disqualified[iterator] = disqualified

    def _F1plot(self):
        self.get_data()
        plt.bar(self.years, self.disqualified)
        plt.show()


a = RetiredPlotter()
a.F1plot()
#b = PolePlotter()
#b.get_data()
#b.show_drivers()