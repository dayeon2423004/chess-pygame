# 룩, 비숍, 퀸(상대의)
def chess_check_list_pos(chess_board, check_list, player_color):
    for key, value in chess_board.items():
        if value[1] == "king" and value[2] == player_color:
            king_x, king_y = key
            break
    for key in check_list.keys():
        x, y = check_list[key]
        piece = check_list[key][1]

    # 저장할 좌표 리스트
    pos_list = []
    
    # 상대 피스가 갈 수 있는 좌표 전부 구한 다음, 위에 내가 고른 좌표의 to_에 넣어보고 되면 O, 안되면 X.
    if piece == "rook":
        if y == king_y:  # 좌우로 움직일 경우
            if x < king_x:
                for x in range(x + 1, king_x + 1): # step이 +일 경우, from_x 수는 제외하고 -일 경우 to_x의 값도 볼 수 있도록 조정
                    pos_list.append((x, y))
            elif x > to_x:
                for x in range(x + 1, king_x + 1, -1): # step이 +일 경우, from_x 수는 제외하고 -일 경우 to_x의 값도 볼 수 있도록 조정
                    pos_list.append((x, y))
        elif x == king_x:    # 위아래로 움직일 경우
            if y > king_y:
                for y in range(y + 1, king_y + 1, -1): # step이 +일 경우, from_x 수는 제외하고 -일 경우 to_x의 값도 볼 수 있도록 조정
                    pos_list.append((x, y))
            elif y < king_y:
                for y in range(y + 1, king_y + 1): # step이 +일 경우, from_x 수는 제외하고 -일 경우 to_x의 값도 볼 수 있도록 조정
                    pos_list.append((x, y))
    elif piece == "bishop":
        if abs(x - king_x) == abs(y - king_y):    # x와 y의 이동 칸 수 동일 시
            num = abs(x - king_x) # 이동 칸 수 확인
            x_direction = bishop_find_direction(x, king_x)
            y_direction = bishop_find_direction(y, king_y)
            
            for num in range(1, abs(x - king_x)):
                x = from_x + (num * x_direction)
                y = from_y + (num * y_direction)
                pos_list.append(x, y)
    elif piece == "queen":
        if y == king_y:  # 좌우로 움직일 경우
            if x < king_x:
                for x in range(x + 1, king_x + 1): # step이 +일 경우, from_x 수는 제외하고 -일 경우 to_x의 값도 볼 수 있도록 조정
                    pos_list.append((x, y))
            elif x > to_x:
                for x in range(x + 1, king_x + 1, -1): # step이 +일 경우, from_x 수는 제외하고 -일 경우 to_x의 값도 볼 수 있도록 조정
                    pos_list.append((x, y))
        elif x == king_x:    # 위아래로 움직일 경우
            if y > king_y:
                for y in range(y + 1, king_y + 1, -1): # step이 +일 경우, from_x 수는 제외하고 -일 경우 to_x의 값도 볼 수 있도록 조정
                    pos_list.append((x, y))
            elif y < king_y:
                for y in range(y + 1, king_y + 1): # step이 +일 경우, from_x 수는 제외하고 -일 경우 to_x의 값도 볼 수 있도록 조정
                    pos_list.append((x, y))
        elif abs(x - king_x) == abs(y - king_y):    # x와 y의 이동 칸 수 동일 시
            num = abs(x - king_x) # 이동 칸 수 확인
            x_direction = bishop_find_direction(x, king_x)
            y_direction = bishop_find_direction(y, king_y)
            
            for num in range(1, abs(x - king_x)):
                x = from_x + (num * x_direction)
                y = from_y + (num * y_direction)
                pos_list.append(x, y)
    return pos_list

