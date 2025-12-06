from pieces.Piece import Piece
from pieces import Pawn
from Dir import Dir
from constants import WHITE, ROW, COL

TWO_SQUARES = 2

class Pawn(Piece):
    def __init__(self, side, x, y, id):
        super().__init__(side, x, y, id)
        self.begin_dirs = Dir.N if self.side == WHITE else Dir.S
        self.on_condition_dirs =  [Dir.NW, Dir.NE] if self.side == WHITE else [Dir.SW, Dir.SE]
        self.dirs = self.unit_dirs[self.begin_dirs]
        self.moved_two_squares = False
        self.moved_two_squares_turn = -1
        self.enpassant = None
        self.promote = None

    def move_piece(self, board, to_x, to_y, turn):
        try: 
            cur_x, cur_y = self.get_current_position()
            if board[to_x][to_y]:
                board[to_x][to_y].eliminated = True
            elif self.enpassant and cur_y != to_y:
                ex, ey = self.enpassant.get_current_position()
                board[ex][ey].eliminated = True
                board[ex][ey] = 0
            if abs(cur_x - to_x) == TWO_SQUARES:
                self.moved_two_squares = True
                self.moved_two_squares_turn = turn
            board[to_x][to_y] = self
            board[cur_x][cur_y] = 0
            self.has_moved = True
            self.x = to_x
            self.y = to_y
        except Exception as e: 
            print(f"Move Piece Error: {e}")

    def draw_attack_paths(self, board, my_attack_path_map, turn):
        if self.eliminated: return
        self.possible_moves = []
        self.pinned = False
        self.enpassant = None

        # forward
        dx, dy = self.dirs
        nx = self.x + dx
        ny = self.y + dy
        if 0 <= nx < ROW and 0 <= ny < COL:
            if not board[nx][ny]:
                self.possible_moves.append((nx, ny))
        if not self.has_moved and not board[nx][ny]:
            nx += dx
            ny += dy
            if 0 <= nx < ROW and 0 <= ny < COL and not board[nx][ny]:
                self.possible_moves.append((nx, ny))
                
        # diagonal
        for dir in self.on_condition_dirs:
            dx, dy = self.unit_dirs[dir]
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
                            piece.attacked_squares.append([(self.x, self.y)])
                else:
                    ex = self.x
                    ey = ny
                    instance = board[ex][ey]
                    if instance and instance.side != self.side and instance.type == Pawn:
                        # enpassant
                        if turn == instance.moved_two_squares_turn + 1:
                            self.enpassant = instance
                            self.possible_moves.append((nx, ny))
                            print(f'on condition possible_move(enpassant): {nx, ny}')

# if __name__ == "__main__":
# p = Pawn(0, 0, 0)
# p.possible_move()