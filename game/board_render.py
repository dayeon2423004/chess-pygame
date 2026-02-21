# board_render.py
import pygame
from utils import chess_find_pos
from state import COLORS, CELL_SIZE, BOARD_START

# -------------------
# 1. 테두리 렌더링
# -------------------
def draw_border(screen, start_x, start_y, width, height, brown):
    pygame.draw.rect(screen, brown, (start_x, start_y, width, height), 3)


# -------------------
# 2. 영어 문자 렌더링
# -------------------
def draw_letters(screen, font, black, rect_width):
    eng_f = 0
    for eng in range(65, 73):
        font_render = font.render(chr(eng), True, black)
        flipped_letter = pygame.transform.flip(font_render, True, True)  # 수평, 수직으로 뒤집기
        screen.blit(font_render, (rect_width - 15 + eng_f, 858))
        screen.blit(flipped_letter, (rect_width - 15 + eng_f, 8))
        eng_f += 100

# -------------------
# 3. 숫자 렌더링
# -------------------
def draw_numbers(font, black, screen, rect_width):
    num_f = 0
    for num in range(8, 0, -1):
        font_render2 = font.render(str(num), True, black) # True는 부드럽게 텍스트를 렌더링 하는 역할.
        flipped_letter2 = pygame.transform.flip(font_render2, True, True)  # 수평, 수직으로 뒤집기
        screen.blit(font_render2, (18, rect_width - 15 + num_f))
        screen.blit(flipped_letter2, (865, rect_width - 15 + num_f))
        num_f += 100


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

                x, y = chess_find_pos(col, row, state['player_color'])
                screen.bilt(image, (x, y))


# -------------------
# 7. 모든 렌더링
# -------------------
def render(state):
    screen = state['screen']
    font = state['font']

    screen.fill(COLORS['white'])

    draw_border(screen, BOARD_START, BOARD_START, CELL_SIZE * 8, CELL_SIZE * 8, COLORS["borwn"])
    draw_letters(screen, font, COLORS["black"], BOARD_START)
    draw_numbers(font, COLORS["black"], screen, BOARD_START)
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

            