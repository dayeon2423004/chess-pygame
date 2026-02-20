#  server/server_main.py
import socket
import protocol
import game_init

# 서버의 IP주소, poth 주소 설정
HOST = '127.0.0.1'
PORT = 12345

# socket : UDP 설정
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

print("서버 실행 중...")

while True:
    data, addr = protocol.recv(server_socket)
    
    # 데이터 없는 경우
    if data is None:
        continue
    
    # 참가 메세지
    msg_type = data["type"]

    if msg_type == "JOIN":
        game_init.handle_join(server_socket, addr)

    elif msg_type == "MOVE":
        game_init.handle_turn(server_socket)