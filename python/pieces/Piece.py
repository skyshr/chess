# dirs 
# 0: north
# 1: north-west
# 2: west
# 3: south-west
# 4: south
# 5: south-east
# 6: east
# 7: north-east

class Piece:
    def __init__(self, side, x, y, id):
        self.unit_dirs = {
            0: (-1, 0),
            1: (-1, -1),
            2: (0, -1),
            3: (1, -1),
            4: (1, 0),
            5: (1, 1),
            6: (0, 1),
            7: (-1, 1),
        }
        self.dirs = {i: [] for i in range(8)}
        self.side = side
        self.x = x
        self.y = y
        self.id = id
        self.has_moved = False
        self.eliminated = False
        self.possible_moves = []

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
                        break
                    print(f'possible_move: {nx, ny}')
                    self.possible_moves.append((nx, ny))
                    if board[nx][ny] and board[nx][ny].side != self.side:
                        break