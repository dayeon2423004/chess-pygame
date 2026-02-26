# chess_logic/pieces/rook.py
from chess_logic.utils import is_straight_move, is_path_clear
from typing import Dict, Tuple, Any


def is_valid_rook_move(board: Dict[Tuple[int, int], Dict[str, Any]], from_x: int, from_y: int, to_x: int, to_y: int) -> bool:
    if is_straight_move(from_x, from_y, to_x, to_y):
        return is_path_clear(board, from_x, from_y, to_x, to_y)

    return False