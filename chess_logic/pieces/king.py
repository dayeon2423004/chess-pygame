# chess_logic/pieces/queen.py

def is_valid_king_move(from_x: int, from_y: int, to_x: int, to_y: int) -> bool:
    dx = abs(to_x - from_x)
    dy = abs(to_y - from_y)

    return dx <= 1 and dy <= 1