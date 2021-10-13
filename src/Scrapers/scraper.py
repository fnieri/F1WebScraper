import pandas as pd
from urllib.request import urlopen
from ..sources.const import *
from ..sources.errors import *
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

