# dirs 
# 0: north
# 1: north-west
# 2: west
# 3: south-west
# 4: south
# 5: south-east
# 6: east
# 7: north-east
from python import King

class BoardOccupiedError(Exception):
    pass

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
        self.last_move_num = -1
        self.pinned = -2

    def set_piece(self, board, to_x, to_y):
        try: 
            if board[to_x][to_y]:
                raise BoardOccupiedError(f"Board[{to_x}][{to_y}] is Already Occuied!")
            board[to_x][to_y] = self
            self.x = to_x
            self.y = to_y
        except Exception as e: 
            print(f"Set Piece Error: {e}")

    def move_piece(self, board, to_x, to_y):
        try: 
            cur_x, cur_y = self.get_current_position()
            if board[to_x][to_y]:
                board[to_x][to_y].eliminated = True
            board[to_x][to_y] = self
            board[cur_x][cur_y] = 0
            self.x = to_x
            self.y = to_y
        except Exception as e: 
            print(f"Move Piece Error: {e}")

    def possible_move(self, board, map, turn=-1):
        print(f"\n\n{type(self)}[{self.x}][{self.y}]: ")
        if self.pinned == turn:
            print("I'm pinned therefore can't move!!")
        self.possible_moves = []
        map[self.x][self.y] += 1
        for _ in range(8):
            for dx, dy in self.dirs[_]:
                nx = self.x + dx
                ny = self.y + dy
                if 0 <= nx < 8 and 0 <= ny < 8:
                    map[nx][ny] += 1
                    if board[nx][ny] and board[nx][ny].side == self.side:
                        break
                    if self.pinned != turn:
                        self.possible_moves.append((nx, ny))
                    if board[nx][ny] and board[nx][ny].side != self.side:
                        kx, ky = nx, ny
                        instance = board[kx][ky]
                        if isinstance(instance, King):
                            break
                        while True:
                            kx += dx
                            ky += dy
                            if kx < 0 or kx >= 8 or ky < 0 or ky >= 8:
                                break
                            if board[kx][ky]:
                                if board[kx][ky].side != self.side and isinstance(board[kx][ky], King):
                                    board[kx][ky].pinned = turn
                                break
                        break
        print(f'possible_moves: {self.possible_moves}')

    def get_current_position(self):
        return [self.x, self.y]

    def reset_possible_moves(self):
        self.possible_moves = []

    def filter_possible_moves(self, possible_squares):
        self.possible_moves = [move for move in self.possible_moves if move in possible_squares]