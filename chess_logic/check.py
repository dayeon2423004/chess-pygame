# chess_logic/check.py
from server.board import copy_board, move_piece
from chess_logic.movement_utils import is_valid_piece_move
from typing import Dict, Tuple, Any

# 제 기물의 왕이 체크인 경우
def is_check(board: Dict[Tuple[int, int], Dict[str, Any]], color: str) -> bool:
    king_pos = None

    # 제 기물의 킹 좌표 구하기
    for pos, piece in board.items():
        if piece["type"] == "king" and piece["color"] == color:
            king_pos = pos
            break
    if not king_pos: # 킹이 없는 경우 에러 방지
        return False 

    # 체크인 경우 True, 체크가 아닌 경우 False.
    for pos, piece in board.items():
        if piece["color"] != color:
            if is_valid_piece_move(board, piece, pos[0], pos[1], king_pos[0], king_pos[1]):
                return True
    return False

# 보드를 복사하여 체크 확인
def would_cause_suicide(board: Dict[Tuple[int, int], Dict[str, Any]], from_x: int, from_y: int, to_x: int, to_y: int, color: str) -> bool:
    temp_board = copy_board(board)
    move_piece(temp_board, from_x, from_y, to_x, to_y)
    return is_check(temp_board, color)

# 체크 메이트 확인
def is_checkmate(board: Dict[Tuple[int, int], Dict[str, Any]], color: str) -> bool:
    if not is_check(board, color):
        return False

    # 체크 당하면서, 이동했을 때 왕이 체크당하는 경우만 True.
    for pos, piece in board.items():
        if piece["color"] != color:
            continue
        for x in range(8):
            for y in range(8):
                if is_valid_piece_move(board, piece, pos[0], pos[1], x, y):
                    if not would_cause_suicide(board, pos[0], pos[1], x, y, color):
                        return False
    return True

# 스테일메이트 확인
def is_stalemate(board: Dict[Tuple[int, int], Dict[str, Any]], color: str) -> bool:
    if is_check(board, color):
        return False

    # 체크 당하지 않으면서, 이동했을 때 왕이 체크당하는 경우만 True.
    for pos, piece in board.items():
        if piece["color"] != color:
            continue
        for x in range(8):
            for y in range(8):
                if is_valid_piece_move(board, piece, pos[0], pos[1], x, y):
                    if not would_cause_suicide(board, pos[0], pos[1], x, y, color):
                        return False
    return True