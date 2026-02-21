# server/protocol.py
import json


# -------------------------
# 메시지 생성 함수
# -------------------------
def make_join_ok():
    return {
        "type": "JOIN_OK"
    }

def make_start(color, turn):
    return {
        "type": "START",
        "color": color,
        "turn": turn
    }

def make_move(data_dict):
    return {
        "type": "MOVE",
        **data_dict
    }

def make_move_invalid():
    return {
        "type": "MOVE_INVALID"
    }

def make_chat(msg):
    return {
        "type": "CHAT",
        "message": msg
    }

# -------------------------
# 서버 수신
# -------------------------
def recv(server_socket):
    data, addr = server_socket.recvfrom(32768)
    message = data.decode("utf-8")
    return json.loads(message), addr


# -------------------------
# 서버 송신
# -------------------------
def send(server_socket, addr, data_dict):
    message = json.dumps(data_dict)
    server_socket.sendto(message.encode("utf-8"), addr)