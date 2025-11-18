from Player import BLACK, WHITE, Player
import random
import pieces

# 0: White, 1: Black
# 0: Rook, 1: Knight, 2: Bishop, 3: Queen, 4: King, 5: Bishop, 6: Knight, 7: Pawn

# 중심 3을 기준으로 side만큼 보정
piece_coords_x = {
    'Rook': [0, 7],
    'Knight': [1, 6],
    'Bishop': [2, 5],
    'Queen': [3],
    'King': [4],
    'Pawn': [0, 1, 2, 3, 4, 5, 6, 7],
}

# Board coordinates:
# [x][y]
# x => 0: A, 1: B, 2: C, 3: D, 4: E, 5: F, 6: G, 7: H
# y => 0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8

# state
# 0: Before Match
# 1: Match Complete
# 2: In Game
# 3: END

STATE_BEFORE_MATCH = 0
STATE_MATCH_COMPLETE = 1
STATE_IN_GAME = 2
STATE_GAME_OVER = 3

# Piece Type
# 0: None
# 1: Pawn
# 2: Bishop
# 3: Knight
# 4: Rook
# 5: Queen
# 6: King

# Ansi Color
# 검정(black)	        \033[30m
# 빨강(red)	            \033[31m
# 초록(green)	        \033[32m
# 노랑(yellow)	        \033[33m
# 파랑(blue)	        \033[34m
# 마젠타(magenta)	    \033[35m
# 사이언(cyan)  	    \033[36m
# 흰색(white)	        \033[37m
# 리셋(reset)           \033[0m

# white: 초록(green), black: 빨강(red)

global row, col
row = col = 8
class Board:
    game_number = 0

    def __init__(self, playerA, playerB):
        global row, col
        self.game_number = Board.game_number
        self.state = STATE_BEFORE_MATCH
        self.playerA = playerA
        self.playerB = playerB
        self.board = [[0] * col for _ in range(row)]
        self.turn = 0
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
        self.whiteAttackPath = [[0]*row for _ in range(col)]
        self.blackAttackPath = [[0]*row for _ in range(col)]
        side = random.randint(0, 1)
        self.playerA.register_side(side, self.board)
        self.playerB.register_side(side + 1, self.board)
        self.state = STATE_MATCH_COMPLETE
        self.pinned = []
        Board.game_number += 1

    def print_piece_type(self, piece):
        pre, suf = '', ''
        if piece:
            suf = '\033[0m'
            pre = '\033[31m' if piece.side == BLACK else '\033[32m'
        if isinstance(piece, pieces.Pawn):
            print(pre + "1" + suf, end="")
        elif isinstance(piece, pieces.Knight):
            print(pre + "2" + suf, end="")
        elif isinstance(piece, pieces.Bishop):
            print(pre + "3" + suf, end="")
        elif isinstance(piece, pieces.Rook):
            print(pre + "4" + suf, end="")
        elif isinstance(piece, pieces.Queen):
            print(pre + "5" + suf, end="")
        elif isinstance(piece, pieces.King):
            print(pre + "6" + suf, end="")
        else:
            print("0", end="")
        print(" ", end="")


    def print_board(self):
        print('\n\nboard: ')
        for row in self.board:
            print("[ ", end="")
            for square in row:
                self.print_piece_type(square)
            print("]\n", end="")

    def start_game(self):
        print(f'Game {self.game_number} has started! {'White' if self.turn == 0 else 'Black'}s Move...')
        self.state = STATE_IN_GAME
        self.set_attack_path()

        personA = self.playerA if self.playerA.side == WHITE else self.playerB
        personB = self.playerB if personA == self.playerA else self.playerA

        while self.state != STATE_GAME_OVER:
            player = personA if self.turn % 2 == 0 else personB
            player.move(self)
            self.pinned = []
            self.update_attack_path()
            self.print_board()

        # personA.move(self)
        # self.update_attack_path()
        # self.print_board()
        # personB.move(self)
        # self.update_attack_path()
        # self.print_board()

        # personA.move(self)
        # self.update_attack_path()
        # self.print_board()
        # personB.move(self)
        # self.update_attack_path()
        # self.print_board()

        # personA.move(self)
        # self.update_attack_path()
        # self.print_board()
        # personB.move(self)
        # self.update_attack_path()
        # self.print_board()

    def set_attack_path(self):
        global row, col
        for x in range(row):
            for y in range(col):
                piece = self.board[x][y]
                if not piece: continue
                if piece.side == WHITE:
                    piece.possible_move(self.board, self.whiteAttackPath, self.turn)
                else:
                    piece.possible_move(self.board, self.blackAttackPath, self.turn)
        print(f'\n\nBLACK ATTACK_PATH\n')
        for _row in self.blackAttackPath:
            print(_row)
        print(f'\n\nWHITE ATTACK_PATH\n')
        for _row in self.whiteAttackPath:
            print(_row)
    
    def update_attack_path(self):
        global row, col
        try:
            self.blackAttackPath = [[0] * row for _ in range(col)]
            self.whiteAttackPath = [[0] * row for _ in range(col)]
            self.set_attack_path()
        except Exception as e:
            print("Update Attack Path error!: ", e)


if __name__ == "__main__":
    board = Board(Player('sky'), Player('tom'))
    # board.print_board()
    board.start_game()

    # board1 = Board(Player('sky1'), Player('tom1'))
    # board1.print_board()
