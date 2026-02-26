# chess_login/validator.py
from typing import Dict, Tuple, Any

# 플레이어 턴이 맞는지 확인
def validate_turn(current_turn: str, piece_color: str) -> bool:
    return current_turn == piece_color

# 같은 칸 선택 방지
def validate_not_same_position(from_x: int, from_y: int, to_x: int, to_y: int) -> bool:
    return (from_x, from_y) != (to_x, to_y)

# 자기 기물 잡는 것 방지
def validate_not_self_capture(board: Dict[Tuple[int, int], Dict[str, Any]], player_color: str, to_x: int, to_y: int) -> bool:
    piece = board.get((to_x, to_y))
    if piece and piece["color"] == player_color:
        return False
    return True

# 이동하려는 위치에 기물이 존재하는지 확인
def validate_piece_exists(board: Dict[Tuple[int, int], Dict[str, Any]], from_x: int, from_y: int) -> bool:
    return (from_x, from_y) in board