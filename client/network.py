# client/network.py

import socket
import threading
import json
from queue import Queue

# 클라이언트 소켓 / 서버 주소
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_addr = ("127.0.0.1", 12345)

recv_queue = Queue()
send_queue = Queue()

# 서버로부터 데이터 수신
def server_recv():
    while True:
        data, _ = client_socket.recvfrom(32768)
        message = data.decode("utf-8")
        parsed = json.loads(message)
        recv_queue.put(parsed)

# 서버로 송신
def send_message():
    while True:
        message = send_queue.get()
        json_data = json.dumps(message)
        client_socket.sendto(json_data.encode("utf-8"), server_addr)

# 비동기 통신
def start_network():
    threading.Thread(target=server_recv, daemon=True).start()
    threading.Thread(target=send_message, daemon=True).start()