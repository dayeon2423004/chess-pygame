# utils.py
from server.board import has_piece
from chess_logic.pieces.bishop import is_valid_bishop_move
from chess_logic.pieces.rook import is_valid_rook_move
from chess_logic.pieces.pawn import is_valid_pawn_move
from chess_logic.pieces.knight import is_valid_knight_move
from chess_logic.pieces.queen import is_valid_queen_move
from chess_logic.pieces.king import is_valid_king_move

# 보드 범위 안인지 확인 
def is_inside_board(x, y):
    return 0 <= x <= 7 and 0 <= y <= 7

# 대각선 이동 확인
def is_diagonal_move(from_x, from_y, to_x, to_y):
    return abs(from_x - to_x) == abs(from_y - to_y)

# 직선 이동 확인
def is_straight_move(from_x, from_y, to_x, to_y):
    return from_x == to_x or from_y == to_y

# 나이트 이동 확인
def is_knight_move(from_x, from_y, to_x, to_y):
    dx = abs(from_x - to_x)
    dy = abs(from_y - to_y)
    return (dx == 2 and dy == 1) or (dx == 1 and dy == 2)

# 상하좌우 방향 계산(룩, 비숍, 퀸)
def get_direction(from_x, from_y, to_x, to_y):
    dx = to_x - from_x
    dy = to_y - from_y

    # step_x
    if dx == 0: # 좌우 이동
        step_x = 0
    elif dx > 0: # 아래로 이동
        step_x = 1
    else: # 위로 이동
        step_x = -1

    # step_y
    if dy == 0: # 상하 이동
        step_y = 0
    elif dy > 0: # 우로 이동
        step_y = 1
    else: # 좌로 이동
        step_y = -1

    return step_x, step_y

# 좌표 이동 거리 계산
def get_distance(from_x, from_y, to_x, to_y):
    return abs(from_x - to_x), abs(from_y - to_y)

# 경로가 비어있는지 시뮬레이션
def is_path_clear(board, from_x, from_y, to_x, to_y):
    step_x, step_y = get_direction(from_x, from_y, to_x, to_y)

    x = from_x + step_x
    y = from_y + step_y

    # 중간에 기물이 보드에 있는지 도착까지 검사 
    while (x, y) != (to_x, to_y):
        if has_piece(board, x, y):
            return False
        x += step_x
        y += step_y

    return True

# 각 기물별 이동 가능 판별 함수
def is_valid_piece_move(board, piece, from_x, from_y, to_x, to_y):
    if piece["type"] == "pawn":
        return is_valid_pawn_move(board, piece, from_x, from_y, to_x, to_y)
    elif piece["type"] == "rook":
        return is_valid_rook_move(board, piece, from_x, from_y, to_x, to_y)
    elif piece["type"] == "knight":
        return is_valid_knight_move(board, piece, from_x, from_y, to_x, to_y)
    elif piece["type"] == "bishop":
        return is_valid_bishop_move(board, piece, from_x, from_y, to_x, to_y)
    elif piece["type"] == "queen":
        return is_valid_queen_move(board, piece, from_x, from_y, to_x, to_y)
    elif piece["type"] == "king":
        return is_valid_king_move(board, piece, from_x, from_y, to_x, to_y)
    return False