class Year:
    """
    Class used to store Pole
    """
    def __init__(self, year):
        self.sitter_winner = {}
        self.races = []
        self.year = year
        self.pole_win_prob = 0

    def add_race(self, race, sitter, winner):
        self.sitter_winner[race] = [sitter, winner]

    def __str__(self):
         return
