import sys
import os

from itertools import product

import pieces

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from .Piece import Piece

class King(Piece):
    def __init__(self, side, x, y, id):
        super().__init__(side, x, y, id)
        for _ in range(8):
            self.dirs[_] = [self.unit_dirs[_]]
        self.attacked_squares = []

    def possible_move(self, board, my_attack_map):
        print(f"\n\n{type(self)}[{self.x}][{self.y}]: \n\n")
        self.possible_moves = []
        for _ in range(8):
            for dx, dy in self.dirs[_]:
                nx = self.x + dx
                ny = self.y + dy
                if 0 <= nx < 8 and 0 <= ny < 8:
                    my_attack_map[nx][ny] += 1
                    if board[nx][ny] and board[nx][ny].side == self.side:
                        continue
                    print(f'possible_move: {nx, ny}')
                    self.possible_moves.append((nx, ny))

    def count_attack_dirs(self, board, opponent_attack_map):
        cnt = 0
        self.attacked_squares = []
        for _ in range(8):
            for dx, dy in self.dirs[_]:
                nx = self.x + dx
                ny = self.y + dy
                if 0 <= nx < 8 and 0 <= ny < 8:
                    if opponent_attack_map[nx][ny] and (not board[nx][ny] or board[nx][ny].side != self.side):
                        cnt += 1
                        self.possible_moves.remove((nx, ny))
                        self.attacked_squares.append((nx, ny))

        knight_dirs = [
            (x, y) 
            for a, b in [([-1, 1], [-2, 2]), ([-2, 2], [-1, 1])]
            for x, y in product(a, b)
        ]
        for dx, dy in knight_dirs:
            nx = self.x + dx
            ny = self.y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                piece = board[nx][ny]
                if not piece or piece.side == self.side or not isinstance(piece, pieces.Knight):
                    continue
                cnt += 1
                self.attacked_squares.append((nx, ny))
        return cnt
# k = King(0, 0, 0)
# k.possible_move()