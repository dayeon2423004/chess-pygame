# server/game_init.py

import protocol

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

        protocol.send(server_socket, client_addr, {
            "type": "JOIN_OK"
        })
        
    # 2명 모이면 게임 시작
    if len(client_list) == 2 and game_status is None:
        print("게임 시작")

        protocol.send(server_socket, client_list[0], {
            "type": "START",
            "color": "black"
        })

        protocol.send(server_socket, client_list[1], {
            "type": "START",
            "color": "white"
        })

        game_status = 1

        # white 먼저 턴
        protocol.send(server_socket, client_list[1], {
            "type": "TURN"
        })
        
# 턴 관리
def handle_turn(server_socket):
    global game_status

    if len(client_list) != 2:
        return

    game_status += 1

    # 짝수면 black
    if game_status % 2 == 0:
        protocol.send(server_socket, client_list[0], {
            "type": "TURN"
        })
    else:
        protocol.send(server_socket, client_list[1], {
            "type": "TURN"
        })
