from pieces.Piece import Piece
from constants import KING

class King(Piece):
    def __init__(self, side, x, y, id):
        super().__init__(side, x, y, id)
        for dir, dir_vec in self.unit_dirs.items():
            self.dirs[dir] = [dir_vec]
        self.attacked_squares = []
        self.is_king = True
        self.attacked_dirs = [0] * 16
        self.type = KING

    def get_attacked_dirs_count(self):
        return sum(self.attacked_dirs)

    def get_attacked_squares(self):
        return self.attacked_squares

    def reset_squares(self):
        self.attacked_squares = []
        self.attacked_dirs = [0] * 16

    def delete_attacked_squares(self, opponent_attack_map):
        self.possible_moves = [(x, y) for (x, y) in self.possible_moves if not opponent_attack_map[x][y]]

    def is_empty_square(self, board, x, from_y, to_y):
        for y in range(from_y, to_y):
            if board[x][y]:
                return False
        return True

    def is_safe_square(self, opponent_attack_map, x, from_y, to_y):
        for y in range(from_y, to_y + 1):
            if opponent_attack_map[x][y]:
                return False
        return True

    def check_castling(self, board, opponent_attack_map):
        if self.has_moved: return
        cur_x, cur_y = self.get_current_position()
        # king side
        king_side_rook = board[cur_x][cur_y + 3]
        if king_side_rook and not king_side_rook.has_moved:
            if self.is_empty_square(board, cur_x, cur_y + 1, cur_y + 3) and self.is_safe_square(opponent_attack_map, cur_x, cur_y, cur_y + 3):
                self.possible_moves.append((cur_x, cur_y + 2))
        # queen side
        queen_side_rook = board[cur_x][cur_y - 4]
        if queen_side_rook and not queen_side_rook.has_moved:
            if self.is_empty_square(board, cur_x, cur_y - 3, cur_y) and self.is_safe_square(opponent_attack_map, cur_x, cur_y - 4, cur_y):
                self.possible_moves.append((cur_x, cur_y - 2))

    def move_piece(self, board, to_x, to_y, turn):
        try: 
            self.has_moved = True
            cur_x, cur_y = self.get_current_position()
            if board[to_x][to_y]:
                board[to_x][to_y].eliminated = True
            elif to_y > cur_y and to_y - cur_y == 2:
                board[cur_x][to_y + 1].move_piece(board, cur_x, to_y - 1, turn)
            elif to_y < cur_y and cur_y - to_y == 2:
                board[cur_x][to_y - 2].move_piece(board, cur_x, to_y + 1, turn)
            board[to_x][to_y] = self
            board[cur_x][cur_y] = 0
            self.x = to_x
            self.y = to_y
        except Exception as e: 
            print(f"Move Piece Error: {e}")

# if __name__ == "__main__":
# k = King(0, 0, 0)
# k.possible_move()