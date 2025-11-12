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
        self.on_condition_moves = []
        self.moved_two_squares = False
        self.enpassant = None

    def possible_move(self, board, map):
        print(f"\n\n{type(self)}[{self.x}][{self.y}]: \n\n")
        self.possible_moves = []
        self.on_condition_moves = []
        for _ in range(8):
            for dx, dy in self.dirs[_]:
                nx = self.x + dx
                ny = self.y + dy
                if 0 <= nx < 8 and 0 <= ny < 8:
                    if board[nx][ny] and board[nx][ny].side == self.side:
                        break
                    print(f'possible_move: {nx, ny}')
                    self.possible_moves.append((nx, ny))
                    if _ == self.begin_dirs and not self.has_moved and not board[nx][ny]:
                        nx += dx
                        ny += dy
                        if 0 <= nx < 8 and 0 <= ny < 8 and not board[nx][ny]:
                            self.possible_moves.append((nx, ny))
        for _ in self.on_condition_dirs:
            dx, dy = self.unit_dirs[_]
            nx = self.x + dx
            ny = self.y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                map[nx][ny] += 1
                if not board[nx][ny]:
                    pass
                elif board[nx][ny].side == self.side:
                    continue
                else:
                    self.on_condition_moves.append((nx, ny))
                print(f'on condition possible_move: {nx, ny}')


# p = Pawn(0, 0, 0)
# p.possible_move()