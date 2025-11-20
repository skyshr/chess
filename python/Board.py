import random
from pieces import *
from Player import Player
from utils import convert_num_to_str
from constants import *

DEFAULT_COLOR_BLACK = COLOR_RED
DEFAULT_COLOR_WHITE = COLOR_GREEN

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
            print(color + str(piece.type) + resetColor, end="")
        else:
            print(EMPTY, end="")
        print(" ", end="")

    def print_board(self):
        print('\nboard: ')
        for row in self.board:
            print("[ ", end="")
            for square in row:
                self.print_piece_type(square)
            print("]")

    def print_single_player_piece_state(self, player):
        side = player.side
        sideName = player.side_name
        print(f"\n---------------------{sideName}------------------------")
        for pieceType, pieces in self.piece_storage[side].items():
            for piece in pieces:
                if piece.eliminated:
                    print(f"{pieceType}[{piece._id}]: eliminated", end=", ")    
                    continue
                x, y = piece.get_current_position()
                print(f"{pieceType}({piece._id}): {convert_num_to_str(x, y)}", end=", ")
            print("")

    def print_both_player_piece_state(self):
        self.print_single_player_piece_state(self.playerA)
        self.print_single_player_piece_state(self.playerB)

    def start_game(self):
        print(f'Game [{self.game_number}] has started! White to Move...')
        self.state = STATE_IN_GAME
        self.set_attack_path()
        # self.print_both_player_piece_state()
        # self.print_board()
        # player = self.playerA

        # while not player.checkmate:
        #     player.move(self)
        #     self.update_attack_path()
        #     self.print_board()
        #     player = self.playerA if player == self.playerB else self.playerB
        # self.state = STATE_GAME_OVER

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
                piece.draw_attack_paths(self.board, self.whiteAttackPaths)
                # piece.possible_move(self.board, self.whiteAttackPaths, self.turn)
        
        for pieces in self.piece_storage[BLACK].values():
            for piece in pieces:
                piece.draw_attack_paths(self.board, self.blackAttackPaths)
                # piece.possible_move(self.board, self.blackAttackPaths, self.turn)

        self.print_attack_path()
    
    def update_attack_path(self):
        try:
            self.blackAttackPaths = [[0] * ROW for _ in range(COL)]
            self.whiteAttackPaths = [[0] * ROW for _ in range(COL)]
            self.set_attack_path()
        except Exception as e:
            print("Update Attack Path error!: ", e)


if __name__ == "__main__":
    board = Board(Player('sky'), Player('tom'))
    board.start_game()

    # board1 = Board(Player('sky1'), Player('tom1'))
    # board1.print_board()
