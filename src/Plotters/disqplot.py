from plotter import *
from scrapers.standscrape import *

class DisqualifiedPlotter(Plotter):
    def __init__(self, start_year=1950, end_year=LAST_YEAR):
        super().__init__(start_year, end_year)
        self.disqualified = [0 for _ in range(start_year, end_year + 1)]

    def _get_data(self, start, end):
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

    def _F1plot(self, start, end):
        self.get_data(start, end)
        plt.bar(self.years, self.disqualified)
        plt.show()

    def _update(self, start, end):
        self.start = start
        self.end = end
        self.disqualified = [0 for _ in range(self.start, self.end + 1)]
