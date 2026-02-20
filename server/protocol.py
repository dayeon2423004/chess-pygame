# server/protocol.py
import json

# 서버 수신
def recv(server_socket):
    data, addr = server_socket.recvfrom(32768)
    message = data.decode("utf-8")
    return json.loads(message), addr  

#  서버 송신
def send(server_socket, addr, data_dict):
    message = json.dumps(data_dict)
    server_socket.sendto(message.encode("utf-8"), addr)