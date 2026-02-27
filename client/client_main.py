# client/client_main.py
# python -m client.client_main
from client.network import start_network, recv_queue, send_queue
from client import protocol
from game.state import create_game_state
from game.game_loop import run
from typing import Any, Dict, Tuple

# 클라이언트 state 생성
state: Dict[str, Any] = create_game_state()

# 비동기 통신 시작
start_network()

# print("게임 참가를 위해 아무 메시지 입력")
# input("서버에 보낼 메시지: ")

ready = protocol.make_ready()
send_queue.put(ready)

while True:
    if not recv_queue.empty():
        message = recv_queue.get()
        result: Tuple[Any, ...] = protocol.parse_message(message)

        if result[0] == "JOIN_OK":
            print(result[1])

        elif result[0] == "START":
            my_color = result[1]
            print(f"게임 시작! 당신은 {my_color} 입니다.", state['turn'])
            state["player_color"] = my_color
            state["turn"] = result[2]
            
            # 게임 루프 시작
            run(state)

        elif result[0] == "MOVE":
            move_data = result[1]
            state["turn"] = move_data["next_turn"]
            # 보드 상태 갱신

        elif result[0] == "MOVE_INVALID":
            print("잘못된 이동입니다.")

        elif result[0] == "CHAT":
            print(result[1])