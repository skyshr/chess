from constants import PAWN, ROW, COL
from Dir import Dir

class BoardOccupiedError(Exception):
    pass

class Piece:
    def __init__(self, side, x, y, id):
        self.unit_dirs = {
            Dir.N: (-1, 0),
            Dir.NE: (-1, 1),
            Dir.E: (0, 1),
            Dir.SE: (1, 1),
            Dir.S: (1, 0),
            Dir.SW: (1, -1),
            Dir.W: (0, -1),
            Dir.NW: (-1, -1),
        }
        self.dirs = {i: [] for i in range(8)}
        self.side = side
        self.x = x
        self.y = y
        self.type = PAWN
        self._id = id
        self.has_moved = False
        self.eliminated = False
        self.possible_moves = []
        self.last_move_num = -1
        self.pinned = -2
        self.is_king = False

    # 수정 불가능하게 만들기 → property로 read-only 만들기
    @property
    def id(self):
        return self._id

    def set_piece(self, board, to_x, to_y):
        try: 
            if board[to_x][to_y]:
                raise BoardOccupiedError(f"Board[{to_x}][{to_y}] is Already Occuied!")
            board[to_x][to_y] = self
            self.x = to_x
            self.y = to_y
        except Exception as e: 
            print(f"Set Piece Error: {e}")

    def move_piece(self, board, to_x, to_y, turn):
        try: 
            self.has_moved = True
            cur_x, cur_y = self.get_current_position()
            if board[to_x][to_y]:
                board[to_x][to_y].eliminated = True
            board[to_x][to_y] = self
            board[cur_x][cur_y] = 0
            self.x = to_x
            self.y = to_y
            self.last_move_num = turn
        except Exception as e: 
            print(f"Move Piece Error: {e}")

    def draw_attack_paths(self, board, my_attack_path_map):
        for dir, dir_vecs in self.dirs.items():
            for dx, dy in dir_vecs:
                nx = self.x + dx
                ny = self.y + dy
                if 0 <= nx < ROW and 0 <= ny < COL:
                    my_attack_path_map[nx][ny] += 1
                    piece = board[nx][ny]
                    if piece:
                        if piece.side != self.side and piece.is_king: 
                                piece.attacked_dirs[dir] = 1
                        break

    def check_opponent_piece_pinned_status(self, board, my_attack_path_map):
        for dir, dir_vecs in self.dirs.items():
            for dx, dy in dir_vecs:
                nx = self.x + dx
                ny = self.y + dy
                if 0 <= nx < ROW and 0 <= ny < COL:g

    def possible_move(self, board, map, turn=-1):
        print(f"\n{type(self)}[{self.x}][{self.y}]: ")
        if self.pinned == turn:
            print("I'm pinned therefore can't move!!")
        self.possible_moves = []
        for dir in self.dirs:
            for dx, dy in self.dirs[dir]:
                nx = self.x + dx
                ny = self.y + dy
                if 0 <= nx < ROW and 0 <= ny < COL:
                    map[nx][ny] += 1
                    if board[nx][ny] and board[nx][ny].side == self.side:
                        break
                    if self.pinned != turn:
                        self.possible_moves.append((nx, ny))
                    if board[nx][ny] and board[nx][ny].side != self.side:
                        kx, ky = nx, ny
                        instance = board[kx][ky]
                        if instance.is_king:
                            count = max(dx, dy)
                            _dx, _dy = dx // count, dy // count
                            for i in range(count):
                                _kx -= kx - i * _dx
                                _ky -= ky - i * _dy
                                instance.attacked_squares.append((_kx, _ky))

                            instance.attacked_dirs[dir] = 1
                            break
                        while True:
                            kx += dx
                            ky += dy
                            if kx < 0 or kx >= ROW or ky < 0 or ky >= COL:
                                break
                            if board[kx][ky]:
                                if board[kx][ky].side != self.side and board[kx][ky].is_king:
                                    board[nx][ny].pinned = turn
                                break
                        break
        print(f'possible_moves: {self.possible_moves}')

    def get_current_position(self):
        return (self.x, self.y)

    def reset_possible_moves(self):
        self.possible_moves = []

    def filter_possible_moves(self, possible_squares):
        self.possible_moves = [move for move in self.possible_moves if move in possible_squares]

    def get_possible_moves(self):
        return self.possible_moves