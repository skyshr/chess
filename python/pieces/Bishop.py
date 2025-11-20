from constants import BISHOP
from pieces.Piece import Piece
from Dir import Dir

class Bishop(Piece):
    def __init__(self, side, x, y, id):
        super().__init__(side, x, y, id)
        for dir in [Dir.NE, Dir.SE, Dir.SW, Dir.NW]:
            ux, uy = self.unit_dirs[dir]
            self.dirs[dir] = [(i*ux, i*uy) for i in range(1, 8)]
        self.type = BISHOP

# if __name__ == "__main__":
# b = Bishop(0, 0, 0)
# b.possible_move()