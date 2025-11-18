import sys
import os
import pieces

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from .Piece import Piece

class Pawn(Piece):
    def __init__(self, side, x, y, id):
        super().__init__(side, x, y, id)
        self.begin_dirs = 4 if self.side else 0
        self.on_condition_dirs = [3, 5] if self.side else [1, 7]
        self.dirs[self.begin_dirs] = [self.unit_dirs[self.begin_dirs]]
        self.moved_two_squares = False
        self.moved_two_squares_turn = -1
        self.enpassant = None

    def move_piece(self, board, to_x, to_y):
        try: 
            cur_x, cur_y = self.get_current_position()
            if board[to_x][to_y]:
                board[to_x][to_y].eliminated = True
            elif self.enpassant and cur_y != to_y:
                ex, ey = self.enpassant.get_current_position()
                board[ex][ey].eliminated = True
                board[ex][ey] = 0
            board[to_x][to_y] = self
            board[cur_x][cur_y] = 0
            self.x = to_x
            self.y = to_y
        except Exception as e: 
            print(f"Move Piece Error: {e}")

    def possible_move(self, board, map, turn):
        print(f"\n\n{type(self)}[{self.x}][{self.y}]: ")
        if self.pinned == turn:
            print("I'm pinned therefore can't move!!")
        self.possible_moves = []
        self.enpassant = None
        map[self.x][self.y] += 1
        if self.pinned != turn:
            for _ in range(8):
                for dx, dy in self.dirs[_]:
                    nx = self.x + dx
                    ny = self.y + dy
                    if 0 <= nx < 8 and 0 <= ny < 8:
                        if board[nx][ny] and board[nx][ny].side == self.side:
                            break
                        self.possible_moves.append((nx, ny))
                        if _ == self.begin_dirs and not self.has_moved and not board[nx][ny]:
                            nx += dx
                            ny += dy
                            if 0 <= nx < 8 and 0 <= ny < 8 and not board[nx][ny]:
                                self.possible_moves.append((nx, ny))
        for _ in self.on_condition_dirs:
            dx, dy = self.unit_dirs[_]
            nx = self.x + dx
            ny = self.y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                map[nx][ny] += 1
                if self.pinned == turn:
                    continue
                elif not board[nx][ny]:
                    ex = self.x
                    ey = ny
                    piece = board[ex][ey]
                    if piece and piece.side != self.side and isinstance(piece, pieces.Pawn):
                        # enpassant
                        if turn == piece.moved_two_squares_turn + 1:
                            self.enpassant = piece
                            self.possible_moves.append((nx, ny))
                            print(f'on condition possible_move(enpassant): {nx, ny}')
                elif board[nx][ny].side == self.side:
                    continue
                else:
                    self.possible_moves.append((nx, ny))
                    print(f'on condition possible_move: {nx, ny}')
        print(f'possible_moves: {self.possible_moves}')


# p = Pawn(0, 0, 0)
# p.possible_move()