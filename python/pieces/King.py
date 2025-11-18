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

    def possible_move(self, board, my_attack_map, turn=-1):
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

    def is_empty_square(self, board, opponent_attack_map, x, y):
        return not board[x][y] and not opponent_attack_map[x][y]

    def check_castling(self, board, opponent_attack_map):
        if self.has_moved: return
        cur_x, cur_y = self.get_current_position()
        # king side
        if self.is_empty_square(board, opponent_attack_map, cur_x, cur_y + 1) and self.is_empty_square(board, opponent_attack_map, cur_x, cur_y + 2) and
        board[cur_x][cur_y + 3] and not board[cur_x][cur_y + 3].has_moved:
            self.po

        king_side_rook = board[cur_x][cur_y + 3]
        # queen side


# k = King(0, 0, 0)
# k.possible_move()