class Year:
    """
    Class used to store Pole
    """
    def __init__(self, year):
        self.sitter_winner = []
        self.races = []
        self.year = year
        self.pole_win_prob = 0

    def set_prob(self, prob):
        self.pole_win_prob = prob

    def add_race(self, race, sitter, winner):
        self.sitter_winner.append({"Race" : race, "Pole sitter" : sitter, "Winner" : winner})

    def __str__(self):
        string = ["RACE      POLE SITTER      WINNER"]
        for race_no in range(len(self.sitter_winner)):
            string.append(f"{self.sitter_winner[race_no]['Race']} - {self.sitter_winner[race_no]['Pole sitter']}, "
                          f"{self.sitter_winner[race_no]['Winner']}")
        string.append(f"Pole to win chance -> {self.pole_win_prob}")
        return "\n".join(string)
