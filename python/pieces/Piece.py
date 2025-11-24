from constants import KING, KNIGHT, PAWN, ROW, COL
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

    def draw_attack_paths(self, board, my_attack_path_map, turn):
        self.possible_moves = []

        for dir, dir_vecs in self.dirs.items():
            for dx, dy in dir_vecs:
                nx = self.x + dx
                ny = self.y + dy
                if 0 <= nx < ROW and 0 <= ny < COL:
                    my_attack_path_map[nx][ny] += 1
                    piece = board[nx][ny]
                    if piece:
                        if piece.side != self.side:
                            self.possible_moves.append((nx, ny))
                            if piece.is_king:
                                piece.attacked_dirs[dir] = 1
                        break
                    else:
                        self.possible_moves.append((nx, ny))

    def check_opponent_piece_pinned_status(self, board, turn):
        if self.type in [PAWN, KING, KNIGHT]: return
        if self.eliminated: return
        for dir_vecs in self.dirs.values():
            for dx, dy in dir_vecs:
                nx = self.x + dx
                ny = self.y + dy
                if 0 <= nx < ROW and 0 <= ny < COL:
                    piece = board[nx][ny]
                    if piece:
                        if piece.side == self.side:
                            break
                        if piece.is_king:
                            ps = []
                            _dx = dx // abs(dx) if dx else 0
                            _dy = dy // abs(dy) if dy else 0
                            while nx != self.x or ny != self.y:
                                nx -= _dx
                                ny -= _dy
                                ps.append((nx, ny))
                            piece.attacked_squares.append(ps)
                            break
                        ps = [(nx, ny)]
                        while True:
                            nx += dx
                            ny += dy
                            if nx < 0 or nx >= ROW or ny < 0 or ny >= COL:
                                break
                            ps.append((nx, ny))
                            instance = board[nx][ny]
                            if instance and instance.side != self.side and instance.is_king:
                                piece.pinned = turn
                                instance.attacked_squares.append(ps)
                                break
                        break

    def possible_move(self, status, turn, squares):
        if self.pinned == turn:
            self.possible_moves = []
            return
        # check in two directions
        if status == 2:
            self.possible_moves = []
            return
        # check
        if status == 1:
            self.filter_possible_moves(squares)

    def get_current_position(self):
        return (self.x, self.y)

    def filter_possible_moves(self, possible_squares):
        self.possible_moves = [move for move in self.possible_moves if move in possible_squares]

    def get_possible_moves(self):
        return self.possible_moves