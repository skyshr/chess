from pieces import *
from csv import Error
from Map import MAP_BASIC
from constants import *
from PlayerState import PlayerState
from utils import convert_str_to_num, get_instance_first_letter, get_piece_type_by_int, list_convert_num_to_str, check_input, user_input_control
from collections import defaultdict
from Input import Input

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
            if type == KING:
                self.king_instance = piece

    def check_is_my_piece(self, piece):
        if not piece:
            return False
        return piece.side == self.side

    def handle_move_to(self, ip):
        while True:
            print("(PRESS ESC TO EXIT)")
            # possible_moves = list_convert_num_to_str(ip.piece_from)
            # print(f"possible moves: {possible_moves}")
            print(f"\n************{self.name}************\nInput Your Move To (e.g. d1): ", end="")

            
            result = user_input_control()

            # 비정상 종료 (ESC)
            if not result.get('status'):
                self.state = PlayerState.ESC
                print("Exiting Play Mode...")
                return

            ip.to = result.get('buffer')

            if not check_input(ip.to):
                continue

            to_x, to_y = convert_str_to_num(ip.to)
            if (to_x, to_y) not in ip.piece_from.get_possible_moves():
                print(f"You made an invalid move!")
                continue

            ip.to_x = to_x
            ip.to_y = to_y
            ip.piece_to = ip.board[to_x][to_y]
            ip.piece_from.move_piece(ip.board, to_x, to_y, ip.turn)

            if ip.piece_from.type == PAWN and to_x in (0, 7):
                while True:
                    print("Pawn Reached The End Of The Board!")
                    ip.promote_piece = input("Input which piece you want to promote to (K: Knight, B: Bishop, R: Rook, Q: Queen):")
                    if ip.promote_piece in ('K', 'B', 'R', 'Q'):
                        self.handle_promotion(ip)
                        break
                    else:
                        print("Wrong Input!")
            break

    def handle_move_start(self, ip):
        while True:
            print("(PRESS ESC TO EXIT)")
            print(f"\n************{self.name}************\nInput Your Move From (e.g. d1): ", end="")
            
            result = user_input_control()

            # 비정상 종료 (ESC)
            if not result.get('status'):
                self.state = PlayerState.ESC
                print("Exiting Play Mode...")
                return

            ip.begin = result.get('buffer')

            if not check_input(ip.begin):
                continue

            begin_x, begin_y = convert_str_to_num(ip.begin)
            ip.begin_x = begin_x
            ip.begin_y = begin_y
            ip.piece_from = ip.board[begin_x][begin_y]

            if not self.check_is_my_piece(ip.piece_from):
                print(f"Choose a square in which your piece exists!")
                continue

            possible_moves = list_convert_num_to_str(ip.piece_from)
            print(f"possible moves: {possible_moves}")

            if not possible_moves:
                print(f"Your selected piece doesn't have a valid square to move to.")
                continue
            break

    def move(self, board_instance):
        ip = Input()
        ip.board = board_instance.board
        ip.turn = board_instance.turn
        if self.side != ip.turn % 2:
            print(f"You are on the {self.side_name}'s side. It is {'WHITE' if ip.turn == 0 else 'BLACK'}s turn.")
            return

        self.state = PlayerState.ANY        
        attacked_squares = self.king_instance.get_attacked_squares()
        flat_list = [x for row in attacked_squares for x in row]
        print(f"\nAttacked Squares: {flat_list}")

        if not self.update_on_king_status():
            return

        self.turn = True

        while self.turn:
            self.handle_move_start(ip)
            if self.state == PlayerState.ESC:
                break

            self.handle_move_to(ip)
            if self.state == PlayerState.ESC:
                break

            type = self.get_type(ip.piece_from)
            ip.piece_to = self.get_piece_to(ip.piece_from, ip.piece_to)

            notation = self.get_notation(ip)
                    
            self.moves.append({
                'piece': ip.piece_from,
                'piece_to': ip.piece_to,
                'move': ip.turn,
                'from': ip.begin,
                'to': ip.to,
                'notation': notation,
                'type': type,
                })

            for piece in self._piece_storage[PAWN]:
                piece.enpassant = None

            self.king_instance.reset_squares()
            self.state = PlayerState.ANY
            self.turn = False
        board_instance.turn += 1

    def get_notation(self, ip):
        type = ip.piece_from.type
        if type == PAWN:
            if ip.piece_to:
                if ip.promote_piece:
                    return ip.begin[0] + 'x' + ip.to + '=' + ip.promote_piece
                else:
                    return ip.begin[0] + 'x' + ip.to
            elif ip.promote_piece:
                return ip.to + '=' + ip.promote_piece
            else:
                return ip.to
        else:
            instance_first_letter = get_instance_first_letter(type)
            if type == KING:
                if ip.piece_from.king_side_castling:
                    return 'O-O'
                elif ip.piece_from.queen_side_castling:
                    return 'O-O-O'
                elif ip.piece_to:
                    return instance_first_letter + 'x' + ip.to
                else:
                    return instance_first_letter + ip.to
            else:
                # 다른 기물 가능성 여부
                my_id = ip.piece_from.id
                dup = ''
                for piece in self._piece_storage[type]:
                    if piece.id == my_id or piece.eliminated:
                        continue
                    possible_moves = piece.get_possible_moves()
                    if (ip.to_x, ip.to_y) in possible_moves:
                        dup = ip.begin[1] if piece.y == ip.begin_y else ip.begin[0]
                        break
                if ip.piece_to:
                    return instance_first_letter + dup + 'x' + ip.to
                else:
                    return instance_first_letter + dup + ip.to

    def handle_promotion(self, ip):
        if ip.promote_piece == 'K':
            piece_type = KNIGHT
        elif ip.promote_piece == 'B':
            piece_type = BISHOP
        elif ip.promote_piece == 'R':
            piece_type = ROOK
        else:
            piece_type = QUEEN
        _id = len(self._piece_storage[piece_type])
        piece = self.get_piece(piece_type, ip.to_x, ip.to_y, _id)
        self._piece_storage[piece_type].append(piece)
        ip.piece_from.promote = piece
        piece.move_piece(ip.board, ip.to_x, ip.to_y, ip.turn)

    def automove(self, board_instance, move_from, move_to):
        ip = Input()
        ip.board = board_instance.board
        ip.turn = board_instance.turn
        if self.side != ip.turn % 2:
            print(f"You are on the {self.side_name}s side. It is {'WHITE' if ip.turn == 0 else 'BLACK'}s turn.")
            return False
        
        if not self.update_on_king_status():
            return True
        
        self.turn = True
        begin_x, begin_y = convert_str_to_num(move_from)
        ip.piece_from = ip.board[begin_x][begin_y]
        if not self.check_is_my_piece(ip.piece_from):
            print(f"Wrong Input!")
            return False

        possible_moves = list_convert_num_to_str(ip.piece_from)
        # print(f"possible moves:, {possible_moves}")
        if not possible_moves:
            print(f"Your selected piece doesn't have a valid square to move to.")
            return False
        ip.begin = move_from
        ip.begin_x = begin_x
        ip.begin_y = begin_y

        if len(move_to) == 4:
            if ip.piece_from.type != PAWN or move_to[1] not in ('1', '8'):
                print(f"Invalid move! Only Pawns Can Promote To Another Piece!")
                return False
                
        elif ip.piece_from.type == PAWN and move_to[1] in ('1', '8'):
            print(f"Invalid move! Pawns Must Promote To Another Piece At The End of The Board!")
            return False
    
        to_x, to_y = convert_str_to_num(move_to)
        if (to_x, to_y) not in ip.piece_from.get_possible_moves():
            print(f"Wrong Input!")
            return False

        ip.piece_to = ip.board[to_x][to_y]
        ip.to = move_to[:2]
        ip.to_x = to_x
        ip.to_y = to_y
        ip.piece_from.move_piece(ip.board, to_x, to_y, ip.turn)
        
        if len(move_to) == 4:
            ip.promote_piece = move_to[-1]
            self.handle_promotion(ip)

        # castling, enpassant
        type = self.get_type(ip.piece_from)
        ip.piece_to = self.get_piece_to(ip.piece_from, ip.piece_to)

        notation = self.get_notation(ip)
        self.moves.append({
            'piece': ip.piece_from,
            'piece_to': ip.piece_to,
            'move': ip.turn,
            'from': ip.begin,
            'to': ip.to,
            'notation': notation,
            'type': type,
            })

        for piece in self._piece_storage[PAWN]:
            piece.enpassant = None

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
                    return self.can_block_check(flat_list)
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
            return self.can_move()

    def can_block_check(self, list):
        for pieces in self._piece_storage.values():
            for piece in pieces:
                if piece.eliminated:
                    continue
                if piece == self.king_instance:
                    continue
                piece.filter_possible_moves(list)
                if piece.get_possible_moves():
                    print("block piece: ", piece.type)
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
        print(f"{self.side_name} has no possible moves! It is a STALEMATE! ")

        return False

    def get_type(self, piece_from):
        if piece_from.type == PAWN:
            if piece_from.promote:
                return PROMOTION
            elif piece_from.enpassant:
                return ENPASSANT
        elif piece_from.type == KING:
            if piece_from.king_side_castling:
                return KING_SIDE_CASTLING
            elif piece_from.queen_side_castling:
                return QUEEN_SIDE_CASTLING
        return NORMAL

    def get_piece_to(self, piece_from, piece_to):
        if piece_to:
            return piece_to
        elif piece_from.type == KING:
            if piece_from.king_side_castling:
                return piece_from.king_side_castling
            elif piece_from.queen_side_castling:
                return piece_from.queen_side_castling
        return piece_to

# if __name__ == "__main__":
# A = Player('sky')
# A.find_game()