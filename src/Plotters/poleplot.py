from plotter import *
from scrapers.polescrape import *
from scrapers.standscrape import *

class PolePlotter(Plotter):
    """Class representing a Pole Plotter, plotting year - win mean for start_year - end_year"""
    def __init__(self, start_year=1950, end_year=LAST_YEAR):
        super().__init__(start_year, end_year)
        self.prob = [0 for i in range(start_year, end_year+1)]
        self.drivers = {}
        self.years_dict = {}
        self.ran_once = {}
        self.run_once()

    def run_once(self):
        for year in range(1950, 2020):
            self.ran_once[year] = False

    def get_year_data(self, year):
        assert isinstance(year, int)
        assert 1950 <= year <= LAST_YEAR
        print(self.ran_once[year])
        if self.ran_once[year]:
            return self.years_dict[year]
        self.get_data(year, year)
        return self.years_dict[year]

    def _get_data(self, start, end):
        """Get pole - win relation from start year to end year"""
        for iterator, pole_year in enumerate(range(start, end+1)):
            end_result = 0
            year = PoleScraper(pole_year)  #Scrape data from year
            races_names = StandingsScraper(pole_year).get_race_names()
            year.load()     #Load year
            self.ran_once[pole_year] = True
            year_class = Year(pole_year)
            print(f"Scraping year {pole_year}", year.url)
            pole_sitters, winners = year.pole_sitters_array, year.winners_array  #Get numpy arrays for sitters and winners
            for race_no, sitter, winner in enumerate(zip(pole_sitters, winners)):
                end_result += self._check_sitter_winner(sitter, winner, year)
                year_class.add_race(races_names[race_no], sitter, winner)
            year_class.races = races_names
            this_year_prob = (end_result / pole_sitters.size) * 100
            self.prob[iterator] = this_year_prob    #Add probability of the year
            self.years_dict[pole_year] = year_class

    def _check_sitter_winner(self, sitter, winner, year):
        end_res = 0
        sitter, winner = re.sub("[\(\[].*?[\)\]]", "", sitter), re.sub("[\(\[].*?[\)\]]", "", winner)
        # Remove source brackets
        if sitter not in self.drivers:  # Add driver and/or winner if not in dictionary
            self.drivers[sitter] = Driver(sitter)
        self.drivers[sitter].add_pole()
        self.drivers[sitter].add_year(year)
        if winner not in self.drivers:
            self.drivers[winner] = Driver(winner)
        self.drivers[winner].add_win()
        self.drivers[winner].add_year(year)
        if sitter in winner:  # In the early days
            end_res += 1
        return end_res

    def _F1plot(self, start, end):
        """Bar plot for years and probability"""
        self.get_data(start, end)
        plt.bar(self.years, self.prob)
        plt.show()

    def show_drivers(self):
        for i in self.drivers:
            print(self.drivers[i])

    def _update(self, start, end):
        self.start = start
        self.end = end
        self.prob = [0 for i in range(self.start, self.end + 1)]
