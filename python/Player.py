from pieces import *
from csv import Error
from Map import MAP_BASIC
from constants import PAWN, WHITE
from PlayerState import PlayerState
from utils import convert_str_to_num, list_convert_num_to_str, check_input
from collections import defaultdict

class Player:
    def __init__(self, name):
        self.name = name
        self.side = 0
        self.side_name = ''
        self._piece_storage = defaultdict(list)
        self.king_instance = None
        self.turn = False
        self.state = PlayerState.ANY
        self.moves = []

    @property
    def get_piece_storage(self):
        return self._piece_storage

    def find_game(self):
        print(f'Player {self.name} finding game...')

    def register_side(self, side, board):
        try:
            side = side % 2
            self.side = side
            self.side_name = 'WHITE' if side == WHITE else 'BLACK'
            print(f"{self.name} is on {self.side_name} side")
            self.set_board(board)
        except Exception as e:
            print("Player register_side error!: ", e)

    def get_piece(self, piece_type, row, col, num):
        if piece_type == 'King':
           return King(self.side, row, col, num)
        elif piece_type == 'Queen':
           return Queen(self.side, row, col, num)
        elif piece_type == 'Rook':
           return Rook(self.side, row, col, num)
        elif piece_type == 'Knight':
           return Knight(self.side, row, col, num)
        elif piece_type == 'Bishop':
           return Bishop(self.side, row, col, num)
        elif piece_type == 'Pawn':
           return Pawn(self.side, row, col, num)
        else:
            raise Error(f'Wrong Piece Type - {piece_type}')
    
    def set_board(self, board):
        for piece_data in MAP_BASIC[self.side]:
            row, col, piece_type = piece_data.values()
            _id = len(self._piece_storage[piece_type])
            piece = self.get_piece(piece_type, row, col, _id)
            piece.set_piece(board, row, col)
            self._piece_storage[piece_type].append(piece)
            if isinstance(piece, King):
                self.king_instance = piece

    def check_is_my_piece(self, piece):
        if not piece:
            return False
        return piece.side == self.side

    def move(self, board_instance):
        board = board_instance.board
        turn = board_instance.turn
        if self.side != turn % 2:
            print(f"You are on the {self.side_name}s side. It is {'WHITE' if turn == 0 else 'BLACK'}s turn.")
            return
        
        attacked_squares = self.king_instance.get_attacked_squares()
        flat_list = [x for row in attacked_squares for x in row]
        print(f"\nAttacked Squares: {flat_list}")
        if not self.update_on_king_status():
            return

        self.turn = True
        while self.turn:
            begin = input(f"\n************{self.name}************\nInput Your Move From (e.g. d1): ")
            if not check_input(begin):
                continue
            begin_x, begin_y = convert_str_to_num(begin)
            piece_from = board[begin_x][begin_y]
            if not self.check_is_my_piece(piece_from):
                print(f"Choose a square in which your piece exists!")
                continue
            possible_moves = list_convert_num_to_str(piece_from)
            print(f"possible moves:, {possible_moves}")
            if not possible_moves:
                print(f"Your selected piece doesn't have a valid square to move to.")
                continue
            to = input(f"\n************{self.name}************\nInput Your Move To (e.g. d1): ")
            if not check_input(to):
                continue
            to_x, to_y = convert_str_to_num(to)
            if (to_x, to_y) not in piece_from.get_possible_moves():
                print(f"You made an invalid move!")
                continue
            piece_from.move_piece(board, to_x, to_y, turn)
            if piece_from.type == PAWN and to_x in (0, 7):
                while True:
                    print("Pawn Reached The End Of The Board!")
                    promote_piece = input("Input which piece you want to promote to (K: Knight, B: Bishop, R: Rook, Q: Queen):")
                    if promote_piece in ('K', 'B', 'R', 'Q'):
                        if promote_piece == 'K':
                            piece_type = 'Knight'
                        elif promote_piece == 'B':
                            piece_type = 'Bishop'
                        elif promote_piece == 'R':
                            piece_type = 'Rook'
                        else:
                            piece_type = 'Queen'
                        _id = len(self._piece_storage[piece_type])
                        piece = self.get_piece(piece_type, to_x, to_y, _id)
                        self._piece_storage[piece_type].append(piece)
                        piece.move_piece(board, to_x, to_y, turn)
                        break
            self.king_instance.reset_squares()
            self.moves.append({
                'piece': board[to_x][to_y],
                'move': turn,
                'from': (begin_x, begin_y),
                'to': (to_x, to_y),
                })
            self.state = PlayerState.ANY
            self.turn = False
        board_instance.turn += 1
            

    def automove(self, board_instance, move_from, move_to):
        board = board_instance.board
        turn = board_instance.turn
        if self.side != turn % 2:
            print(f"You are on the {self.side_name}s side. It is {'WHITE' if turn == 0 else 'BLACK'}s turn.")
            return False
        
        if not self.update_on_king_status():
            return True
        
        begin_x, begin_y = convert_str_to_num(move_from)
        piece_from = board[begin_x][begin_y]
        if not self.check_is_my_piece(piece_from):
            print(f"Wrong Input!")
            return False

        possible_moves = list_convert_num_to_str(piece_from)
        # print(f"possible moves:, {possible_moves}")
        if not possible_moves:
            print(f"Your selected piece doesn't have a valid square to move to.")
            return False

        to_x, to_y = convert_str_to_num(move_to)
        if (to_x, to_y) not in piece_from.get_possible_moves():
            print(f"Wrong Input!")
            return False

        piece_from.move_piece(board, to_x, to_y, turn)
        self.king_instance.reset_squares()
        self.state = PlayerState.ANY
        self.turn = False
        board_instance.turn += 1
        return True

    def update_on_king_status(self):
        check_dir_count = self.king_instance.get_attacked_dirs_count()
        attacked_squares = self.king_instance.get_attacked_squares()
        flat_list = [x for row in attacked_squares for x in row]

        if check_dir_count > 0:
            self.state = PlayerState.CHECK
            if len(self.king_instance.possible_moves) == 0:
                # checkmate
                if check_dir_count > 1:
                    self.state = PlayerState.CHECKMATE
                    print(f"{self.side_name}'s King is checkmated!")
                    return False
                # block / take
                else:
                    flag = False
                    for pieces in self._piece_storage.values():
                        for piece in pieces:
                            if piece == self.king_instance:
                                continue
                            piece.filter_possible_moves(flat_list)
                            if piece.get_possible_moves():
                                flag = True
                    if not flag:
                        self.state = PlayerState.CHECKMATE
                        print(f"{self.side_name}'s King has no possible moves so is checkmated!")
                        return False
            # king move or block / take
            else: 
                # king move
                squares = [] if check_dir_count > 1 else flat_list
                for pieces in self._piece_storage.values():
                    for piece in pieces:
                        if piece == self.king_instance:
                            continue
                        piece.filter_possible_moves(squares)
        return True

# if __name__ == "__main__":
# A = Player('sky')
# A.find_game()