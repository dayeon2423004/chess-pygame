# game/utils.py

# 좌표 계산기 chess_piece(white_rook -> 1, 1)
def chess_find_pos(chess_y, chess_x):
    if player_color == "black":
        chess_x = (9 - chess_x)
        chess_y = (9 - chess_y)

    y_original = 50
    for y in range(1, 9):
        if y != 1:
            y_original += 100
        for x in range(1, 9):
            if x == 1:
                x_original = 50
            else:
                x_original += 100
                     
            if chess_x == x and chess_y == y:      
                return (x_original, y_original)                           

# 해당 마우스의 좌표
def mouse_pos(mouse_x, mouse_y):
    y_pos = 50
    for y in range(1, 9):
        if y != 1:
            y_pos += 100
        for x in range(1, 9): 
            if x == 1:
                x_pos = 50
            else:
                x_pos += 100
            if x_pos <= mouse_x < x_pos + 100 and y_pos <= mouse_y < y_pos + 100:
                return (x, y) 