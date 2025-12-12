from pieces import *
from csv import Error
from Map import MAP_BASIC
from constants import *
from PlayerState import PlayerState
from utils import convert_str_to_num, get_instance_first_letter, get_piece_type_by_int, list_convert_num_to_str, check_input, user_input_control
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
        if piece_type == KING:
           return King(self.side, row, col, num)
        elif piece_type == QUEEN:
           return Queen(self.side, row, col, num)
        elif piece_type == ROOK:
           return Rook(self.side, row, col, num)
        elif piece_type == KNIGHT:
           return Knight(self.side, row, col, num)
        elif piece_type == BISHOP:
           return Bishop(self.side, row, col, num)
        elif piece_type == PAWN:
           return Pawn(self.side, row, col, num)
        else:
            raise Error(f'Wrong Piece Type - {piece_type}')
    
    def set_board(self, board):
        for piece_data in MAP_BASIC[self.side]:
            row, col, piece_type = piece_data.values()
            type = get_piece_type_by_int(piece_type)
            _id = len(self._piece_storage[type])
            piece = self.get_piece(type, row, col, _id)
            piece.set_piece(board, row, col)
            self._piece_storage[type].append(piece)
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
            print(f"You are on the {self.side_name}'s side. It is {'WHITE' if turn == 0 else 'BLACK'}s turn.")
            return

        self.state = PlayerState.ANY        
        attacked_squares = self.king_instance.get_attacked_squares()
        flat_list = [x for row in attacked_squares for x in row]
        print(f"\nAttacked Squares: {flat_list}")

        if not self.update_on_king_status():
            return

        self.turn = True
        while self.turn:
            print("(PRESS ESC TO EXIT)")
            print(f"\n************{self.name}************\nInput Your Move From (e.g. d1): ", end="")
            
            result = user_input_control()

            # 비정상 종료 (ESC)
            if not result.get('status'):
                self.state = PlayerState.ESC
                print("Exiting Play Mode...")
                break

            begin = result.get('buffer')

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

            print("(PRESS ESC TO EXIT)")
            print(f"\n************{self.name}************\nInput Your Move From (e.g. d1): ", end="")
            
            result = user_input_control()

            # 비정상 종료 (ESC)
            if not result.get('status'):
                self.state = PlayerState.ESC
                print("Exiting Play Mode...")
                break

            to = result.get('buffer')

            if not check_input(to):
                continue
            to_x, to_y = convert_str_to_num(to)
            if (to_x, to_y) not in piece_from.get_possible_moves():
                print(f"You made an invalid move!")
                continue
            exist_piece = True if board[to_x][to_y] else False
            piece_to = board[to_x][to_y]
            promote_piece = ''
            piece_from.move_piece(board, to_x, to_y, turn)

            if piece_from.type == PAWN and to_x in (0, 7):
                while True:
                    print("Pawn Reached The End Of The Board!")
                    promote_piece = input("Input which piece you want to promote to (K: Knight, B: Bishop, R: Rook, Q: Queen):")
                    if promote_piece in ('N', 'B', 'R', 'Q'):
                        if promote_piece == 'N':
                            piece_type = KNIGHT
                        elif promote_piece == 'B':
                            piece_type = BISHOP
                        elif promote_piece == 'R':
                            piece_type = ROOK
                        else:
                            piece_type = QUEEN
                        _id = len(self._piece_storage[piece_type])
                        piece = self.get_piece(piece_type, to_x, to_y, _id)
                        self._piece_storage[piece_type].append(piece)
                        piece_from.promote = piece
                        piece.move_piece(board, to_x, to_y, turn)
                        break
            self.king_instance.reset_squares()

            # castling, enpassant
            type = NORMAL
            if piece_from.type == PAWN:
                if piece_from.enpassant:
                    piece_to = piece_from.enpassant
                    type = ENPASSANT
                    piece_from.enpassant = None
                elif piece_from.promote:
                    type = PROMOTION
            elif piece_from.type == KING:
                if piece_from.king_side_castling:
                    piece_to = piece_from.king_side_castling
                    type = KING_SIDE_CASTLING
                elif piece_from.queen_side_castling:
                    piece_to = piece_from.queen_side_castling
                    type = QUEEN_SIDE_CASTLING

            notation = self.get_notation(piece_from, begin, to, exist_piece, promote_piece)
                    
            self.moves.append({
                'piece': piece_from,
                'piece_to': piece_to,
                'move': turn,
                'from': begin,
                'to': to,
                'notation': notation,
                'type': type,
                })

            self.state = PlayerState.ANY
            self.turn = False
        board_instance.turn += 1

    def get_notation(self, instance, begin, to, piece_to, promote):
        type = instance.type
        if type == PAWN:
            if piece_to:
                if promote:
                    return begin[0] + 'x' + to + '=' + promote
                else:
                    return begin[0] + 'x' + to
            elif promote:
                return to + '=' + promote
            else:
                return to
        else:
            instance_first_letter = get_instance_first_letter(type)
            if type == KING:
                if instance.king_side_castling:
                    return 'O-O'
                elif instance.queen_side_castling:
                    return 'O-O-O'
                elif piece_to:
                    return instance_first_letter + 'x' + to
                else:
                    return instance_first_letter + to
            else:
                # 다른 기물 가능성 여부
                my_id = instance.id
                begin_x, begin_y = convert_str_to_num(begin)
                to_x, to_y = convert_str_to_num(to)
                dup = ''
                for piece in self._piece_storage[type]:
                    if piece.id == my_id or piece.eliminated:
                        continue
                    possible_moves = piece.get_possible_moves()
                    if (to_x, to_y) in possible_moves:
                        dup = begin[1] if piece.y == begin_y else begin[0]
                        break
                if piece_to:
                    return instance_first_letter + dup + 'x' + to
                else:
                    return instance_first_letter + dup + to

    def automove(self, board_instance, move_from, move_to):
        board = board_instance.board
        turn = board_instance.turn
        if self.side != turn % 2:
            print(f"You are on the {self.side_name}s side. It is {'WHITE' if turn == 0 else 'BLACK'}s turn.")
            return False
        
        if not self.update_on_king_status():
            return True
        
        self.turn = True
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

        if len(move_to) == 4:
            if piece_from.type != PAWN or move_to[1] not in ('1', '8'):
                print(f"Invalid move! Only Pawns Can Promote To Another Piece!")
                return False
        elif piece_from.type == PAWN and move_to[1] in ('1', '8'):
            print(f"Invalid move! Pawns Must Promote To Another Piece At The End of The Board!")
            return False
    
        to_x, to_y = convert_str_to_num(move_to)
        if (to_x, to_y) not in piece_from.get_possible_moves():
            print(f"Wrong Input!")
            return False
        piece_to = board[to_x][to_y]
        piece_from.move_piece(board, to_x, to_y, turn)
        promote_piece = ''
        
        if len(move_to) == 4:
            promote_piece = move_to[-1]
            if promote_piece == 'N':
                piece_type = KNIGHT
            elif promote_piece == 'B':
                piece_type = BISHOP
            elif promote_piece == 'R':
                piece_type = ROOK
            else:
                piece_type = QUEEN
            _id = len(self._piece_storage[piece_type])
            piece = self.get_piece(piece_type, to_x, to_y, _id)
            self._piece_storage[piece_type].append(piece)
            piece_from.promote = piece
            piece.move_piece(board, to_x, to_y, turn)

        self.king_instance.reset_squares()

        # castling, enpassant
        type = NORMAL
        if piece_from.type == PAWN:
            if piece_from.enpassant:
                piece_to = piece_from.enpassant
                type = ENPASSANT
                piece_from.enpassant = None
            elif piece_from.promote:
                type = PROMOTION
        elif piece_from.type == KING:
            if piece_from.king_side_castling:
                piece_to = piece_from.king_side_castling
                type = KING_SIDE_CASTLING
            elif piece_from.queen_side_castling:
                piece_to = piece_from.queen_side_castling
                type = QUEEN_SIDE_CASTLING

        notation = self.get_notation(piece_from, move_from, move_to[:2], piece_to, promote_piece)
        self.moves.append({
            'piece': piece_from,
            'piece_to': piece_to,
            'move': turn,
            'from': move_from,
            'to': move_to[:2],
            'notation': notation,
            'type': type,
            })

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
                    return can_block_check(self. flat_list)
            # king move or block / take
            else: 
                # king move
                squares = [] if check_dir_count > 1 else flat_list
                for pieces in self._piece_storage.values():
                    for piece in pieces:
                        if piece.eliminated:
                            continue
                        if piece == self.king_instance:
                            continue
                        piece.filter_possible_moves(squares)
                return True

        else:
            return can_move()

def can_block_check(self, list):
    for pieces in self._piece_storage.values():
        for piece in pieces:
            if piece.eliminated:
                continue
            if piece == self.king_instance:
                continue
            piece.filter_possible_moves(list)
            if piece.get_possible_moves():
                print("piece: ", piece.type)
                print(piece.get_possible_moves())
                return True

    self.state = PlayerState.CHECKMATE
    print(f"{self.side_name}'s King is in check but has no possible moves! You are CHECKMATED!")

    return False

def can_move(self):
    for pieces in self._piece_storage.values():
        for piece in pieces:
            if piece.eliminated:
                continue
            if piece.get_possible_moves():
                print("piece: ", piece.type)
                print(piece.get_possible_moves())
                return True
    
    self.state = PlayerState.STALEMATE
    print(f"{self.side_name}'s King has no possible moves! It is a STALEMATE! ")

    return False
# if __name__ == "__main__":
# A = Player('sky')
# A.find_game()