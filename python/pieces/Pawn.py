import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from .Piece import Piece

class Pawn(Piece):
    def __init__(self, side, x, y, id):
        super().__init__(side, x, y, id)
        self.begin_dirs = 4 if self.side else 0
        self.on_condition_dirs = [3, 5] if self.side else [1, 7]
        self.dirs[self.begin_dirs] = [self.unit_dirs[self.begin_dirs]]

    def possible_move(self, board):
        for _ in range(8):
            for dx, dy in self.dirs[_]:
                nx = self.x + dx
                ny = self.y + dy
                if 0 <= nx < 8 and 0 <= ny < 8:
                    if board[nx][ny] and board[nx][ny].side == self.side:
                        break
                    print(f'possible_move: {nx, ny}')
                    if board[nx][ny] and board[nx][ny].side != self.side:
                        break
        for _ in self.on_condition_dirs:
            dx, dy = self.unit_dirs[_]
            nx = self.x + dx
            ny = self.y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                if not board[nx][ny] or board[nx][ny].side == self.side:
                    continue
                print(f'possible_move: {nx, ny}')
# p = Pawn(0, 0, 0)
# p.possible_move()