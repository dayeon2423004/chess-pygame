# board_render.py
import pygame
from .utils import chess_find_pos
from .state import COLORS, CELL_SIZE, BOARD_START

# -------------------
# 1. 테두리 렌더링
# -------------------
def draw_border(screen, start_x, start_y, width, height, brown):
    pygame.draw.rect(screen, brown, (start_x, start_y, width, height), 3)


# -------------------
# 2. 영어 문자 렌더링 
# -------------------
def draw_letters(screen, font, black, player_color):
    for i in range(8):

        # white 기준: A B C D E F G H 정방향
        # if player_color == "white":
        letter = chr(65 + i)
        # else:
        #     # black이면 반대로
        #     letter = chr(65 + (7 - i))

        text = font.render(letter, True, black)

        # 위치 조정
        x = 50 + i * 100 + 35
        screen.blit(text, (x, 858))
        screen.blit(text, (x, 8))

# -------------------
# 3. 숫자 렌더링 
# -------------------
def draw_numbers(screen, font, black, player_color):
    for i in range(8):

        # if player_color == "white":
        number = 8 - i
        # else:
        #     number = i + 1

        text = font.render(str(number), True, black)

        y = 50 + i * 100 + 35

        screen.blit(text, (18, y))  
        screen.blit(text, (865, y))  


# -------------------
# 4. 게임판 렌더링
# -------------------
def draw_board(screen, cream, brown, rect_width, rect_height):
    for row in range(1, 9):
        for col in range(1, 9):
            if (row + col) % 2 == 0:
                pygame.draw.rect(screen, cream, ((rect_width * row) - 50, (rect_height * col) - 50, rect_width, rect_height))
            else:
                pygame.draw.rect(screen, brown, ((rect_width * row) - 50, (rect_height * col) - 50, rect_width, rect_height))


# -------------------
# 5. 선택된 칸 하이라이트
# -------------------
def draw_highlight(screen, green, state, rect_width, rect_height):
    highlight_pos = state["green_board"]
    if highlight_pos:
        pygame.draw.rect(screen, green, (highlight_pos[0], highlight_pos[1], rect_width, rect_height))
        

# -------------------
# 6. 기물 렌더링
# -------------------
def draw_pieces(screen, state):
    board = state["piece"]
    images = state["images"]
    selected = state["selected_piece"]

    for row in range(8):
        for col in range(8):
            
            # 선택된 기물은 렌더링 제외
            if selected == (row, col):
                continue

            piece = board[row][col]

            # key 값이 있는 경우만, key를 이용해 기물 렌더링
            if piece:
                key = f"{piece['color']}_{piece['type']}"
                image = images[key]

                x, y = chess_find_pos(row, col, state['player_color'])
                screen.blit(image, (x, y))


# -------------------
# 7. 모든 렌더링
# -------------------
def render(state):
    screen = state['screen']
    font = state['font']

    screen.fill(COLORS['white'])

    draw_border(screen, BOARD_START, BOARD_START, CELL_SIZE * 8, CELL_SIZE * 8, COLORS["brown"])
    draw_letters(screen, font, COLORS["black"], state["player_color"])
    draw_numbers(screen, font, COLORS["black"], state["player_color"])
    draw_board(screen, COLORS["cream"], COLORS["brown"], CELL_SIZE, CELL_SIZE)
    draw_highlight(screen, COLORS["green"], state, CELL_SIZE, CELL_SIZE)
    draw_pieces(screen, state)

    # 이동 중인 기물은 맨 위에 렌더링
    if state['dragging'] and state['selected_piece']:
        row, col = state["selected_piece"]
        piece = state["piece"][row][col]

        if piece:
            key = f"{piece['color']}_{piece['type']}"
            image = state['images'][key]

            # 새로운 이미지 사각형 객체를 만들어 빌드.
            mouse_x, mouse_y = state["drag_pos"]
            rect = image.get_rect(center=(mouse_x, mouse_y))
            screen.blit(image, rect)