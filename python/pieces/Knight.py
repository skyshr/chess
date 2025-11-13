import itertools
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from .Piece import Piece

class Knight(Piece):
    def __init__(self, side, x, y, id):
        super().__init__(side, x, y, id)
        self.dirs = [
            (x, y) 
            for a, b in [([-1, 1], [-2, 2]), ([-2, 2], [-1, 1])]
            for x, y in itertools.product(a, b)
        ]
    def possible_move(self, board, map, turn=-1):
        print(f"{type(self)}[{self.x}][{self.y}]: \n\n")
        self.possible_moves = []
        for dx, dy in self.dirs:
            nx = self.x + dx
            ny = self.y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                map[nx][ny] += 1
                if board[nx][ny] and board[nx][ny].side == self.side:
                    continue
                print(f'possible_move: {nx, ny}')
                self.possible_moves.append((nx, ny))

# k = Knight(0, 0, 0)
# k.possible_move()