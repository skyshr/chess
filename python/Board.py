from Player import Player
import random

global row, col
row = col = 8
class Board:
    game_number = 0

    def __init__(self, playerA, playerB):
        global row, col
        self.game_number = Board.game_number
        self.playerA = playerA
        self.playerB = playerB
        self.board = [[0] * col for _ in range(row)]
        self.turn = 0
        self.moves = []
        self.strength = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [-1, -2, -2, -2, -2, -2, -2, -1],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [1, 2, 2, 2, 2, 2, 2, 1],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ]

        side = random.randint(0, 1)
        self.playerA.register_side(side, self.board)
        self.playerB.register_side(side + 1, self.board)
        Board.game_number += 1


    def print_board(self):
        print(f'{self.playerA.name}, {self.playerB.name} is about to play game {self.game_number}...')
        print('\n\nboard: ')
        for row in self.board:
            print(row)

    def start_game(self):
        print(f'Game {self.game_number} has started! {'White' if self.turn == 0 else 'Black'}s Move...')
        self.playerA.move(self.board)

if __name__ == "__main__":
    board = Board(Player('sky'), Player('tom'))
    board.print_board()
    board.start_game()

    # board1 = Board(Player('sky1'), Player('tom1'))
    # board1.print_board()
