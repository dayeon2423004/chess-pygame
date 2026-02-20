# state.py
import pygame

# -------------------------
# 색상 정의
# -------------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BEIGE = (255, 255, 230)
BROWN = (210, 139, 73)
CREAM = (254, 206, 158)

RECT_SIZE = 100


# -------------------------
# 게임 상태 생성
# -------------------------
def create_game_state():
       return {
       "pieces": [],           
       "selected_piece": None,
       "mouse_pos": (None, None),
       "turn": "white",
       "board_highlight": [],
       "player_color": None,
       }


# -------------------------
# 이미지 로드
# -------------------------
def load_piece_images():
       pieces = {}
       colors = ["white", "black"]
       names = ["king", "queen", "rook", "bishop", "knight", "pawn"]

       for color in colors:
              for name in names:
                     path = f"piece_image/{color}_{name}_resize.png"
                     pieces[f"{color}_{name}"] = pygame.image.load(path)

       return pieces


# -------------------------
# 초기 기물 배치
# -------------------------
def create_board():
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