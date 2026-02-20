# client/client_main.py

from client.network import start_network, recv_queue, send_queue, client_socket
import client.protocol as protocol
import game.game as game

print("게임 참가를 위해 아무 메시지 입력")
msg = input("서버에 보낼 메시지: ")
client_socket.sendto(msg.encode("utf-8"), ("127.0.0.1", 12345))

# 비동기 통신 시작
start_network()

while True:
    # 만일 서버에서 메세지가 왔다면 메세지 변환 함수를 통해 
    if not recv_queue.empty():
        message = recv_queue.get()

        result = protocol.parse_message(message)

        if result[0] == "START":
            my_color = result[1]
            game.player_color = my_color
            game.chess(send_queue, recv_queue)