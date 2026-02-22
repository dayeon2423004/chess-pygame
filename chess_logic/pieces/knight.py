# chess_logic/pieces/queen.py
from chess_logic.utils import is_knight_move

def is_valid_knight_move(from_x, from_y, to_x, to_y):
    return is_knight_move(from_x, from_y, to_x, to_y)