import sys
import msvcrt
from constants import PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING

def convert_str_to_num(str):
    x, y = 8 - int(str[1]), ord(str[0]) - ord('a')
    return (x, y)

def convert_num_to_str(x, y):
    nx, ny = str(8 - x), chr(ord('a') + y)
    return f'{ny}{nx}'

def list_convert_num_to_str(piece):
    return list(map(lambda pos: convert_num_to_str(pos[0], pos[1]), piece.get_possible_moves()))

def check_input(str):
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

def check_auto_input(str, order):
    if len(str) != 2 and (len(str) != 4 or order == 1):
        print(f'[{str}]: Wrong Format: Notation Length!')
        return False
    if str[0] < 'a' or str[0] > 'h':
        print(f'[{str}]: Wrong First Letter: First letter must be an alphabet between "a" and "h"')
        return False
    if str[1] < '1' or str[1] > '8':
        print(f'[{str}]: Wrong Second Letter: Second letter must be an integer between "1" and "8"')
        return False
    if len(str) == 4:
        if str[2] != '=' or str[3] not in ('K', 'B', 'R', 'Q'):
            print(f'[{str}]: Wrong format: =(K, B, R, Q) ')
    return True

def get_instance_first_letter(type):
    if type == PAWN:
        return ''
    elif type == KNIGHT:
        return 'N'
    elif type == BISHOP:
        return 'B'
    elif type == ROOK:
        return 'R'
    elif type == QUEEN:
        return 'Q'
    else:
        return 'K'

def get_piece_type_by_int(type):
    if type == 'Pawn':
        return PAWN
    elif type == 'Knight':
        return KNIGHT
    elif type == 'Bishop':
        return BISHOP
    elif type == 'Rook':
        return ROOK
    elif type == 'Queen':
        return QUEEN
    else:
        return KING

def get_piece_type_by_alphabet(type):
    if type == PAWN:
        return 'Pawn'
    elif type == KNIGHT:
        return 'Knight'
    elif type == BISHOP:
        return 'Bishop'
    elif type == ROOK:
        return 'Rook'
    elif type == QUEEN:
        return 'Queen'
    else:
        return 'King'

def user_input_control():
    buffer = []
    while True:
        ch = msvcrt.getch()
        
        if ch == b'\x1b':  # ESC
            print("ESC Detected!")
            return {"status": False, "buffer": ''}

        if ch == b'\r':  # Enter
            print()
            break

        if ch == b'\x08':  # backspace
            if buffer:
                buffer.pop()
                # 콘솔에서 뒤로 가서 문자 지우기
                sys.stdout.write('\b \b')
                sys.stdout.flush()
            continue

        char = ch.decode('utf-8')
        buffer.append(char)
        sys.stdout.write(char)
        sys.stdout.flush()
    
    buffer = ''.join(buffer)

    return {"status": True, "buffer": buffer}