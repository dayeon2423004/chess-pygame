# client/protocol.py

from typing import Dict, Any, Tuple

def make_ready() -> Dict[str, str]:
    return {
        "type": "JOIN"
    }

def make_chat(msg: str) -> Dict[str, str]:
    return {
        "type": "CHAT",
        "message": msg
    }

def make_move_request(from_row: int, from_col: int, to_row: int, to_col: int) -> Dict[str, int | str]:
    return {
        "type": "MOVE",
        "from_row": from_row,
        "from_col": from_col,
        "to_row": to_row,
        "to_col": to_col,
    }

# 서버 수신 메시지 해석
def parse_message(data: Dict[str, Any]) -> Tuple[Any, ...]:

    msg_type = data["type"]

    if msg_type == "JOIN_OK":
        return ("JOIN_OK", "상대를 기다리고 있습니다.")

    elif msg_type == "START":
        return ("START", data["color"], data["turn"])

    elif msg_type == "MOVE":
        return ("MOVE", data)

    elif msg_type == "MOVE_INVALID":
        return ("MOVE_INVALID",)

    elif msg_type == "CHAT":
        return ("CHAT", data["message"])

    return ("UNKNOWN",)