def convert_str_to_num(str):
    x, y = 8 - int(str[1]), ord(str[0]) - ord('a')
    # print('x, y: ', x, y)
    return (x, y)

def convert_num_to_str(x, y):
    nx, ny = str(8 - x), chr(ord('a') + y)
    return f'{ny}{nx}'