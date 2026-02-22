# chess_logic/pieces/bishop.py
from chess_logic.utils import is_diagonal_move, is_path_clear

def is_valid_bishop_move(board, from_x, from_y, to_x, to_y):
    if is_diagonal_move(from_x, from_y, to_x, to_y):
        return is_path_clear(board, from_x, from_y, to_x, to_y)

    return False