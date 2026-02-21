# game/utils.py

# 좌표 계산기 chess_piece(white_rook -> 50, 50)
def chess_find_pos(chess_y, chess_x, player_color):
    # black인 경우 좌표 뒤집기
    if player_color == "black":
        chess_x = 7 - chess_x
        chess_y = 7 - chess_y

    x_original = 50 + chess_x * 100
    y_original = 50 + chess_y * 100

    return (x_original, y_original)                        

# 해당 마우스 (좌표 -> 5, 5)
def mouse_pos(mouse_x, mouse_y, player_color):

    # 체스판을 벗어난 경우
    if not (50 <= mouse_x < 850 and 50 <= mouse_y < 850):
        return None
    
    x = (mouse_x - 50) // 100
    y = (mouse_y - 50) // 100

    # black인 경우 다시 뒤집기
    if player_color == "black":
        x = 7 - x
        y = 7 - y

    return (y, x)