# chess_logic/pieces/queen.py

def is_valid_king_move(from_x, from_y, to_x, to_y):
    dx = abs(to_x - from_x)
    dy = abs(to_y - from_y)

    return dx <= 1 and dy <= 1