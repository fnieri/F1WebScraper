from scraper import *


class StandingsScraper(Scraper):
    def __init__(self, year):
        super().__init__(year)
        self.standings_table = None #Wikipedia years' standings table
        self.races = None
        self.race_names = []

    def _get_table(self):
        for table in range(2, len(self.tables)):
            #Not the most effective way but Italy and Monaco are always in a year
            if "ITA" in self.tables[table] or "MON" in self.tables[table] and "Driver" in self.tables[table]:
                self.standings_table = self.tables[table]
                break

    def _get_race_results(self):
        last_index = self.source_index()
        columns = self.standings_table.columns[2:last_index]
        self.races = np.empty([len(self.standings_table.columns[2:last_index]), (len(self.standings_table[columns[1]]))+ \
                               last_index], dtype=object)
        #races is an empty array of all races
        for array_row, column in enumerate(columns):  #Get race result
            for array_col, result in enumerate((self.standings_table[column])[:last_index]): #Place result in array
                self.races[array_row][array_col] = result

    def get_race_names(self):
        self.get_table()
        self.race_names = self.standings_table[self.source_index()]

    def source_index(self):
        race_or_source = self.standings_table.iloc[-1].tolist()
        # Check if source row is at the end of the table, this means that we won't need to scrape the last
        # two rows because they contain nothing of interest
        if "Source" in race_or_source[1]:
            last_index = -2
        else:
            last_index = -1
        return last_index

    def _load(self):
        self.get_table()
        self._get_race_results()

    @property
    def get_races(self):
        return self.races
