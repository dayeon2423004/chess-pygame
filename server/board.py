# server/board.py

# 서버 보드 기물 관리
def create_board():
    block = ["rook", "knight", "bishop", "queen",
            "king", "bishop", "knight", "rook"]

    board = {}
    # black 배치
    for col in range(8):
        board[(0, col)] = {"type": block[col], "color": "black", "moved": False}
        board[(1, col)] = {"type": "pawn", "color": "black", "moved": False}

    # white 배치
    for col in range(8):
        board[(7, col)] = {"type": block[col], "color": "white", "moved": False}
        board[(6, col)] = {"type": "pawn", "color": "white", "moved": False}

    return board

# key값을 이용해 해당 보드 정보 값 가져오기
def get_piece(board, from_x, from_y):
    return board.get((from_x, from_y))

# 이동하려는 칸에 기물이 있는지 확인
def has_piece(board, to_x, to_y):
    return (to_x, to_y) in board

# 이동 확정하는 경우 키 값 변경
def move_piece(board, from_x, from_y, to_x, to_y):
    piece = board.pop((from_x, from_y))
    board[(to_x, to_y)] = piece

# 기물을 잡을 경우
def remove_piece(board, to_x, to_y):
    if (to_x, to_y) in board:
        del board[(to_x, to_y)]

import copy

# 체크 / 체크메이트 계산을 위하여 현재 보드 복사
def copy_board(board):
    return copy.deepcopy(board)