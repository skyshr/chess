from pieces.Piece import Piece
from constants import ROOK
from Dir import Dir

class Rook(Piece):
    def __init__(self, side, x, y, id):
        super().__init__(side, x, y, id)
        for dir in [Dir.N, Dir.E, Dir.S, Dir.W]:
            ux, uy = self.unit_dirs[dir]
            self.dirs[dir] = [(i*ux, i*uy) for i in range(1, 8)]
        self.type = ROOK

# if __name__ == "__main__":
# r = Rook(0, 0, 0)
# r.possible_move()