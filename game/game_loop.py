# game/game_loop.py
from .input_handler import handle_events
from .board_render import render
from client.network import recv_queue
from client import protocol
from typing import Dict, Any
import pygame


# 상태 업데이트
def update_board(state: Dict[str, Any], data: Dict[str, Any]) -> None:
    from_x, from_y = data["from"]
    to_x, to_y = data["to"]

    board = state["piece"]

    piece = board[from_x][from_y]
    board[from_x][from_y] = None
    board[to_x][to_y] = piece

    # 턴 관리
    state["turn"] = data["next_turn"]

    # 드래그 상태 초기화
    state["selected_piece"] = None
    state["dragging"] = False
    state["drag_pos"] = None

    print("서버의 메세지", data)

# 게임 루프
def run(state: Dict[str, Any]) -> None:
    clock = pygame.time.Clock()
    running = True

    while running:

        # 네트워크 메시지 처리
        while not recv_queue.empty():
            message = recv_queue.get()
            result = protocol.parse_message(message)

            if result[0] == "MOVE":
                data = result[1]
                if data["success"]:
                    update_board(state, data)

            elif result[0] == "MOVE_INVALID":
                print("잘못된 이동입니다.")

        # 이벤트 처리
        running = handle_events(state)

        # 렌더링
        render(state)
        pygame.display.flip()

        clock.tick(60)