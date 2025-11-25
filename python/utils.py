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