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
        print(f"{type(self)}[{self.x}][{self.y}]: ")
        if self.pinned == turn:
            print("I'm pinned therefore can't move!!")
        self.possible_moves = []
        map[self.x][self.y] += 1
        for dx, dy in self.dirs:
            nx = self.x + dx
            ny = self.y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                map[nx][ny] += 1
                if self.pinned == turn:
                    continue
                elif board[nx][ny] and board[nx][ny].side == self.side:
                    continue
                else:
                    self.possible_moves.append((nx, ny))
        print(f'possible_moves: {self.possible_moves}')

# k = Knight(0, 0, 0)
# k.possible_move()