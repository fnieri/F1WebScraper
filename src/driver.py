class Driver:
    def __init__(self, name):
        self.name = name
        self.poles = 0
        self.wins = 0

    def add_pole(self):
        self.poles += 1

    def add_win(self):
        self.wins += 1

    def __str__(self):
        return f"{self.name} has: \n" \
               f"{self.poles} Poles \n" \
               f"{self.wins}  Wins"