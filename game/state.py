# state.py
import pygame
from typing import Dict, Any, List, Tuple, Optional

# =========================
# 전역 환경 설정
# =========================

# 화면 설정
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900

# 보드 설정
CELL_SIZE = 100
BOARD_START = 50

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BROWN = (210, 139, 73)
CREAM = (254, 206, 158)

COLORS = {
    "white": WHITE,
    "black": BLACK,
    "green": GREEN,
    "brown": BROWN,
    "cream": CREAM,
}


# -------------------------
# 이미지 로드
# -------------------------
def load_piece_images() -> Dict[str, pygame.Surface]:
       pieces = {}
       colors = ["white", "black"]
       names = ["king", "queen", "rook", "bishop", "knight", "pawn"]

       for color in colors:
              for name in names:
                     path = f"piece_image/{color}_{name}_resize.png"
                     pieces[f"{color}_{name}"] = pygame.image.load(path)

       return pieces


# -------------------------
# 초기 기물 배치 (y, x)
# -------------------------
def create_piece() -> List[List[Optional[Dict[str, Any]]]]:
    # 보드 생성
    board = []

    for _ in range(8):
        row_list = []  
        for _ in range(8):
            row_list.append(None)
        board.append(row_list)

    # 말 배치 순서
    block = ["rook", "knight", "bishop", "queen",
                "king", "bishop", "knight", "rook"]

    # black 배치
    for col in range(8):
        board[0][col] = {"type": block[col], "color": "black", "moved": False}
        board[1][col] = {"type": "pawn", "color": "black", "moved": False}

    # white 배치
    for col in range(8):
        board[7][col] = {"type": block[col], "color": "white", "moved": False}
        board[6][col] = {"type": "pawn", "color": "white", "moved": False}

    return board

# pieces[board['color']_board['type']] = piece img


# -------------------------
# 게임 상태 생성
# -------------------------
def create_game_state() -> Dict[str, Any]:

    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pygame.font.SysFont(None, 35)

    return {
        # 화면 관련
        "screen": screen,
        "font": font,

        # 피스 관련
        "piece": create_piece(),

        # 게임 상태
        "selected_piece": None,
        "dragging": False,
        "drag_pos": (0, 0),
        "green_board": None,
        "turn": "white",
        "player_color": "white",

        # 이미지
        "images": load_piece_images(),
    }