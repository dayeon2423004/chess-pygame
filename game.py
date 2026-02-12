import pygame
import queue
import json


# 파이게임 초기화
pygame.init()

# # 화면 크기 조정
# width, height = 900, 900
# screen = pygame.display.set_mode((width, height))
# pygame.display.set_caption("chess game")

# FPS 설정
clock = pygame.time.Clock()

# 색상/폰트/이미지 정의
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
beige = (255, 255, 230)
brown = (210, 139, 73)
cream = (254, 206, 158)
# font = pygame.font.SysFont('garamond', 30)
# font_1 = pygame.font.SysFont('garamond', 100)

wait_running = True

chess_piece = {}
selected_piece = None
mouse_x = None
mouse_y = None

# 플레이어 설정
player_color = None


# # 대기 보드 설정
# def wait_board():
#        # pygame.init()

#        # 화면 크기 조정
#        width, height = 900, 900
#        screen = pygame.display.set_mode((width, height))
#        pygame.display.set_caption("chess game")

#        # 폰트 설정
#        font_1 = pygame.font.SysFont('garamond', 100)

#        while wait_running:
#               clock.tick(30)
#               screen.fill(black)
#               font_render_wait = font_1.render("Just moment", True, white)
#               screen.blit(font_render_wait, (200, 380))
#               pygame.display.flip()

#               # 이벤트 리슨
#               for event in pygame.event.get():
#                      if event.type == pygame.QUIT:
#                             running = False
#        pygame.quit()


