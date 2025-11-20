from pieces import *
from csv import Error
from Map import MAP_BASIC
from constants import WHITE
from PlayerState import PlayerState
from utils import convert_num_to_str, convert_str_to_num
from collections import defaultdict
from types import MappingProxyType

class Player:
    def __init__(self, name):
        self.name = name
        self.state = PlayerState.ANY
        self.check = False
        self.checkmate = False
        self.turn = False
        self._piece_storage = defaultdict(list)
        self.moves = []
        self.king_instance = None
        self.side = 0
        self.side_name = ''

    @property
    def get_piece_storage(self):
        return self._piece_storage

        # return MappingProxyType(self.piece_storage)

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

    def check_is_my_piece(self, piece):
        if not piece:
            return False
        return piece.side == self.side

    def move(self, board_instance):
        board = board_instance.board
        turn = board_instance.turn
        opponent_attack_map = board_instance.blackAttackPaths if self.side == 0 else board_instance.whiteAttackPaths
        if self.side != turn % 2:
            print(f"You are on the {self.side_name}s side. It is {'white' if turn == 0 else 'black'}s turn.")
            return
        cur_x, cur_y = self.king_instance.get_current_position()
        check_dir_count = self.king_instance.count_attack_dirs(board, opponent_attack_map)
        print(f"\n{self.side_name} King's position: {convert_num_to_str(cur_x, cur_y)}")
        print(f"{self.side_name} King attacked in {check_dir_count} different direction(s)!")
        if check_dir_count > 0:
            self.turnState = PlayerState.CHECK
            if len(self.king_instance.possible_moves) == 0:
                # checkmate
                if check_dir_count > 1:
                    self.turnState = PlayerState.CHECKMATE
                    print(f"{self.side_name}'s King is checkmated!")
                    return
                # block / take
                else:
                    for pieceType in self._piece_storage:
                        for piece in self._piece_storage[pieceType]:
                            if piece == self.king_instance:
                                continue
                            possible_moves = self.king_instance.attacked_squares
                            piece.filter_possible_moves(possible_moves)
            # king move or block / take
            else: 
                # king move
                if check_dir_count > 1:
                    for pieceType in self._piece_storage:
                        for piece in self._piece_storage[pieceType]:
                            if piece == self.king_instance:
                                continue
                            piece.reset_possible_moves()
                # king move or block / take
                else:
                    for pieceType in self._piece_storage:
                        for piece in self._piece_storage[pieceType]:
                            if piece == self.king_instance:
                                continue
                            possible_moves = self.king_instance.attacked_squares
                            piece.filter_possible_moves(possible_moves)
        self.turn = True
        while self.turn:
            begin = input(f"************{self.name}************\nInput Your Move From (e.g. d1): ")
            if not self.check_input(begin):
                continue
            begin_x, begin_y = convert_str_to_num(begin)
            piece_from = board[begin_x][begin_y]
            if not self.check_is_my_piece(piece_from):
                print(f"Choose a square in which your piece exists!")
                continue
            to = input(f"************{self.name}************\nInput Your Move To (e.g. d1): ")
            if not self.check_input(to):
                continue
            to_x, to_y = convert_str_to_num(to)
            piece_to = board[to_x][to_y]
            if self.check_is_my_piece(piece_to):
                print(f"You cannot move your piece to a square in which your piece exists!")
                continue
            if (to_x, to_y) not in board[begin_x][begin_y].possible_moves:
                print(f"You made an invalid move!")
                continue
            piece_from.move_piece(board, to_x, to_y, turn)
            self.king_instance.attacked_dirs = [0] * 8
            self.king_instance.attacked_squares = []
            self.moves.append({
                'piece': board[to_x][to_y],
                'move': turn,
                'from': (begin_x, begin_y),
                'to': (to_x, to_y),
                })
            self.check = False
            self.turn = False
        board_instance.turn += 1
            

# if __name__ == "__main__":
# A = Player('sky')
# A.find_game()