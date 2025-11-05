from Player import Player
from pieces import *
import random

# 0: White, 1: Black
# 0: Rook, 1: Knight, 2: Bishop, 3: Queen, 4: King, 5: Bishop, 6: Knight, 7: Pawn

# 중심 3을 기준으로 side만큼 보정
piece_coords_x = {
    'Rook': [0, 7],
    'Knight': [1, 6],
    'Bishop': [2, 5],
    'Queen': [3],
    'King': [4],
    'Pawn': [0, 1, 2, 3, 4, 5, 6, 7],
}

# Board coordinates:
# [x][y]
# x => 0: A, 1: B, 2: C, 3: D, 4: E, 5: F, 6: G, 7: H
# y => 0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8

class Board:
    game_number = 0

    def __init__(self, playerA, playerB):
        self.game_number = Board.game_number
        self.playerA = playerA
        self.playerB = playerB
        self.board = [[None for _ in range(8)] for _ in range(8)]

        self.board[0][0] = Rook(0, 0, 0)
        self.board[0][1] = Knight(0, 1, 0)
        self.board[0][2] = Bishop(0, 2, 0)
        self.board[0][3] = Queen(0, 3, 0)
        self.board[0][4] = King(0, 4, 0)
        self.board[0][5] = Bishop(0, 5, 0)
        self.board[0][6] = Knight(0, 6, 0)
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
