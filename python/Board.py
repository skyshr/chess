from turtle import update
from Player import WHITE, Player
from pieces import *
import random

import pieces

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

# state
# 0: Before Match
# 1: Match Complete
# 2: In Game
# 3: END

STATE_BEFORE_MATCH = 0
STATE_MATCH_COMPLETE = 1
STATE_IN_GAME = 2
STATE_END = 3

global row, col
row = col = 8
class Board:
    game_number = 0

    def __init__(self, playerA, playerB):
        global row, col
        self.game_number = Board.game_number
        self.state = STATE_BEFORE_MATCH
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
        self.whiteAttackPath = [[0]*row for _ in range(col)]
        self.blackAttackPath = [[0]*row for _ in range(col)]
        side = random.randint(0, 1)
        self.playerA.register_side(side, self.board)
        self.playerB.register_side(side + 1, self.board)
        self.state = STATE_MATCH_COMPLETE
        Board.game_number += 1


    def print_board(self):
        print(f'{self.playerA.name}, {self.playerB.name} is about to play game {self.game_number}...')
        print('\n\nboard: ')
        for row in self.board:
            print(row)

    def start_game(self):
        print(f'Game {self.game_number} has started! {'White' if self.turn == 0 else 'Black'}s Move...')
        self.state = STATE_IN_GAME
        self.set_attack_path()
        self.playerA.move(self)
        self.update_attack_path()
        self.playerB.move(self)
        self.update_attack_path()

    def set_attack_path(self):
        global row, col
        for x in range(row):
            for y in range(col):
                piece = self.board[x][y]
                if not piece: continue
                if piece.side == WHITE:
                    piece.possible_move(self.board, self.whiteAttackPath)
                else:
                    piece.possible_move(self.board, self.blackAttackPath)
        print(f'\n\nBLACK ATTACK_PATH\n')
        for _row in self.blackAttackPath:
            print(_row)
        print(f'\n\nWHITE ATTACK_PATH\n')
        for _row in self.whiteAttackPath:
            print(_row)
    
    def update_attack_path(self):
        global row, col
        try:
            self.blackAttackPath = [[0] * row for _ in range(col)]
            self.whiteAttackPath = [[0] * row for _ in range(col)]
            self.set_attack_path()
        except Exception as e:
            print("Update Attack Path error!: ", e)


if __name__ == "__main__":
    board = Board(Player('sky'), Player('tom'))
    board.print_board()
    board.start_game()

    # board1 = Board(Player('sky1'), Player('tom1'))
    # board1.print_board()
