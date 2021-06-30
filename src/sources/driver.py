from functools import reduce


class Driver:
    def __init__(self, name):
        self.name = name
        self.poles = 0
        self.wins = 0
        self.years = []

    def add_pole(self):
        self.poles += 1

    def add_win(self):
        self.wins += 1

    def add_year(self, year):
        if year not in self.years:
            self.years.append(year)

    def __str__(self):
        s = reduce('{}{}-'.format, self.years, '-')
        return f"{self.name} has: \n" \
               f"{self.poles} Poles \n" \
               f"{self.wins} Wins \n" \
               f"in {s}"