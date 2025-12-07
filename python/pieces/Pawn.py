from pieces.Piece import Piece
from pieces import Pawn
from Dir import Dir
from constants import PAWN, WHITE, ROW, COL

TWO_SQUARES = 2

class Pawn(Piece):
    def __init__(self, side, x, y, id):
        super().__init__(side, x, y, id)
        self.begin_dirs = Dir.N if self.side == WHITE else Dir.S
        self.on_condition_dirs =  [Dir.NW, Dir.NE] if self.side == WHITE else [Dir.SW, Dir.SE]
        self.dirs = self.unit_dirs[self.begin_dirs]
        self.moved_two_squares = False
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
                left_y = cur_y - 1
                left_piece = board[to_x][left_y]
                if 0 < left_y < COL and left_piece and left_piece.side != self.side and left_piece.type == PAWN:
                    left_piece.enpassant = self
                right_y = cur_y + 1
                right_piece = board[to_x][right_y]
                if 0 < right_y < COL and right_piece and right_piece.side != self.side and right_piece.type == PAWN:
                    right_piece.enpassant = self

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
                elif self.enpassant:
                    self.possible_moves.append((nx, ny))

# if __name__ == "__main__":
# p = Pawn(0, 0, 0)
# p.possible_move()