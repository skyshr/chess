from Player import Player
import random

class Board:
    game_number = 0

    def __init__(self, playerA, playerB):
        self.game_number = Board.game_number
        self.playerA = playerA
        self.playerB = playerB

        side = random.randint(0, 1)
        self.playerA.register_side(side)
        self.playerB.register_side(side + 1)
        Board.game_number += 1

    def print_board(self):
        print(f'{self.playerA.name}, {self.playerB.name} is about to play game {self.game_number}...')

if __name__ == "__main__":
    board = Board(Player('sky'), Player('tom'))
    board.print_board()

    board1 = Board(Player('sky1'), Player('tom1'))
    board1.print_board()