def chess(send_queue, recv_queue):
       global chess_piece, selected_piece, mouse_x, mouse_y
       # 화면 크기 조정
       width, height = 900, 900
       screen = pygame.display.set_mode((width, height))
       pygame.display.set_caption("chess game")

       # 폰트 설정
       font = pygame.font.SysFont('garamond', 30)

       # 반투명 정의 (가로, 세로)
       transparent_surface = pygame.Surface((900, 900), pygame.SRCALPHA)  # 알파 채널을 지원하는 서피스
       transparent_surface.fill((0, 0, 0, 180))

       # 체스 기물 이미지 정의
       black_king = pygame.image.load('piece_image/black_king_resize.png')
       black_queen = pygame.image.load('piece_image/black_queen_resize.png')
       black_bishop_l = pygame.image.load('piece_image/black_bishop_resize.png')
       black_bishop_r = pygame.image.load('piece_image/black_bishop_resize.png')
       black_knight_l = pygame.image.load('piece_image/black_knight_resize.png')
       black_knight_r = pygame.image.load('piece_image/black_knight_resize.png')
       black_rook_l = pygame.image.load('piece_image/black_rook_resize.png')
       black_rook_r = pygame.image.load('piece_image/black_rook_resize.png')
       white_king = pygame.image.load('piece_image/white_king_resize.png')
       white_queen = pygame.image.load('piece_image/white_queen_resize.png')
       white_bishop_l = pygame.image.load('piece_image/white_bishop_resize.png')
       white_bishop_r = pygame.image.load('piece_image/white_bishop_resize.png')
       white_knight_l = pygame.image.load('piece_image/white_knight_resize.png')
       white_knight_r = pygame.image.load('piece_image/white_knight_resize.png')
       white_rook_l = pygame.image.load('piece_image/white_rook_resize.png')
       white_rook_r = pygame.image.load('piece_image/white_rook_resize.png')

       # 폰 정의
       black_pawn1 = pygame.image.load('piece_image/black_pawn_resize.png')
       black_pawn2 = pygame.image.load('piece_image/black_pawn_resize.png')
       black_pawn3 = pygame.image.load('piece_image/black_pawn_resize.png')
       black_pawn4 = pygame.image.load('piece_image/black_pawn_resize.png')
       black_pawn5 = pygame.image.load('piece_image/black_pawn_resize.png')
       black_pawn6 = pygame.image.load('piece_image/black_pawn_resize.png')
       black_pawn7 = pygame.image.load('piece_image/black_pawn_resize.png')
       black_pawn8 = pygame.image.load('piece_image/black_pawn_resize.png')
       white_pawn1 = pygame.image.load('piece_image/white_pawn_resize.png')
       white_pawn2 = pygame.image.load('piece_image/white_pawn_resize.png')
       white_pawn3 = pygame.image.load('piece_image/white_pawn_resize.png')
       white_pawn4 = pygame.image.load('piece_image/white_pawn_resize.png')
       white_pawn5 = pygame.image.load('piece_image/white_pawn_resize.png')
       white_pawn6 = pygame.image.load('piece_image/white_pawn_resize.png')
       white_pawn7 = pygame.image.load('piece_image/white_pawn_resize.png')
       white_pawn8 = pygame.image.load('piece_image/white_pawn_resize.png')
       

       # 체스 칸 크기
       rect_width = 100
       rect_height = 100

       # 선택 기물
       selected_piece = None
       click_piece = None

       # 체스 기물 이미지 배치
       chess_piece = {black_rook_l : [(1, 1), "rook", "black", True],
                     black_knight_l : [(1, 2), "knight", "black", None],
                     black_bishop_l : [(1, 3), "bishop", "black", None],
                     black_queen : [(1, 4), "queen", "black", None],
                     black_king : [(1, 5), "king", "black", True],
                     black_bishop_r : [(1, 6),"bishop", "black", None],
                     black_knight_r : [(1, 7),"knight", "black", None],
                     black_rook_r : [(1, 8),"rook", "black", True],
                     white_rook_l : [(8, 1),"rook", "white", True],
                     white_knight_l : [(8, 2),"knight", "white", None],
                     white_bishop_l : [(8, 3),"bishop", "white", None],
                     white_queen : [(8, 4),"queen", "white", None],
                     white_king : [(8, 5),"king", "white", True],
                     white_bishop_r : [(8, 6),"bishop", "white", None],
                     white_knight_r : [(8, 7),"knight", "white", None],
                     white_rook_r : [(8, 8),"rook", "white", True]}
       
       chess_piece.update({black_pawn1 : [(2, 1),"pawn", "black", True],
                           black_pawn2 : [(2, 2),"pawn", "black", True],
                           black_pawn3 : [(2, 3),"pawn", "black", True],
                           black_pawn4 : [(2, 4),"pawn", "black", True],
                           black_pawn5 : [(2, 5),"pawn", "black", True],
                           black_pawn6 : [(2, 6),"pawn", "black", True],
                           black_pawn7 : [(2, 7),"pawn", "black", True],
                           black_pawn8 : [(2, 8),"pawn", "black", True],
                           white_pawn1 : [(7, 1),"pawn", "white", True],
                           white_pawn2 : [(7, 2),"pawn", "white", True],
                           white_pawn3 : [(7, 3),"pawn", "white", True],
                           white_pawn4 : [(7, 4),"pawn", "white", True],
                           white_pawn5 : [(7, 5),"pawn", "white", True],
                           white_pawn6 : [(7, 6),"pawn", "white", True],
                           white_pawn7 : [(7, 7),"pawn", "white", True],
                           white_pawn8 : [(7, 8),"pawn", "white", True]})
       

       # 테두리 간격
       chess_piece_x = 50

       chess_board = {}     
       green_board = []
       Turn_flag = False

       # 게임 보드 업로드
       for row in range(1, 9):
              for col in range(1, 9):
                     chess_board.update({(row, col) : [ ((rect_width * row) - 50, (rect_height * col) - 50), None, None ]})

       # 게임 보드에 기물 있는 좌표 추가
       for key in chess_board.keys():
              for chess_value in chess_piece.values():
                     if key == chess_value[0]:
                            chess_board[key][1] = chess_value[1]
                            chess_board[key][2] = chess_value[2]
                            break
       
       # 게임 루프
       running = True
       while running:
              clock.tick(30)
              screen.fill(white)
              

              # 테두리 그리기
              pygame.draw.rect(screen, brown, (rect_width - chess_piece_x, rect_height - chess_piece_x, 800, 800), 3)  # 두께 3의 테두리

              # 테두리 영어 글자
              eng_f = 0
              for eng in range(65, 73):
                     font_render = font.render(chr(eng), True, black)
                     flipped_letter = pygame.transform.flip(font_render, True, True)  # 수평, 수직으로 뒤집기
                     screen.blit(font_render, (rect_width - 15 + eng_f, 858))
                     screen.blit(flipped_letter, (rect_width - 15 + eng_f, 8))
                     eng_f += 100

              # 테두리 숫자 글자
              num_f = 0
              for num in range(8, 0, -1):
                     font_render2 = font.render(str(num), True, black) # True는 부드럽게 텍스트를 렌더링 하는 역할.
                     flipped_letter2 = pygame.transform.flip(font_render2, True, True)  # 수평, 수직으로 뒤집기
                     screen.blit(font_render2, (18, rect_width - 15 + num_f))
                     screen.blit(flipped_letter2, (865, rect_width - 15 + num_f))
                     num_f += 100
       
              # 게임판 그리기
              for row in range(1, 9):
                     for col in range(1, 9):
                            if (row + col) % 2 == 0:
                                   pygame.draw.rect(screen, cream, ((rect_width * row) - 50, (rect_height * col) - 50, rect_width, rect_height))
                            else:
                                   pygame.draw.rect(screen, brown, ((rect_width * row) - 50, (rect_height * col) - 50, rect_width, rect_height))
       
              # 마우스 클릭 후 드래그 동안 그리기
              if green_board:
                     pygame.draw.rect(screen, green, (green_board[0], green_board[1], rect_width, rect_height))
                     
              # 체스 기물 그리기
              for key, value in chess_piece.items():
                     x, y = value[0]
                     if selected_piece is not None:
                            if selected_piece == key:
                                   continue
                     screen.blit(key, chess_find_pos(x, y)) # 이미지, 좌표

              # for key, value in chess_piece.items():
              #        x, y = value
              #        if selected_piece is not None:
              #               if selected_piece == key:
              #                      continue
              #        screen.blit(key, chess_find_pos(x, y)) # 이미지, 좌표
                            

              
              # 이벤트 리슨
              for event in pygame.event.get():
                     if event.type == pygame.QUIT:
                            running = False
                     
                     # 마우스 좌표
                     mouse_x, mouse_y = pygame.mouse.get_pos()
                     # Turn_flag = True
                     if not recv_queue.empty():
                            msg_recv = recv_queue.get()

                            # 마우스 이동 -> 서버로 TRUN 메세지를 받은 후
                            if msg_recv == "TURN":
                                   Turn_flag = True

                     if Turn_flag:
                            # 마우스 클릭 시 기물 선택
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                   # 클릭한 기물 선택하기
                                   for key, value in chess_piece.items():
                                          x, y = value[0]
                                          piece_x, piece_y = chess_find_pos(x, y)
                            
                                          if piece_x <= mouse_x <= piece_x + 100 and piece_y <= mouse_y <= piece_y + 100:
                                                 selected_piece = key
                                                 click_piece = piece_x, piece_y
                                                 break
                                          
                            # 체스칸 표시하기
                            if click_piece is not None:
                                   for key in chess_board.keys():
                                          pos_x, pos_y = chess_board[key][0]
                                          piece_x, piece_y = click_piece
                                          if (pos_x < piece_x < pos_x + 100) and (pos_y < piece_y < pos_y + 100):
                                                 green_board = [pos_x, pos_y]

                            # 기물과 함께 마우스 이동
                            if event.type == pygame.MOUSEMOTION and selected_piece is not None:
                                   screen.blit(selected_piece, (mouse_x - 50, mouse_y - 50))
                                          
                                   # 기물 위로 선택하기 < < 가장 최근에 추가한 것이 가장 위로 올라감.
                                   wait_pos, wait_piece, wait_color, wait_first = chess_piece.pop(selected_piece) # 키를 이용해 해당 값을 반환하고 삭제한다. 
                                   chess_piece.update({selected_piece : [wait_pos, wait_piece, wait_color, wait_first]})

                            # 마우스 버튼을 떼면 선택 해제
                            if event.type == pygame.MOUSEBUTTONUP and selected_piece is not None:
                                   # 검증을 위해 서버로 클라이언트 -> 서버 보내기
                                   from_x, from_y = chess_piece[selected_piece][0] # 이동 전 좌표(1, 4 이런식)
                                   to_x, to_y = mouse_pos(mouse_x, mouse_y) # 이동할 좌표(1, 4 이런 식)
                                   # message = f"MOVE {chess_piece[selected_piece]} {chess_board} {to_x} {to_y}" # queue 넣기

                                   chess_board_string = {}
                                   # 체스 보드 튜플 -> 문자열로 바꾸기
                                   for key in chess_board.keys():
                                          x, y = key
                                          chess_board_string.update({f"{x}, {y}" : [chess_board[key][0], chess_board[key][1], chess_board[key][2]]})
                                   message = {
                                          "type" : "MOVE",
                                          "selected_piece" : chess_piece[selected_piece],
                                          "chess_board" : chess_board_string,
                                          "to_x" : to_x,
                                          "to_y" : to_y
                                   }

                                   # json 직렬화 (GPT 참고)
                                   message = json.dumps(message)

                                   send_queue.put(message)

                                   # 서버 -> 클라이언트로 온 queue의 메세지가 MOVE일 경우
                                   if msg_recv == "MOVE" and msg_recv == "FIRST_MOVE":
                                          Turn_flag = False
                                          # 보드 속 기물 추가
                                          for key in chess_board.keys():
                                                 board_x, board_y = key
                                                 if board_x == to_x and board_y == to_y:
                                                        chess_board[key][1] = chess_piece[selected_piece][1]
                                                        chess_board[key][2] = chess_piece[selected_piece][2]
                                                 elif board_x == from_x and board_y == from_y:
                                                        chess_board[key][1] = None
                                                        chess_board[key][2] = None
                                          chess_piece[selected_piece][0] = (to_x, to_y)

                                   else:
                                          continue
                                   
                                   # # 중앙 배치 (abs는 절대값.)
                                   # for board_pos in chess_board.values():
                                   #        pos_x, pos_y = board_pos
                                   #        if abs(pos_x < mouse_x) and abs(pos_x + 100 > mouse_x) and abs(pos_y < mouse_y) and abs(pos_y + 100  > mouse_y):
                                   #               chess_piece[selected_piece][1] = pos_x, pos_y
                                   
                                   k = None
                                   delte_piece = []
                                   # 부딪힐 시 기물 삭제
                                   for key, value in chess_piece.items():
                                          chess_x, chess_y = chess_piece[selected_piece][0] # 선택 기물의 좌표 넘김 
                                          value_x, value_y = value # for로 돌아가며 모든 기물의 좌표 넘김.
                                          if chess_x == value_x and chess_y == value_y: # 만일 선택 기물과 돌아가며 얻은 기물의 좌표가 같다면 선택
                                                 if selected_piece != key: # 자신일 경우 제외해야함.
                                                        delte_piece.append(key)
                                                        k = key
                                   if k:
                                          del chess_piece[k]
                                   

                                   selected_piece = None  # 선택 해제
                                   click_piece = None
                                   green_board.clear()

              pygame.display.flip()

       # 게임 종료
       pygame.quit()

        



# 좌표 계산기 chess_piece(white_rook -> 1, 1) 이런식이라고 칠 때
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
                            return (x_original, y_original) # break 하는 방법 google 검색해서 찾아봄                           

def mouse_pos(mouse_x, mouse_y):
       y_pos = 50
       for i in range(1, 9):
              if i != 1:
                     y_pos += 100
              for y in range(1, 9): 
                     if y == 1:
                            x_pos = 50
                     else:
                            x_pos += 100
                     if x_pos <= mouse_x < x_pos + 100 and y_pos <= mouse_y < y_pos + 100:
                            return (i, y) 




if __name__ == "__main__":
       # wait_board()
       chess()
       



