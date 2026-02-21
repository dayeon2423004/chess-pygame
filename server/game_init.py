# server/game_init.py

from server import protocol

# 상태 값
client_list = []
game_status = None
player_color = None

# 게임 시작 관리
def handle_join(server_socket, client_addr):
    global game_status

    # 중복 방지
    if client_addr not in client_list:
        client_list.append(client_addr)

        protocol.send(server_socket, client_addr,
                      protocol.make_join_ok())
        
    # 2명 모이면 시작
    if len(client_list) == 2 and game_status is None:
        print("게임 시작")

        # black
        protocol.send(server_socket, client_list[0],
                      protocol.make_start("black", "white"))

        # white
        protocol.send(server_socket, client_list[1],
                      protocol.make_start("white", "white"))

        game_status = "PLAYING"