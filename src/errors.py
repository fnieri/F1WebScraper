import datetime


class InvalidYear(Exception):
    def __init__(self, year):
        self.year = year

    def __str__(self):
        return f"{self.year} is not a valid year, enter an year between 1950 and {datetime.datetime.now().year - 1}"