# 폰의 이동 경로(한 칸 전진, 두 칸 전진, 기물 잡기)
def pawn_move_remove(status_flag, chess_board, from_x, from_y, to_x, to_y, num, enemy_pawn_list, player_color):
    move_msg = ""
    # 첫 턴일 경우 2칸 + 앞에 기물이 없는 경우
    if status_flag == True:
        if ((to_x == from_x and to_y == from_y - 2 * num) or (to_x == from_x and to_y == from_y - num)) and chess_board[(to_x, to_y)][1] == None:
            if (to_x == from_x and to_y == from_y - 2 * num):
                enemy_pawn_list.update({(to_x, to_y) : [player_color, (from_x, from_y)]})
            move_msg = "FIRST_MOVE"
    # 두번째 턴일 경우 1칸 + 앞에 기물이 없는 경우
    elif status_flag == False:
        if to_x == from_x and to_y == from_y - num and chess_board[(to_x, to_y)][1] == None:
            # 만일 에너미 폰 리스트에 있는 경우 삭제
            if (from_x, from_y) in enemy_pawn_list:
                if player_color == enemy_pawn_list[(from_x, from_y)][0]:
                    del enemy_pawn_list[(from_x, from_y)]
            move_msg = "MOVE"
    # 기물 잡을 수 있는 경우
    elif abs(to_x - from_x) == 1 and to_y == from_y - num: # abs() 절대값 반환 함수 GPT 도움 받아 작성
        if(to_x, to_y) in chess_board:
            if (chess_board[to_x, to_y][1] is not None) and player_color != chess_board[to_x, to_y][2]:
                move_msg = "REMOVE"
    return move_msg

def king_move_find_check(chess_board, player_color):
    king_x = None
    king_y = None
    for key, value in chess_board.items():
        # value가 None이거나, 길이가 3보다 작으면 건너뜀
        if not value or len(value) < 3:
            continue
        if chess_board[key][1].lower() == "king" and chess_board[key][2].lower() == player_color.lower():
                king_x, king_y = key
                break


    king_check_list = {}
    dic = king_move_find_pos(chess_board, king_x, king_y-1, player_color) # 다른 색이 자리에 있을 경우
    dic2 = king_move_find_pos(chess_board, king_x, king_y, player_color)
    dic3 = king_move_find_pos(chess_board, king_x, king_y+1, player_color)
    king_check_list.update(dic)
    king_check_list.update(dic2)
    king_check_list.update(dic3)
    return king_check_list

# 킹 이동 시뮬레이션 - 1, 기물 + 킹 좌표 찾기
def king_move_find_pos(chess_board, king_x, king_y, player_color):
    king_check_list = {}
    for x in range(king_x-1, king_x+2):

        if x == king_x:
            continue
        # 보드 속 모든 다른 색 기물의 위치 가져오기
        for key, value in chess_board.items():
            if value[2] == player_color:    # 같은 색이면 건너 뛰기
                continue
            elif chess_board[key][1] is not None:
                piece_x, piece_y = key
                piece = chess_board[key][1]
                piece_color = chess_board[key][2]
                # 시뮬레이션 함수 호출
                check_flag = king_move_simulation(piece, piece_x, piece_y, x, king_y, piece_color)
                king_check_list.update({(x, king_y) : [piece, check_flag, piece_color]})
    return king_check_list

