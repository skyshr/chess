import itertools
from pieces.Piece import Piece
from constants import KNIGHT, ROW, COL
from Dir import Dir

class Knight(Piece):
    def __init__(self, side, x, y, id):
        super().__init__(side, x, y, id)
        self.dirs = {
            Dir.KN_NNE: (-2, 1),
            Dir.KN_NEE: (-1, 2),
            Dir.KN_SEE: (1, 2),
            Dir.KN_SSE: (2, 1),
            Dir.KN_SSW: (2, -1),
            Dir.KN_SWW: (1, -2),
            Dir.KN_NWW: (-1, -2),
            Dir.KN_NNW: (-2, -1),
        }
        self.type = KNIGHT

    def draw_attack_paths(self, board, my_attack_path_map):
        for dir, dir_vec in self.dirs.items():
            dx, dy = dir_vec
            nx = self.x + dx
            ny = self.y + dy
            if 0 <= nx < ROW and 0 <= ny < COL:
                my_attack_path_map[nx][ny] += 1
                piece = board[nx][ny]
                if piece and piece.side != self.side and piece.is_king: 
                    piece.attacked_dirs[dir] = 1

    def possible_move(self, board, map, turn=-1):
        print(f"\n{type(self)}[{self.x}][{self.y}]: ")
        if self.pinned == turn:
            print("I'm pinned therefore can't move!!")
        self.possible_moves = []
        for dx, dy in self.dirs.values():
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

# if __name__ == "__main__":
    # k = Knight(0, 0, 0)
    # k.possible_move()