import matplotlib.pyplot as plt
import numpy as np
from ..sources.const import *
from ..sources.driver import *
from ..sources.year import *
import regex as re
from abc import ABCMeta, abstractmethod
import time


class Plotter(metaclass=ABCMeta):
    """Metaclass representing general Plotter"""
    def __init__(self, start_year=1950, end_year=LAST_YEAR):
        self.start = start_year
        self.end = end_year
        self.years = [i for i in range(self.start, self.end + 1)]
        self.races_names = []

    @abstractmethod
    def _F1plot(self, start, end):
        pass

    def F1plot(self, start, end):
        self._F1plot(start, end)

    @abstractmethod
    def _get_data(self, start, end):
        pass

    def get_data(self, start, end):
        self._get_data(start, end)

    @abstractmethod
    def _update(self, start, end):
        pass

    def update(self, start, end):
        self._update(start, end)
        self.years = [i for i in range(start, end + 1)]

