# chess_logic/pieces/queen.py
from chess_logic.pieces.bishop import is_valid_bishop_move
from chess_logic.pieces.rook import is_valid_rook_move
from typing import Dict, Tuple, Any

def is_valid_queen_move(board: Dict[Tuple[int, int], Dict[str, Any]], from_x: int, from_y: int, to_x: int, to_y: int) -> bool:
    return (
        is_valid_rook_move(board, from_x, from_y, to_x, to_y)
        or
        is_valid_bishop_move(board, from_x, from_y, to_x, to_y)
    )