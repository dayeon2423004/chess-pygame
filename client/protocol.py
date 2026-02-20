# client/protocol.py
import json

def make_ready():
    return json.dumps({
        "type": "READY"
    })

def make_chat(msg):
    return json.dumps({
        "type": "CHAT",
        "message": msg
    })

# 서버 수신 메세지 변환
def parse_message(message):
    data = json.loads(message)

    msg_type = data["type"]

    if msg_type == "START":
        return ("START", data["color"])

    elif msg_type == "MOVE":
        return ("MOVE", data)

    elif msg_type == "CHAT":
        return ("CHAT", data["message"])

    return ("UNKNOWN",)