from chess_logic.pieces.bishop import is_valid_bishop_move
from chess_logic.pieces.rook import is_valid_rook_move
from chess_logic.pieces.pawn import is_valid_pawn_move
from chess_logic.pieces.knight import is_valid_knight_move
from chess_logic.pieces.queen import is_valid_queen_move
from chess_logic.pieces.king import is_valid_king_move

# 각 기물별 이동 가능 판별 함수
def is_valid_piece_move(board, piece, from_x, from_y, to_x, to_y):
    if piece["type"] == "pawn":
        return is_valid_pawn_move(board, piece, from_x, from_y, to_x, to_y)
    elif piece["type"] == "rook":
        return is_valid_rook_move(board, from_x, from_y, to_x, to_y)
    elif piece["type"] == "knight":
        return is_valid_knight_move(from_x, from_y, to_x, to_y)
    elif piece["type"] == "bishop":
        return is_valid_bishop_move(board, from_x, from_y, to_x, to_y)
    elif piece["type"] == "queen":
        return is_valid_queen_move(board, from_x, from_y, to_x, to_y)
    elif piece["type"] == "king":
        return is_valid_king_move(from_x, from_y, to_x, to_y)
    return False