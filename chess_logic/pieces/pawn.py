# pawn.py
from typing import Dict, Tuple, Any

def is_valid_pawn_move(board: Dict[Tuple[int, int], Dict[str, Any]], piece: Dict[str, Any], from_x: int, from_y: int, to_x: int, to_y: int) -> bool:
    if piece["color"] == "white":
        direction = -1  
        start_row = 6   
    else:
        direction = 1  
        start_row = 1   

    dx = to_x - from_x
    dy = to_y - from_y

    # 가로막히지 않는 경우, 전진 1칸
    if dy == 0 and dx == direction and (to_x, to_y) not in board:
        return True

    # 전진 2칸 (첫 이동)
    if (
        from_x == start_row
        and dy == 0
        and dx == 2 * direction
        and (from_x + direction, from_y) not in board
        and (to_x, to_y) not in board
    ):
        return True

    # 대각선 공격
    if abs(dy) == 1 and dx == direction:
        if (to_x, to_y) in board:
            return True

    return False