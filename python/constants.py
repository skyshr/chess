ROW = 8
COL = 8

# 0: White, 1: Black
WHITE = 0
BLACK = 1

# Piece Type
# 0: None
# 1: Pawn
# 2: Bishop
# 3: Knight
# 4: Rook
# 5: Queen
# 6: King
EMPTY, PAWN, BISHOP, KNIGHT, ROOK, QUEEN, KING = range(7)

# Piece Dirs 
# 0: north
# 1: north-west
# 2: west
# 3: south-west
# 4: south
# 5: south-east
# 6: east
# 7: north-east

# state
# 0: Before Match
# 1: Match Complete
# 2: In Game
# 3: END
STATE_BEFORE_MATCH = 0
STATE_GAME_READY = 1
STATE_IN_GAME = 2
STATE_GAME_OVER = 3

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
# printing => white: green, black: red
COLOR_BLACK = '\033[30m'
COLOR_RED = '\033[31m'
COLOR_GREEN = '\033[32m'
COLOR_YELLOW = '\033[33m'
COLOR_BLUE = '\033[34m'
COLOR_MAGENTA = '\033[35m'
COLOR_CYAN = '\033[36m'
COLOR_WHITE = '\033[37m'
COLOR_RESET = '\033[0m'

# King State
NOT_IN_CHECK = 0
SINGLE_CHECK = 1
DOUBLE_CHECK = 2