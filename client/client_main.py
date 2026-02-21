# client/client_main.py

from client.network import start_network, recv_queue, send_queue, client_socket
import client.protocol as protocol
from game import state
import game.game as game

print("게임 참가를 위해 아무 메시지 입력")
msg = input("서버에 보낼 메시지: ")
ready = protocol.make_ready()
client_socket.sendto(ready.encode("utf-8"), ("127.0.0.1", 12345))

# 비동기 통신 시작
start_network()

while True:
    if not recv_queue.empty():
        message = recv_queue.get()
        result = protocol.parse_message(message)

        if result[0] == "JOIN_OK":
            print(result[1])

        elif result[0] == "START":
            my_color = result[1]
            print(f"게임 시작! 당신은 {my_color} 입니다.")
            state["player_color"] = my_color
            state["turn"] = result[2]
            # game.chess(send_queue, recv_queue)

        elif result[0] == "MOVE":
            move_data = result[1]
            state["turn"] = move_data["next_turn"]
            # 보드 상태 갱신

        elif result[0] == "MOVE_INVALID":
            print("잘못된 이동입니다.")

        elif result[0] == "CHAT":
            print(result[1])