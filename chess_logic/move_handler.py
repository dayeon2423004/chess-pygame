# chess_logic/move_handler.py
from chess_logic.validator import validate_piece_exists, validate_turn
from server.board import get_piece, move_piece, remove_piece
from chess_logic.movement_utils import is_valid_piece_move
from chess_logic.check import would_cause_suicide, is_checkmate, is_stalemate, is_check
from typing import Dict, Tuple, Any


# --------------------------
# 서버 규칙 검증 함수
# --------------------------
def handle_move(game_state: Dict[str, Any], from_x: int, from_y: int, to_x: int, to_y: int) -> Dict[str, Any]:
    current_turn = game_state["turn"]
    board = game_state['board']

    # 기물 존재 확인
    if not validate_piece_exists(board, from_x, from_y):
        return {"success": False}

    # 현 기물 정보
    piece = get_piece(board, from_x, from_y)

    # 턴 검증
    if not validate_turn(current_turn, piece["color"]):
        return {"success": False}
    
    # 임시 보드판으로 체크받는지 확인
    if would_cause_suicide(board, from_x, from_y, to_x, to_y,  piece['color']):
        return {"success": False}

    # 이동 가능 계산
    if not is_valid_piece_move(board, piece, from_x, from_y, to_x, to_y):
        return {"success": False}
    
    # 앙파상 처리
    if piece["type"] == "pawn":
        dy = to_y - from_y
        # 대각선 + 빈칸이면 앙파상 시도
        if abs(dy) == 1 and (to_x, to_y) not in board:
            if not handle_en_passant(board, piece, from_x, from_y, to_x, to_y):
                return {"success": False}

    # 캐슬링 처리
    if piece["type"] == "king" and abs(to_y - from_y) == 2:
        if to_y > from_y:
            rook_pos = (from_x, 7)
        else:
            rook_pos = (from_x, 0)

        # 캐슬링 시도
        if handle_can_castle(board, (from_x, from_y), rook_pos):
            perform_castling(board, (from_x, from_y), rook_pos)
        else:
            return {"success": False}
    else:
        # 이동 확정
        move_piece(board, from_x, from_y, to_x, to_y)
        piece["moved"] = True

    # 폰 프로모션
    if piece["type"] == "pawn":
        handle_pawn_promotion(board, piece, to_x, to_y)

    # 턴 변경
    if current_turn == "white":
        game_state["turn"] = "black"
    else :
        game_state["turn"] = "white"

    # 현 상태 반환
    if is_checkmate(board, game_state["turn"]):
        status = "checkmate"
    elif is_stalemate(board, game_state["turn"]):
        status = "stalemate"
    else:
        status = "normal"

    return {
        "type": "MOVE",
        "success": True,
        "from": (from_x, from_y),
        "to": (to_x, to_y),
        "next_turn": game_state["turn"],
        "status": status
    }


# --------------------------
# 특수 규칙 함수
# --------------------------

# 폰 프로모션
def handle_pawn_promotion(board: Dict[Tuple[int, int], Dict[str, Any]], piece: Dict[str, Any], to_x: int, to_y: int, promote_to="queen") -> None:
    color = piece["color"]

    if (color == "white" and to_x == 0) or (color == "black" and to_x == 7):
        board[(to_x, to_y)] = {
            "type": promote_to,
            "color": color,
            "moved": True
        }

# 앙파상 
def handle_en_passant(board: Dict[Tuple[int, int], Dict[str, Any]], piece: Dict[str, Any], from_x: int, from_y: int, to_x: int, to_y: int) -> bool:

    # 내 폰이 대각선 이동했는지
    dx = to_x - from_x
    dy = to_y - from_y

    if piece["color"] == "white":
        direction = -1  
    else :
        direction = 1

    # 대각선 이동, 이동 칸 비어있는 경우
    if ((dx == direction and abs(dy) == 1) and ((to_x, to_y) not in board)):
        captured_pawn_pos = (from_x, to_y)
        captured_pawn = board.get(captured_pawn_pos)

        # 타겟 기물이 pawn이고, 같은 기물 색이 아닌 경우 위치가 맞는 경우.
        if captured_pawn and captured_pawn["type"] == "pawn" and captured_pawn["color"] != piece["color"]:
            if captured_pawn["color"] == "white":
                if from_x == 3:
                    remove_piece(board, from_x, to_y)
                    return True
            else:
                if from_x == 4:
                    remove_piece(board, from_x, to_y)
                    return True
    
    return False

# 캐슬링 검증 함수
def handle_can_castle(board: Dict[Tuple[int, int], Dict[str, Any]], king_pos: Tuple[int, int], rook_pos: Tuple[int, int]) -> bool:
    king = board.get(king_pos)
    rook = board.get(rook_pos)

    if not king or not rook:
        return False
    
    # 킹이 현재 체크 상태면 불가
    if is_check(board, king["color"]):
        return False

    # 캐슬링 가능한 위치에 있는 것이 킹/룩이 아니거나, 첫 이동이 False가 아닌 경우
    if king["type"] != "king" or rook["type"] != "rook":
        return False
    if king["moved"] or rook["moved"]:
        return False
    
    king_x, king_y = king_pos
    rook_x, rook_y = rook_pos

    # 사이 칸 체크
    if rook_y > king_y:
        step = 1 
    else : 
        step = -1

    # 킹 좌표 - 룩 좌표 사이 기물이 없는 경우 가능.
    for y in range(king_y + step, rook_y, step):
        if (king_x, y) in board:
            return False

    return True

# 캐슬링 진행
def perform_castling(board: Dict[Tuple[int, int], Dict[str, Any]], king_pos: Tuple[int, int], rook_pos: Tuple[int, int]) -> None:
    king = board.pop(king_pos)
    rook = board.pop(rook_pos)

    king_x, king_y = king_pos
    rook_x, rook_y = rook_pos

    if rook_y > king_y:
        # 킹사이드
        new_king_pos = (king_x, king_y + 2)
        new_rook_pos = (king_x, king_y + 1)
    else:
        # 퀸사이드
        new_king_pos = (king_x, king_y - 2)
        new_rook_pos = (king_x, king_y - 1)

    board[new_king_pos] = king
    board[new_rook_pos] = rook

    king["moved"] = True
    rook["moved"] = True