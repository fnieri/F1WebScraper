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
        self.tables = pd.read_html(str(self.url))       #All the tables in year

    @abstractmethod
    def _get_table(self):
        """Load each year's required table"""
        pass

    def get_table(self):
        self._get_table()

    @abstractmethod
    def _load(self):
        """Load year"""
        pass

    def load(self):
        self._load()

    def url_builder(self):
        """
        Build url from given year if year is correct
        Returns:
            (str) : years' url
        """
        assert isinstance(self.year, int)
        year_correctness = self.year_is_correct()
        if not year_correctness:
            raise InvalidYear(self.year)
        if self.year > 1980:
            return 'https://en.wikipedia.org/wiki/' + str(self.year) + '_Formula_One_World_Championship'
        return 'https://en.wikipedia.org/wiki/' + str(self.year) + '_Formula_One_season'

    def year_is_correct(self):
        """Check if given year is correct"""
        return 1950 <= self.year <= LAST_YEAR


class PoleScraper(Scraper):
    """Class used for scraping pole-win mean"""
    def __init__(self, year: int = 1960):
        super().__init__(year)
        self.pole_table = None  #Wikipedia race table
        self.pole_sitters_array = None    #Numpy Array containing pole sitters
        self.winners_array = None     #Numpy array containing winners
        self.pole = "Pole position"   #Pole position name may differ from year to year
        self.winner = "Winning driver"    #As does Winning driver

    def _get_table(self):
        """Get table from said year"""
        for column in range(1, len(self.tables)):     #Go through each table until Pole position is in it
            if "Pole position" in self.tables[column] or "Pole Position" in self.tables[column]:
                self.pole = "Pole position" if "Pole position" in self.tables[column] else "Pole Position"
                self.winner = "Winning driver" if "Winning driver" in self.tables[column] else "Winning Driver"
                self.pole_table = self.tables[column]
                break

    def _get_pole(self):
        """Numpy array of pole sitters"""
        #Put pole sitters in pole position column in numpy array
        self.pole_sitters_array = self.pole_table[self.pole].to_numpy()

    def _get_winners(self):
        """Numpy array of winners"""
        # Put winners in wiiners' column in numpy array
        self.winners_array = self.pole_table[self.winner].to_numpy()

    def _load(self):
        """Load this year's pole and winners"""
        self.get_table()
        self._get_pole()
        self._get_winners()


class StandingsScraper(Scraper):
    def __init__(self, year):
        super().__init__(year)
        self.standings_table = None #Wikipedia years' standings table
        self.races = None

    def _get_table(self):
        for table in range(2, len(self.tables)):
            #Not the most effective way but Italy and Monaco are always in a year
            if "ITA" in self.tables[table] or "MON" in self.tables[table] and "Driver" in self.tables[table]:
                self.standings_table = self.tables[table]
                break

    def _get_race_results(self):
        race_or_source = self.standings_table.iloc[-1].tolist()
        if "Source" in race_or_source[1]:
            #Check if source row is at the end of the table, this means that we won't need to scrape the last
            #two rows because they contain nothing of interest
            last_index = -2
        else:
            last_index = -1
        columns = self.standings_table.columns[2:last_index]
        self.races = np.empty([len(self.standings_table.columns[2:last_index]), (len(self.standings_table[columns[1]]))+ \
                               last_index], dtype=object)
        #races is an empty array of all races
        for array_row, column in enumerate(columns):  #Get race result
            for array_col, result in enumerate((self.standings_table[column])[:last_index]): #Place result in array
                self.races[array_row][array_col] = result

    def _load(self):
        self.get_table()
        self._get_race_results()

    @property
    def get_races(self):
        return self.races

class WinnerScraper(Scraper):
    pass

class DN_S_QScraper(Scraper):
    pass