from csv import Error
from sys import exception
from Map import basic
import pieces

WHITE = 0
BLACK = 1

class Player:
    def __init__(self, name):
        self.name = name
        self.check = False

    def play_game(self):
        print(f'Player {self.name} finding game...')

    def register_side(self, side, board):
        try:
            side = side % 2
            self.side = side
            print(f"{self.name} is on {'BLACK' if side else 'WHITE'} side")
            self.set_board(board)
        except Exception as e:
            print("Player register_side error!: ", e)
    
    def set_board(self, board):
        for data in basic[self.side]:
            row, col, piece_type = data.values()
            if piece_type == 'King':
                board[row][col] = pieces.King(self.side, row, col)
            elif piece_type == 'Queen':
                board[row][col] = pieces.Queen(self.side, row, col)
            elif piece_type == 'Rook':
                board[row][col] = pieces.Rook(self.side, row, col)
            elif piece_type == 'Knight':
                board[row][col] = pieces.Knight(self.side, row, col)
            elif piece_type == 'Bishop':
                board[row][col] = pieces.Bishop(self.side, row, col)
            elif piece_type == 'Pawn':
                board[row][col] = pieces.Pawn(self.side, row, col)
            else:
                raise Error(f'Wrong Piece Type - {piece_type}')

    def check_input(self, str):
        if len(str) != 2:
            print(f'[{str}]: Wrong length! Appropriate length is 2')
            return False
        elif str[0] < 'a' or str[0] > 'h':
            print(f'[{str}]: Wrong First Letter! First letter must be an alphabet between "a" and "h"')
            return False
        elif str[1] < '1' or str[1] > '8':
            print(f'[{str}]: Wrong Second Letter! Second letter must be an integer between "1" and "8"')
            return False
        return True

    def check_is_my_piece(self, board, x, y):
        if not board[x][y]:
            return False
        return board[x][y].side == self.side

    def convert_str_to_row_col(self, str):
        x, y = int(str[1]) - 1, ord(str[0]) - ord('a')
        print('x, y: ', x, y)
        return [x, y]

    def move(self, board):
        while True:
            begin = input(f"************{self.name}************\nInput Your Move From (e.g. d1): ")
            if not self.check_input(begin):
                continue
            begin_x, begin_y = self.convert_str_to_row_col(begin)
            if self.check_is_my_piece(board, )
            to = input(f"************{self.name}************\nInput Your Move To (e.g. d1): ")
            if not self.check_input(to):
                continue
            to_x, to_y = self.convert_str_to_row_col(to)
            break
            

# A = Player('sky')
# A.play_game()