# 킹 시뮬레이션 - 킹 자살 수 방지, 체크 메이트 확인, 스테일 메이트 확인 시 필요 (+ 아군 기물로 확인 할 때에도)
def king_move_simulation(piece, piece_x, piece_y, king_x, king_y, piece_color):
    check_flag = False
    move_msg = ""
    # pawn인 경우
    if piece == "pawn":
        # piece의 컬러에 따라 num 위치 변경 필요
        num = None
        if piece_color == "white":     # gpt 도움 받아 로직 작성
            num = 1
        else:
            num = -1
        # pawn인 경우
        if selected_piece == "pawn":
            move_msg = pawn_move_remove(status_flag, chess_board, from_x, from_y, to_x, to_y, num, enemy_pawn_list, player_color)

            if move_msg == "MOVE" or move_msg == "REMOVE":
                check_flag = True

    elif piece == "rook":
        move_flag = None
        move_msg = ""
        if king_y == piece_y:  # 좌우로 움직일 경우
            if from_x < to_x:
                move_msg, move_flag = rook_checking_horizontal(chess_board, player_color, piece_x, king_x, king_y, 1)
            elif from_x > to_x:
                move_msg, move_flag = rook_checking_horizontal(chess_board, player_color, piece_x, king_x, king_y, -1)
            check_flag = True
        elif king_x == piece_x:    # 위아래로 움직일 경우
            if from_y > to_y:
                move_msg, move_flag = rook_checking_vertical(chess_board, player_color, piece_y, king_x, king_y, -1)
            elif from_y < to_y:
                move_msg, move_flag = rook_checking_vertical(chess_board, player_color, piece_y, king_x, king_y, 1)
        if move_msg == "REMOVE" or move_flag:
            check_flag = True
            
    elif piece == "knight":
        if (abs(piece_x - king_x) == 2 and abs(piece_y - king_y) == 1) or (abs(piece_x - king_x) == 1 and abs(piece_y - king_y) == 2):  # 이동 가능 검증
            check_flag = True

    elif piece == "bishop":
        if abs(piece_x - king_x) == abs(piece_y - king_y):    # x와 y의 이동 칸 수 동일 시
            move_msg = bishop_check(chess_board, player_color, from_x, from_y, to_x, to_y)
            if move_msg == "MOVE":
                check_flag = True
    
    elif piece == "queen":
        move_msg = "" 
        move_flag = None
        if (king_y == piece_y) or (king_x == piece_x):
            if king_y == piece_y:  # 좌우로 움직일 경우
                if from_x < to_x:
                    move_msg, move_flag = rook_checking_horizontal(chess_board, player_color, piece_x, king_x, king_y, 1)
                elif from_x > to_x:
                    move_msg, move_flag = rook_checking_horizontal(chess_board, player_color, piece_x, king_x, king_y, -1)
                check_flag = True
            elif king_x == piece_x:    # 위아래로 움직일 경우
                if from_y > to_y:
                    move_msg, move_flag = rook_checking_vertical(chess_board, player_color, piece_y, king_x, king_y, -1)
                elif from_y < to_y:
                    move_msg, move_flag = rook_checking_vertical(chess_board, player_color, piece_y, king_x, king_y, 1)
            if move_msg == "REMOVE" or move_flag:
                check_flag = True
        elif abs(piece_x - king_x) == abs(piece_y - king_y):    # x와 y의 이동 칸 수 동일 시
            move_msg = bishop_check(chess_board, player_color, from_x, from_y, to_x, to_y)
            if move_msg == "MOVE":
                check_flag = True

    return check_flag


# 좌우 이동 처리 - 룩
def rook_checking_horizontal(chess_board, player_color, from_x, to_x, to_y, step):
    move_msg = None
    blocking_x = None
    blocking_piece_color = None
    move_flag = True
    for x in range(from_x + step, to_x + step, step): # step이 +일 경우, from_x 수는 제외하고 -일 경우 to_x의 값도 볼 수 있도록 조정
        if (x, to_y) in chess_board:
            blocking_x = x
            blocking_piece_color = chess_board[x, to_y][2]
            break
    # 그 전까지 이동
    if blocking_x is not None and to_x > blocking_x and step == 1: # 우측으로 움직일 경우
        move_flag = False
    elif blocking_x is not None and to_x < blocking_x and step == -1: # 좌측으로 움직일 경우
        move_flag = False

    # 사이에 다른 색의 기물인 경우 기물 잡기
    if blocking_x is not None and blocking_piece_color is not None:
        if (player_color != blocking_piece_color) and to_x == blocking_x:
            move_msg = "REMOVE"   
        elif (player_color == blocking_piece_color) and to_x == blocking_x:   # 같은 색인 경우
            move_flag = False
    return move_msg, move_flag

# 위아래 이동 처리 - 룩
def rook_checking_vertical(chess_board, player_color, from_y, to_x, to_y, step): 
    move_msg = None
    blocking_y = None
    blocking_piece_color = None
    move_flag = True
    for y in range(from_y + step, to_y + step, step): # step이 +일 경우, from_x 수는 제외하고 -일 경우 to_x의 값도 볼 수 있도록 조정
        if (to_x, y) in chess_board:
            blocking_y = y
            blocking_piece_color = chess_board[to_x, y][2]
            break
    # 그 전까지 이동
    if blocking_y is not None and (to_y > blocking_y and player_color == "black" and step == -1) or (to_y < blocking_y and player_color == "white" and step == -1): # (white가 위로 움직일 경우, black이 뒤로 움직인 경우)
        move_flag = False
    elif blocking_y is not None and (to_y > blocking_y and player_color == "black" and step == 1) or (to_y < blocking_y and player_color == "white" and step == 1): # (white가 뒤로 움직일 경우, black가 앞으로 움직일 경우)
        move_flag = False

    # 기물 잡기
    if blocking_y is not None and blocking_piece_color is not None:
        if player_color != blocking_piece_color and to_y == blocking_y:
            move_msg = "REMOVE"   
        elif player_color == blocking_piece_color and to_y == blocking_y:
            move_flag = False
    return move_msg, move_flag

