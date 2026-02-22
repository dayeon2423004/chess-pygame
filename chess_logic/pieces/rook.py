# chess_logic/pieces/rook.py
from chess_logic.utils import is_straight_move, is_path_clear

def is_valid_rook_move(board, from_x, from_y, to_x, to_y):
    if is_straight_move(from_x, from_y, to_x, to_y):
        return is_path_clear(board, from_x, from_y, to_x, to_y)

    return False