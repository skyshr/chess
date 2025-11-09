from csv import Error
from sys import exception
from Map import basic
import pieces
import copy

WHITE = 0
BLACK = 1

class Player:
    def __init__(self, name):
        self.name = name
        self.check = False
        self.checkmate = False
        self.position = {}
        self.possible_moves = []
        self.moves = []

    def find_game(self):
        print(f'Player {self.name} finding game...')

    def register_side(self, side, board):
        try:
            side = side % 2
            self.side = side
            print(f"{self.name} is on {'BLACK' if side else 'WHITE'} side")
            self.set_board(board)
        except Exception as e:
            print("Player register_side error!: ", e)

    def get_piece(self, piece_type, row, col, num):
        if piece_type == 'King':
           return pieces.King(self.side, row, col, num)
        elif piece_type == 'Queen':
           return pieces.Queen(self.side, row, col, num)
        elif piece_type == 'Rook':
           return pieces.Rook(self.side, row, col, num)
        elif piece_type == 'Knight':
           return pieces.Knight(self.side, row, col, num)
        elif piece_type == 'Bishop':
           return pieces.Bishop(self.side, row, col, num)
        elif piece_type == 'Pawn':
           return pieces.Pawn(self.side, row, col, num)
        else:
            raise Error(f'Wrong Piece Type - {piece_type}')
    
    def set_board(self, board):
        for num, data in enumerate(basic[self.side]):
            row, col, piece_type = data.values()
            piece = self.get_piece(piece_type, row, col, num)
            board[row][col] = piece
            self.position[num] = piece

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
        print("board[x][y]: ", board[x][y], board[x][y].side, self.side)
        # print("isinstance: ", isinstance(board[x][y], pieces.Pawn))
        # print("instance: ", type(board[x][y]) == pieces.Pawn)
        return board[x][y].side == self.side

    # 1 => 7, 2 => 6, 3 => 5, 4 => 4, 5 => 3, 6 => 2, 7 => 1 

    def convert_str_to_row_col(self, str):
        x, y = 8 - int(str[1]), ord(str[0]) - ord('a')
        print('x, y: ', x, y)
        return [x, y]

    def calculate_possible_moves(self, board):
        for piece in self.position:
            if self.position[piece].eliminated:
                # print(f"piece no longer exists in the board")
                continue
            self.position[piece].possible_move(board)

    def is_valid_move(self, board, from_x, from_y, to_x, to_y):
        my_piece = board[from_x][from_y]

        if self.check:
            # blocking 추가
            if not isinstance(my_piece, pieces.King):
                print("Your King is in check! Move your King to a safe place!!")
                return False
        if isinstance(my_piece, pieces.King):
            if self.check:
                pass
            # Defended
            if my_piece.has_moved:
                if not self.is_safe(self, board, to_x, to_y):
                    print(f"Square [{to_x}][{to_y}] is defended by opponent's piece. Try again.")
                else:
                    return True
            # Castling
            else:
                # King Side Castling
                if to_y- from_y == 2:
                    castling_piece = board[from_x][7]
                    if not castling_piece:
                        print('[1] Your Rook has already moved so king-side castling is not possible!')
                        return False
                    else:
                        castling_piece = board[from_x][7]
                        if not isinstance(castling_piece, pieces.Rook) or castling_piece.has_moved:
                            print('[2] Your Rook has already moved so king-side castling is not possible!')
                            return False
                    pass
                # Queen Side Castling
                elif to_y - from_y == -2:
                    castling_piece = board[from_x][0]
                    if not castling_piece:
                        print('[1] Your Rook has already moved so king-side castling is not possible!')
                        return False
                    else:
                        if not isinstance(castling_piece, pieces.Rook) or castling_piece.has_moved:
                            print('[2] Your Rook has already moved so king-side castling is not possible!')
                            return False
                    pass
                else:
                    pass
        elif isinstance(my_piece, pieces.Pawn):
            pass
        elif isinstance(my_piece, pieces.Knight):
            pass
        elif isinstance(my_piece, pieces.Bishop):
            pass
        elif isinstance(my_piece, pieces.Rook):
            pass
        elif isinstance(my_piece, pieces.Queen):
            pass
        else:
            print(f"Invalid type - board[{from_x}][{from_y}]: ", type(board[from_x][from_y]))
            return False
        return True

    def move(self, board_instance):
        board = board_instance.board
        turn = board_instance.turn
        if self.side != turn:
            print(f"You are on the {'white' if self.side == 0 else 'black'}s side. It is {'white' if turn == 0 else 'black'}s turn.")
            return
        while True:
            begin = input(f"************{self.name}************\nInput Your Move From (e.g. d1): ")
            if not self.check_input(begin):
                continue
            begin_x, begin_y = self.convert_str_to_row_col(begin)
            if not self.check_is_my_piece(board, begin_x, begin_y):
                print(f"Choose a square in which your piece exists!")
                continue
            to = input(f"************{self.name}************\nInput Your Move To (e.g. d1): ")
            if not self.check_input(to):
                continue
            to_x, to_y = self.convert_str_to_row_col(to)
            if self.check_is_my_piece(board, to_x, to_y):
                print(f"You cannot move your piece to a square in which your piece exists!")
                continue
            self.calculate_possible_moves(board)
            # if not self.is_valid_move(board, begin_x, begin_y, to_x, to_y):
            #     if self.checkmate:
            #         return
            #     else:
            #         continue
            # self.moves.append((begin, to))
            # board[begin_x][begin_y].has_moved = True
            # board[to_x][to_y] = copy.deepcopy(board[begin_x][begin_y])
            # board[begin_x][begin_y] = 0
            break
        board_instance.turn = (board_instance.turn + 1) % 2
            

# if __name__ == "__main__":
# A = Player('sky')
# A.find_game()