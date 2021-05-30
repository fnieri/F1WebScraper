import pandas as pd
from urllib.request import urlopen
from .const import *
from .errors import *
import html5lib
import numpy as np
from abc import ABCMeta, abstractmethod


class Scraper(metaclass=ABCMeta):
    def __init__(self, year : int = 2020):
        self.year = year
        self.url = self.url_builder()
        self.table = pd.read_html(str(self.url))

    @abstractmethod
    def _get_table(self):
        pass

    def get_table(self):
        self._get_table()

    @abstractmethod
    def _load(self):
        pass

    def load(self):
        self._load()

    def url_builder(self):
        """
        Build url from given year if year is correct
        Returns:
            years' url
        """
        assert isinstance(self.year, int)
        year_correctness = self.year_is_correct()
        if not year_correctness:
            raise InvalidYear(self.year)
        if self.year > 1980:
            return 'https://en.wikipedia.org/wiki/' + str(self.year) + '_Formula_One_World_Championship'
        elif self.year < 1982:
            return 'https://en.wikipedia.org/wiki/' + str(self.year) + '_Formula_One_season'

    def year_is_correct(self):
        """Check if given year is correct"""
        return 1950 <= self.year <= LAST_YEAR


class PoleScraper(Scraper):
    def __init__(self, year : int = 1960):
        super().__init__(year)
        self.pole_table = None
        self.pole_sitters = None
        self.winners = None
        self.whatispole = "Pole position"
        self.whatiswinner = "Winning driver"

    def _get_table(self):
        """Get table from said year"""
        for i in range(1, len(self.table)):
            if "Pole position" in self.table[i] or "Pole Position" in self.table[i]:
                if "Pole position" in self.table[i]:
                    self.whatispole = "Pole position"
                else:
                    self.whatispole = "Pole Position"
                if "Winning driver" in self.table[i]:
                    self.whatiswinner = "Winning driver"
                else:
                    self.whatiswinner = "Winning Driver"
                self.pole_table = self.table[i]
                break

    def _get_pole(self):
        """Numpy array of pole sitters"""
        self.pole_sitters = self.pole_table[self.whatispole].to_numpy()

    def _get_winners(self):
        """Numpy array of winners"""
        self.winners = self.pole_table[self.whatiswinner].to_numpy()

    def _load(self):
        """Load this year's pole and winners"""
        self.get_table()
        self._get_pole()
        self._get_winners()


class StandingsScraper(Scraper):
    def __init__(self, year):
        super().__init__(year)
        self.standings_table = None
        self.races = None

    def _get_table(self):
        for i in range(2, len(self.table)):
            if "ITA" in self.table[i] or "MON" in self.table[i] and "Driver" in self.table[i]:
                self.standings_table = self.table[i]
                break

    def _get_race_results(self):
        columns = self.standings_table.columns[2:-1]
        self.races = np.empty([len(self.standings_table.columns[2:-1]), (len(self.standings_table[columns[1]]))], dtype=object)
        iter1 = 0
        for column in columns:
            iter2 = 0
            for j in self.standings_table[column]:
                self.races[iter1][iter2] = j
                iter2 += 1
            iter1 += 1

    def _load(self):
        self.get_table()
        self._get_race_results()

    @property
    def get_races(self):
        return self.races
