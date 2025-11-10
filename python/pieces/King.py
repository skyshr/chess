import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from .Piece import Piece

class King(Piece):
    def __init__(self, side, x, y, id):
        super().__init__(side, x, y, id)
        for _ in range(8):
            self.dirs[_] = [self.unit_dirs[_]]
    def possible_move(self, board, map):
        print(f"\n\n{type(self)}[{self.x}][{self.y}]: \n\n")
        self.possible_moves = []
        for _ in range(8):
            for dx, dy in self.dirs[_]:
                nx = self.x + dx
                ny = self.y + dy
                if 0 <= nx < 8 and 0 <= ny < 8:
                    map[nx][ny] += 1
                    if board[nx][ny] and board[nx][ny].side == self.side:
                        continue
                    print(f'possible_move: {nx, ny}')
                    self.possible_moves.append((nx, ny))
# k = King(0, 0, 0)
# k.possible_move()