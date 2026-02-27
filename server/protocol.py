# server/protocol.py
from typing import Dict, Any, Tuple, List
import socket
import json


# -------------------------
# 메시지 생성 함수
# -------------------------
def make_join_ok() -> Dict[str, str]:
    return {
        "type": "JOIN_OK"
    }

def make_start(color: str, turn: str) -> Dict[str, str]:
    return {
        "type": "START",
        "color": color,
        "turn": turn
    }

def make_move(data_dict: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "type": "MOVE",
        **data_dict
    }

def make_move_invalid() -> Dict[str, str]:
    return {
        "type": "MOVE_INVALID"
    }

def make_chat(msg: str) -> Dict[str, str]:
    return {
        "type": "CHAT",
        "message": msg
    }

# -------------------------
# 서버 수신
# -------------------------
def recv(server_socket: socket.socket) -> None :
    data, addr = server_socket.recvfrom(32768)
    message = data.decode("utf-8")
    return json.loads(message), addr


# -------------------------
# 서버 송신
# -------------------------
def send(server_socket: socket.socket, addr: Tuple[str, int], data_dict: Dict[str, Any]) -> None:
    message = json.dumps(data_dict)
    server_socket.sendto(message.encode("utf-8"), addr)

def send_all(server_socket: socket.socket, client_list: List[Tuple[str, int]], data_dict: Dict[str, Any]) -> None:
    message = json.dumps(data_dict)
    for client in client_list:
        server_socket.sendto(message.encode("utf-8"), client)