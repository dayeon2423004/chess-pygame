#  server/server_main.py
import socket

# 서버의 IP주소, poth 주소 설정
HOST = '127.0.0.1'
PORT = 12345

# socket : UDP 설정
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

print("서버 실행 중...")

while True:
    # 클라이언트로부터 메세지 수신
    date, client_socket = server_socket.recvfrom(32768)
    message = date.decode('utf-8')
    print(f"client로부터 송신 : {message}")