class Piece:
    def __init__(self, side, x, y):
        self.total_dirs = {
            i: [(dx * step, dy * step) for step in range(1, 8)]
            for i, (dx, dy) in enumerate([
                (0, 1),   # ↑
                (1, 1),   # ↗
                (1, 0),   # →
                (1, -1),  # ↘
                (0, -1),  # ↓
                (-1, -1), # ↙
                (-1, 0),  # ←
                (-1, 1),  # ↖
            ])
        }
        self.dirs = {
            0: [(x, 1) for x in range(-1, 2)],
            1: [(x, -1) for x in range(-1, 2)],
        }[side]
        self.side = side
        self.x = x
        self.y = y

    def possible_move(self):
        for dx, dy in self.dirs:
            nx = self.x + dx
            ny = self.y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                print(f'possible_move: {nx, ny}')