from sys import exception

WHITE = 0
BLACK = 1

class Player:
    def __init__(self, name):
        self.name = name

    def play_game(self):
        print(f'Player {self.name} finding game...')

    def register_side(self, side):
        try:
            side = side % 2
            self.side = side
            print(f"{self.name} is on {'BLACK' if side else 'WHITE'} side")
        except:
            print("Player register_side error!")
            

# A = Player('sky')
# A.play_game()