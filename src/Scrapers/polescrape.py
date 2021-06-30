from scraper import *


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
