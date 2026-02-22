# chess_logic/pieces/queen.py
from chess_logic.pieces.bishop import is_valid_bishop_move
from chess_logic.pieces.rook import is_valid_rook_move

def is_valid_queen_move(board, from_x, from_y, to_x, to_y):
    return (
        is_valid_rook_move(board, from_x, from_y, to_x, to_y)
        or
        is_valid_bishop_move(board, from_x, from_y, to_x, to_y)
    )