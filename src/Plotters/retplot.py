from plotter import *
from scrapers.polescrape import *
from scrapers.standscrape import *


class RetiredPlotter(Plotter):
    def __init__(self, start_year=1950, end_year=LAST_YEAR):
        super().__init__(start_year, end_year)
        self.retired = [0 for _ in range(self.start, self.end + 1)]
        self.ret_mean = [0 for _ in range(self.start, self.end + 1)]

    def _get_data(self, start, end):
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

    def _F1plot(self, start, end):
        self.get_data(start, end)
        # plt.bar(self.years, self.retired)
        plt.bar(self.years, self.ret_mean)
        plt.show()

    def _update(self, start, end):
        self.start = start
        self.end = end
        self.retired = [0 for _ in range(self.start, self.end + 1)]
        self.ret_mean = [0 for _ in range(self.start, self.end + 1)]

