#  server/server_main.py
# python -m server.server_main
import socket
from server import protocol
from server import game_init
from chess_logic.move_handler import handle_move
from .board import create_board
from .game_init import client_list

# 서버의 IP주소, poth 주소 설정
HOST = '127.0.0.1'
PORT = 12345

# socket : UDP 설정
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

print("서버 실행 중...")

game_state = {
    "board": create_board(),
    "turn": "white"
}

while True:
    data, addr = protocol.recv(server_socket)
    print("받은 메시지:", data)

    msg_type = data["type"]

    if msg_type == "JOIN":
        game_init.handle_join(server_socket, addr)

    elif msg_type == "MOVE":
        result = handle_move(game_state, data["from_row"], data["from_col"], data["to_row"], data["to_col"])

        # flase를 반환 받은 경우, 
        if result["success"] == False:
            protocol.send_all(server_socket, client_list, protocol.make_move_invalid())
        else:
            protocol.send_all(server_socket, client_list, result)

    elif msg_type == "CHAT":
        pass