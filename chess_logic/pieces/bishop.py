# chess_logic/pieces/bishop.py
from chess_logic.utils import is_diagonal_move, is_path_clear
from typing import Dict, Tuple, Any

def is_valid_bishop_move(board: Dict[Tuple[int, int], Dict[str, Any]], from_x: int, from_y: int, to_x: int, to_y: int) -> bool:
    if is_diagonal_move(from_x, from_y, to_x, to_y):
        return is_path_clear(board, from_x, from_y, to_x, to_y)

    return False