# 비숍 방향
def bishop_find_direction(from_, to):
    if from_ < to:
        direction = +1
    elif from_ > to:
        direction = -1
    return direction

# 비숍 로직 확인
def bishop_check(chess_board, player_color, from_x, from_y, to_x, to_y):
    move_msg = None
    if abs(from_x - to_x) == abs(from_y - to_y):    # x와 y의 이동 칸 수 동일 시
        num = abs(from_x - to_x) # 이동 칸 수 확인
        # 만일 중간에 기물이 있는지 확인
        x_direction = bishop_find_direction(from_x, to_x)
        y_direction = bishop_find_direction(from_y, to_y)
        
        move_flag = True
        for num in range(1, abs(from_x - to_x)):
            x = from_x + (num * x_direction)
            y = from_y + (num * y_direction)
            if chess_board[(x, y)][1] is not None:   # 만일 chess_board에 기물이 있다면
                move_flag = False
                break
        # 만일 기물 발견하지 못했다면 가려는 좌표에 기물 있는지 확인
        if move_flag:
            if (chess_board[(to_x, to_y)][1] is not None) and (chess_board[(to_x, to_y)][2] == player_color):    # 만일 플레이어 색과 같다면
                move_flag = False   # 만일 가려는 좌표에 기물이 있다면
            elif  (chess_board[(to_x, to_y)][1] is not None) and (chess_board[(to_x, to_y)][2] != player_color): # 기물 잡기
                move_msg = "REMOVE"
        # 만일 기물 발견X, REMOVE X일 경우 이동
        if move_flag and move_msg != "REMOVE":
            move_msg = "MOVE"
    return move_msg

def check_move(chess_board, player_color, to_x, to_y):
    move_flag = True
    move_msg = ""
    # 만일 다른 색이 자리에 있을 경우
    if chess_board[(to_x, to_y)][1] is not None and chess_board[(to_x, to_y)][2] != player_color:
        move_msg = "REMOVE"
    # 같은 색이 자리에 있을 경우
    elif chess_board[(to_x, to_y)][1] is not None and chess_board[(to_x, to_y)][2] == player_color:
        move_flag = False
    return move_msg, move_flag

def castling_find_move(chess_board, to_y, x, num, step=1):
    castling_flag = True
    if (x, to_y) in rook_list:
        castling_flag = False
    else:
        for check_x in range(x, num, step):
            if chess_board[(check_x, to_y)][1] is not None:
                castling_flag = False
                break
    return castling_flag

def find_mate(chess_board, player_color):
    # 만일 한정된 곳일 경우
    king_check_list = king_move_find_check(chess_board, player_color)
    mate = True
    for value in king_check_list.values():
        if value[1] == False:
            value = value[2]
            mate = False
            break
    king_check_list.clear()
    return mate, value
    


import socket
import json


# 서버의 IP주소, poth 주소 설정
HOST = '127.0.0.1'
PORT = 12345

# socket : UDP 설정
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 바인딩 하기
server_socket.bind((HOST, PORT))

print("실행중")

# 설정값
client_list = []
game_status = None # 게임 상태 저장(게임 판 수)
player_color = None
check = False
enemy_pawn_list = {}
rook_list = {}
check_list = {}

        

