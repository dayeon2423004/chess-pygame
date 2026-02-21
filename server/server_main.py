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
    if data is None:
        continue

    msg_type = data["type"]

    if msg_type == "JOIN":
        game_init.handle_join(server_socket, addr)

    elif msg_type == "MOVE":
        # TODO:
        # 1. 턴 확인
        # 2. 이동 가능 판정
        # 3. 보드 업데이트
        # 4. 양쪽 클라이언트에 MOVE 브로드캐스트
        pass

    elif msg_type == "CHAT":
        # TODO:
        # 상대에게 채팅 전달
        pass