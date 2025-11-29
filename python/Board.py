import random
from pieces import *
from Player import Player
from PlayerState import PlayerState
from fileReader import read_file
from utils import convert_num_to_str
from constants import *

DEFAULT_COLOR_BLACK = COLOR_RED
DEFAULT_COLOR_WHITE = COLOR_GREEN

piece_dict = {
    PAWN: 'Pawn', 
    KNIGHT: 'Knight', 
    BISHOP: 'Bishop',
    ROOK: 'Rook',
    QUEEN: 'Queen',
    KING: 'King',
    }

class Board:
    game_number = 0

    def __init__(self, playerA, playerB):
        self.game_number = Board.game_number
        self.state = STATE_BEFORE_MATCH
        self.playerA = playerA
        self.playerB = playerB
        self.board = [[EMPTY] * COL for _ in range(ROW)]
        self.turn = 0
        self.piece_storage = {WHITE: None, BLACK: None}
        self.moves = []
        self.strength = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [-1, -2, -2, -2, -2, -2, -2, -1],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [1, 2, 2, 2, 2, 2, 2, 1],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ]
        self.whiteAttackPaths = [[EMPTY] * COL for _ in range(ROW)]
        self.blackAttackPaths = [[EMPTY] * COL for _ in range(ROW)]
        
        self.prepare_game()

    def prepare_game(self):
        side = random.randint(0, 1)
        self.playerA.register_side(side, self.board)
        self.playerB.register_side(side + 1, self.board)
        
        # set playerA white, playerB black
        if side == 1:
            self.playerA, self.playerB = self.playerB, self.playerA

        self.piece_storage[WHITE] = self.playerA.get_piece_storage
        self.piece_storage[BLACK] = self.playerB.get_piece_storage

        self.state = STATE_GAME_READY
        Board.game_number += 1

    def print_piece_type(self, piece):
        if piece:
            color = DEFAULT_COLOR_WHITE if piece.side == WHITE else DEFAULT_COLOR_BLACK
            resetColor = COLOR_RESET
            print(color + str(piece.type) + resetColor, end=" ")
        else:
            print(EMPTY, end=" ")

    def print_board(self):
        print('\nboard: ')
        for row in self.board:
            print("[ ", end="")
            for square in row:
                self.print_piece_type(square)
            print("]")

    def print_single_player_piece_state(self, player):
        side = player.side
        side_name = player.side_name

        print(f"\n---------------------{side_name}------------------------")
        for piece_type, pieces in self.piece_storage[side].items():
            for piece in pieces:
                piece_name = piece_dict[piece_type]
                if piece.eliminated:
                    print(f"{piece_name}[{piece._id}]: eliminated", end=", ")    
                    continue
                x, y = piece.get_current_position()
                print(f"{piece_name}({piece._id}): {convert_num_to_str(x, y)}", end=", ")
            print("")

    def print_both_player_piece_state(self):
        self.print_single_player_piece_state(self.playerA)
        self.print_single_player_piece_state(self.playerB)

    def check_king_state(self):
        turn = WHITE if self.turn % 2 == 0 else BLACK
        king = self.piece_storage[turn][KING][0]
        cnt = king.get_attacked_dirs_count()
        # update notation
        if cnt:
            player = self.playerA if turn == BLACK else self.playerB
            player.moves[-1]['notation'] += '+'

        if cnt == DOUBLE_CHECK:
            message = 'Double Check'
        elif cnt == SINGLE_CHECK:
            message = 'Single Check'
        elif cnt == NOT_IN_CHECK:
            message = 'Not In Check'
        else:
            message = 'Something Went Wrong'
        print(f'\n{"White" if turn % 2 == 0 else "Black"} King\'s State: {message}')


    def update_king_squares(self):
        turn = WHITE if self.turn % 2 == 0 else BLACK
        map = self.blackAttackPaths if turn == WHITE else self.whiteAttackPaths
        king = self.piece_storage[turn][KING][0]
        king.check_castling(self.board, map)
        king.delete_attacked_squares(map)

    def start_game(self):
        print(f'Game [{self.game_number}] has started! White to Move...')
        self.state = STATE_IN_GAME
        self.set_attack_path()
        # self.print_both_player_piece_state()
        # self.print_board()
        # self.check_king_state()
        player = self.playerA

        while True:
            player.move(self)
            if player.state == PlayerState.CHECKMATE:
                break
            self.update_attack_path()
            # self.print_both_player_piece_state()
            self.print_board()
            self.update_king_squares()
            self.check_king_state()
            self.print_notations()
            player = self.playerA if player == self.playerB else self.playerB
        self.state = STATE_GAME_OVER

    def print_notations(self):
        white_notations = [move['notation'] for move in self.playerA.moves]
        black_notations = [move['notation'] for move in self.playerB.moves]
        
        if self.playerA.state == PlayerState.CHECKMATE:
            black_notations[-1] = black_notations[-1].replace('+', '')
            black_notations[-1] += '#'
        elif self.playerB.state == PlayerState.CHECKMATE:
            white_notations[-1] = white_notations[-1].replace('+', '')
            white_notations[-1] += '#'

        total_notations = [(white_notations[i], black_notations[i]) if i < len(black_notations) else (white_notations[i], ) for i in range(len(white_notations))]

        print("\nnotations: ")
        for notation in total_notations:
            print(notation)
        if len(white_notations) > len(black_notations) or self.playerB.state == PlayerState.CHECKMATE:
            print("1-0")
        else:
            print("0-1")

    def print_attack_path(self):
        print(f'\nWHITE ATTACK PATH:')
        for row in self.whiteAttackPaths:
            print(row)
        print(f'\nBLACK ATTACK PATH:')
        for row in self.blackAttackPaths:
            print(row)

    def set_attack_path(self):
        for pieces in self.piece_storage[WHITE].values():
            for piece in pieces:
                piece.draw_attack_paths(self.board, self.whiteAttackPaths, self.turn)
        
        for pieces in self.piece_storage[BLACK].values():
            for piece in pieces:
                piece.draw_attack_paths(self.board, self.blackAttackPaths, self.turn)
        
        # self.print_attack_path()
    
    def update_attack_path(self):
        try:
            self.blackAttackPaths = [[0] * ROW for _ in range(COL)]
            self.whiteAttackPaths = [[0] * ROW for _ in range(COL)]
            self.set_attack_path()

            draw_pinned_map = WHITE if self.turn % 2 else BLACK
            for pieces in self.piece_storage[draw_pinned_map].values():
                for piece in pieces:
                    piece.check_opponent_piece_pinned_status(self.board, self.turn)
        except Exception as e:
            print("Update Attack Path error!: ", e)

    def read_file(self):
        self.moves = read_file(input("Input Filename To Read: "))
        self.automove()

    def automove(self):
        if not self.moves:
            print("No Move Data. Game Ends...")
            return
        self.state = STATE_IN_GAME
        self.set_attack_path()
        
        max_moves = len(self.moves)
        end = None

        while True:
            end = input(f"\nInput Your AutoMove End Number (1 ~ {max_moves}): ")
            if end.isdigit():
                if 0 < int(end) <= max_moves:
                    end = int(end)
                    break
                else:
                    print(f"Input Number between 1 ~ {max_moves}")
            else:
                print("Invalid Input!")
        
        self.automove_loop(end)
        self.print_board()
        self.play_after_automove()

    def automove_loop(self, end):
        player = self.playerA

        for i in range(end):
            for move in self.moves[i]:
                move_from, move_to = move
                if not player.automove(self, move_from, move_to):
                    self.state = STATE_GAME_OVER
                    return
                if player.state == PlayerState.CHECKMATE:
                    self.state = STATE_GAME_OVER
                    return
                self.update_attack_path()
                self.update_king_squares()
                self.check_king_state()

                player = self.playerA if player == self.playerB else self.playerB

    def play_after_automove(self):
        if self.state == STATE_GAME_OVER:
            print("Can't Carry On After Automove! The Game Is Over!")
            return

        player = self.playerA

        while True:
            player.move(self)
            if player.state == PlayerState.CHECKMATE:
                break
            self.update_attack_path()
            self.print_board()
            self.update_king_squares()
            self.check_king_state()
            player = self.playerA if player == self.playerB else self.playerB
        self.state = STATE_GAME_OVER
        self.print_notations()

if __name__ == "__main__":
    board = Board(Player('sky'), Player('tom'))
    board.read_file()
    # board.start_game()

    # board1 = Board(Player('sky1'), Player('tom1'))
    # board1.print_board()
