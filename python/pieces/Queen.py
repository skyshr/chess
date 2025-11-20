from pieces.Piece import Piece
from constants import QUEEN

class Queen(Piece):
    def __init__(self, side, x, y, id):
        super().__init__(side, x, y, id)
        for dir, dir_vec in self.unit_dirs.items():
            ux, uy = dir_vec
            self.dirs[dir] = [(i*ux, i*uy) for i in range(1, 8)]  
        self.type = QUEEN

# if __name__ == "__main__":
# b = Queen(0, 0, 0)
# b.possible_move()