while True:
    # 클라이언트로부터 메세지 수신
    date, client_socket = server_socket.recvfrom(32768)
    message = date.decode('utf-8')
    print(f"client로부터 송신 : {message}")
    
    try:
        # json 역직렬화(GPT 참고)
        data_message = json.loads(message)

    except json.JSONDecodeError: # GPT 참고
        # 중복 클라이언트 방지
        if client_socket not in client_list:
            client_list.append(client_socket)
            message_client = "참가 확인"
            server_socket.sendto(message_client.encode('utf-8'), client_socket)

        # 클라이언트 2명이 모인 경우
        if len(client_list) == 2 and game_status is None:
            print("게임 시작 함")
            for client in client_list:
                if client == client_list[0]:
                    msg = "black"
                elif client == client_list[1]:
                    msg = "white"
                server_socket.sendto(f"게임시작 {msg}".encode('utf-8'), client)
            game_status = 1

        # 순서
        if len(client_list) == 2 and game_status is not None:
            if game_status % 2 == 0: # 짝수일경우
                server_socket.sendto("TURN".encode("utf-8"), client_list[0])
                player_color = "black"
            else:
                server_socket.sendto("TURN".encode("utf-8"), client_list[1])
                player_color = "white"
        continue

    # 클라이언트로 MOVE 받을 경우 로직
    # MOVE 처리
    if data_message and data_message["type"] == "MOVE":
        selected_piece_list = data_message["selected_piece"]
        chess_board_string = data_message["chess_board"]
        to_x = data_message["to_x"]
        to_y = data_message["to_y"]

        pos, selected_piece, piece_color, status_flag = selected_piece_list   # selected_piece 리스트 각 변수 할당
        from_x, from_y = pos
        chess_board = {}

        # chessboard -> 튜플로 변환
        for key in chess_board_string.keys():
            x_s, y_s = key.split(",")
            x, y = map(int, [x_s, y_s])
            chess_board.update({(x, y) : [chess_board_string[key][0], chess_board_string[key][1], chess_board_string[key][2]]})
        
        # 좌표는 string이니 int로 변환
        to_x, to_y = map(int, [to_x, to_y]) # map(요소에 적용할 함수, 함수 적용시킬 데이터의 집합)

        # 블랙 / 화이트 일 경우
        num = None
        if player_color == "white":     # gpt 도움 받아 로직 작성
            num = 1
        else:
            num = -1

        # 체크 플래그
        check = False

        
        # 움직이려는 기물과 플레이어 색이 맞을 경우만
        if player_color == piece_color:
            # 해당 좌효에 맞게 기물 이동 로직 수행
            if check == False:
                # pawn인 경우
                if selected_piece == "pawn":
                    move_msg = pawn_move_remove(status_flag, chess_board, from_x, from_y, to_x, to_y, num, enemy_pawn_list, player_color)

                    if move_msg != "MOVE" and move_msg != "REMOVE":
                        # 앙파상 규칙
                        if (player_color == "white" and from_y == 4) or (player_color == "black" and from_y == 5):
                            # 왼쪽인 경우
                            if ((from_x - 1, from_y) in enemy_pawn_list) and player_color != enemy_pawn_list[(from_x - 1, from_y)][0]:
                                del enemy_pawn_list[(from_x - 1, from_y)]
                                move_msg = "en_passant"
                            # 오른쪽인 경우
                            elif (((from_x + 1, from_y) in enemy_pawn_list) and player_color != enemy_pawn_list[(from_x - 1, from_y)][0]):
                                del enemy_pawn_list[(from_x + 1, from_y)]
                                move_msg = "en_passant"   

                    # 프로모션 진행(폰 승진)
                    if (player_color == "white" and to_y == 1) or (player_color == "black" and to_y == 8):
                        if move_msg == "MOVE":
                            move_msg = "PROMOTION"

                        
                # rook인 경우
                elif selected_piece == "rook":
                    if to_y == from_y:  # 좌우로 움직일 경우
                        # 오른쪽으로 움직일 경우, 가로막은 기물 있다면 기물 선택
                        if from_x < to_x:
                            move_msg, move_flag = rook_checking_horizontal(chess_board, player_color, from_x, to_x, to_y, 1)
                        # 왼쪽으로 움직일 경우, 가로막은 기물 있다면 기물 선택
                        elif from_x > to_x:
                            move_msg, move_flag = rook_checking_horizontal(chess_board, player_color, from_x, to_x, to_y, -1)
                        
                    elif to_x == from_x:    # 위아래로 움직일 경우
                        # 가로막은 기물 있다면 기물 선택(white가 위로 움직일 경우, black이 뒤로 움직인 경우)
                        if from_y > to_y:
                            move_msg, move_flag = rook_checking_vertical(chess_board, player_color, from_y, to_x, to_y, -1)

                        # 가로막은 기물 있다면 기물 선택(white가 뒤로 움직일 경우, black가 앞으로 움직일 경우)
                        elif from_y < to_y:
                            move_msg, move_flag = rook_checking_vertical(chess_board, player_color, from_y, to_x, to_y, 1)

                    # 만일 전부 아니고 이동 가능 경우(첫 번째 이동)
                    if move_flag and move_msg is None and status_flag:
                        move_msg = "FIRST_MOVE"
                        rook_list.update({(from_x, from_y) : [piece_color]})
                    elif move_flag and move_msg is None and status_flag == False:
                        move_flag = "MOVE"

                # knight인 경우
                elif selected_piece == "knight":
                    if (abs(from_x - to_x) == 2 and abs(from_y - to_y) == 1) or (abs(from_x - to_x) == 1 and abs(from_y - to_y) == 2):  # 이동 가능 검증
                        move_msg, move_flag = check_move(chess_board, player_color, to_x, to_y)
                        # remove가 아니고, blocked도 아닌 경우 이동
                        if move_flag and move_msg != "REMOVE":
                            move_msg = "MOVE"

                # bishop인 경우
                elif selected_piece == "bishop":
                    move_msg = bishop_check(chess_board, player_color, from_x, from_y, to_x, to_y)

                # king인 경우
                elif selected_piece == "king":                           
                    # 킹 이동 로직 확인
                    if (abs(from_x - to_x) == 1 and (from_y == to_y or abs(from_y - to_y) == 1)) or (abs(from_y - to_y) == 1 and (from_x == to_x or abs(from_x - to_x) == 1)):
                        # 자살 금지를 위한 확인
                        king_check_list = king_move_find_check(chess_board, player_color)

                        # 만일 금지된 좌표 있을 경우 제외
                        if ((to_x, to_y) in king_check_list) and king_check_list[(to_x, to_y)][1] == True:
                            status_flag = False
                        king_check_list.clear()

                        move_msg = check_move(chess_board, player_color, to_x, to_y)
                        # remove가 아니고, blocked도 아닌 경우 이동(첫 번째 이동일 경우)
                        if move_flag and move_msg != "REMOVE" and status_flag:
                            move_msg = "FIRST_MOVE"
                        elif move_flag and move_msg != "REMOVE" and status_flag == False:
                            move_msg = "MOVE"
                    # 캐슬링 규칙 (킹과 룩이 첫 이동 + 이동시킬 킹과 룩 사이 기물 없을 경우)
                    if check == False and (from_y == to_y and abs(from_x - to_x) == 2):  # 킹/퀸 사이드로 2칸 이동한 경우
                        if to_x < 5: # 퀸 사이드인 경우
                            castling_flag = castling_find_move(chess_board, to_y, 1, 5)
                        elif to_x > 5: # 킹 사이드인 경우 
                            castling_flag = castling_find_move(chess_board, to_y, 8, 5, -1)
                        # 검증 전부 통과일 시 
                        if castling_flag:
                            move_msg = "CASTLING"

                # queen인 경우 (bishop + rook)
                elif selected_piece == "queen":
                    if abs(from_x - to_x) == abs(from_y - to_y):    # x와 y의 이동 칸 수 동일 시
                        bishop_check(chess_board, player_color, from_x, from_y, to_x, to_y)
                    # 좌우로 움직일 경우
                    elif to_y == from_y:  
                        # 오른쪽으로 움직일 경우, 가로막은 기물 있다면 기물 선택
                        if from_x < to_x:
                            move_msg, move_flag = rook_checking_horizontal(chess_board, player_color, from_x, to_x, to_y, 1)
                        # 왼쪽으로 움직일 경우, 가로막은 기물 있다면 기물 선택
                        elif from_x > to_x:
                            move_msg, move_flag = rook_checking_horizontal(chess_board, player_color, from_x, to_x, to_y, -1)
                    # 위아래로 움직일 경우
                    elif to_x == from_x:
                        # 가로막은 기물 있다면 기물 선택(white가 위로 움직일 경우, black이 뒤로 움직인 경우)
                        if from_y > to_y:
                            move_msg, move_flag = rook_checking_vertical(chess_board, player_color, from_y, to_x, to_y, -1)

                        # 가로막은 기물 있다면 기물 선택(white가 뒤로 움직일 경우, black가 앞으로 움직일 경우)
                        elif from_y < to_y:
                            move_msg, move_flag = rook_checking_vertical(chess_board, player_color, from_y, to_x, to_y, 1)
                    # 만일 전부 아니고 이동 가능 경우
                    if move_flag and move_msg is None:
                        move_msg = "MOVE"
                

            # 체크일 경우 한정된 이동
            elif check:
                # 킹이 공격 범위 벗어나기
                if selected_piece == "king":
                    # 킹 이동 로직 확인
                    if (abs(from_x - to_x) == 1 and (from_y == to_y or abs(from_y - to_y) == 1)) or (abs(from_y - to_y) == 1 and (from_x == to_x or abs(from_x - to_x) == 1)):
                        status_flag = True
                        # 만일 한정된 곳일 경우
                        king_check_list = king_move_find_check(chess_board, player_color)
                        if ((to_x, to_y) in king_check_list) and king_check_list[(to_x, to_y)][1] == True:
                            status_flag = False
                        king_check_list.clear()
                        move_msg, move_flag = check_move(chess_board, player_color, to_x, to_y)
                        # 만일 status_flag == True 그리고 remove가 아니라면 MOVE를.
                        if status_flag and move_msg != "REMOVE":
                            move_msg = "MOVE"
                            check = False
                            check_list.clear()
                            
                # 아군이 공격 경로 차단
                elif selected_piece != "king":
                    pos_list = chess_check_list_pos(chess_board, check_list, player_color)  # 체크한 상대 기물 좌표
                    flag_list = []
                    pos = []

                    for i in len(pos_list):
                        x, y = pos_list[i]

                        # 먼저 이동 가능한지 그 범위 확인.
                        flag = king_move_simulation(selected_piece, from_x, from_y, x, y, piece_color)
                        if flag:
                            if to_x == x and to_y == y:
                                move_msg = "MOVE"
        
                # 아군이 체크 중인 기물 잡기
                    if move_msg is None:
                        for key, value in check_list.items():
                            check_piece_x, check_piece_y = key
                        check_flag = king_move_simulation(selected_piece, from_x, from_y, check_piece_x, check_piece_y, player_color)
                        if check_flag:
                            move_msg = "REMOVE"
                            check = False
                            check_list.clear()
                        

        # 체크 확인 
        if move_msg == "MOVE" or move_msg == "REMOVE": 
            # to_x와 to_y로 킹이 있는지 검증 한 번 필요
            for key, value in chess_board.items():
                if value[1] == "king" and value[2] != player_color:
                    king_x, king_y = key
                    break
            check_flag = king_move_simulation(selected_piece, to_x, to_y, king_x, king_y, piece_color)
            # 만일 맞고으면
            if check_flag:
                check_list.update({(to_x, to_y) : [selected_piece, player_color]})
                check = True
                move_msg = "CHECK"

        # 체크메이트 -> 체크 O, 어느 수를 두어도 벗어날 수 없는 경우 <- 이 때 다른 아군 기물도 변수로 포함해야함. (수정 필)
        elif check:
            mate, value = find_mate(chess_board, player_color)
            if mate:
                move_msg = f"CHECKMATE WIN {value}"
                king_check_list.clear()
                break

        # 스테일메이트 -> 체크 X, 어느 수를 두어도 벗어날 수 없는 경우 <- 이 때 다른 아군 기물도 변수로 포함해야함. (수정 필)
        elif check == False:
            mate, value = find_mate(chess_board, player_color)
            if mate:
                move_msg = f"STALEMATE WIN {value}"
                king_check_list.clear()
                break
        
        
        server_socket.sendto(move_msg.encode('utf-8'), client)
        player_color = None     # 초기화
        print(move_msg)
    
server_socket.close()


