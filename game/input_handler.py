# input_handler.py
import pygame
from typing import Dict, Any
from client.protocol import make_move_request
from client.network import send_queue
from game.utils import mouse_pos


# -------------------------
# 전체 이벤트
# -------------------------
def handle_events(state: Dict[str, Any]) -> bool:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            return False   # 게임 종료

        if event.type == pygame.MOUSEBUTTONDOWN:
            handle_mouse_down(event, state)

        if event.type == pygame.MOUSEBUTTONUP:
            handle_mouse_up(event, state)

        if event.type == pygame.MOUSEMOTION:
            handle_mouse_motion(event, state)

    return True


# -------------------------
# 마우스 클릭
# -------------------------
def handle_mouse_down(event: pygame.event.Event, state: Dict[str, Any]) -> None:
    if state["player_color"] != state["turn"]:
        return

    # 마우스 좌표 변환
    mouse_x, mouse_y = event.pos
    pos = mouse_pos(mouse_x, mouse_y, state["player_color"])

    # 만일, 0 ~ 7 이외의 값인 경우
    if pos is None:
        state["selected_piece"] = None
        return
    
    row, col = pos
    piece = state["piece"][row][col]

    # 마우스로 선택한 보드에 해당 피스가 있다면 해당 좌표를, 없다면 None 반환
    if piece and piece["color"] == state["player_color"]:
        state["selected_piece"] = (row, col)
        state["dragging"] = True
        state["drag_pos"] = event.pos
    else:
        state["selected_piece"] = None


# -------------------------
# 마우스 이동
# -------------------------
def handle_mouse_motion(event: pygame.event.Event, state: Dict[str, Any]) -> None:
    if state["dragging"]:
        state["drag_pos"] = event.pos

# -------------------------
# 마우스 클릭 해제
# -------------------------
def handle_mouse_up(event: pygame.event.Event, state: Dict[str, Any]) -> None:
    if state["player_color"] != state["turn"]:
        return
    if state["selected_piece"] is None:
        return
    
    # 마우스 좌표, 선택 기물 좌표 통일
    start_row, start_col = state["selected_piece"]
    mouse_x, mouse_y = event.pos
    pos = mouse_pos(mouse_x, mouse_y, state["player_color"])

    # 만일, 0 ~ 7 이외의 값인 경우
    if pos is None:
        state["selected_piece"] = None
        return
    move_row, move_col = pos

    # 같은 칸인 경우, 취소
    if (start_row, start_col) == (move_row, move_col):
        state["selected_piece"] = None
        return

    # 서버 전송
    move_data = make_move_request(start_row, start_col, move_row, move_col)
    send_queue.put(move_data)

    # 드래그 종료
    state["dragging"] = False
    state["selected_piece"] = None
    state["drag_pos"] = None