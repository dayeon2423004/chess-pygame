#client_main.py
import socket
from queue import Queue
import game.game as game
import threading


client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 서버의 주소
server_addr = (("127.0.0.1", 12345))

# 서버에게 메세지 수신
print("게임 참가를 위해서 아무런 메세지 입력.")
send_masge = input("서버에 보낼 메세지:")
client_socket.sendto(send_masge.encode('utf-8'), server_addr)


# 큐 생성(수신 큐)
recv_queue = Queue() # 서버로 받을 큐
send_queue = Queue() # 서버로 보낼 큐


# 별도 스레드1 -> 서버로부터 메세지 수신
def server_rect(recv_queue):
    global client_socket
    while True:
        date, server_recv =  client_socket.recvfrom(32768)
        sercver_masge = date.decode("utf-8")
        recv_queue.put(sercver_masge)     # 큐로 넣기
        print(sercver_masge)

# 별도 스레드2 -> pygame으로부터 큐를 받아 서버로 메세지 송신
def send_message(send_queue):
    while True:
        message = send_queue.get()   # 큐 받기
        client_socket.sendto(message.encode('utf-8'), server_addr)
        print(message)


# 스레드 실행
threading.Thread(target=server_rect, args=(recv_queue,), daemon=True).start() # 괄호로 감싸지 않으면 객체가 되어버려 , 있는 튜플로 보내주어야 함.
threading.Thread(target=send_message, args=(send_queue,), daemon=True).start()

# 메인 스레드
while True:
    # 2명 모일 경우 => 색상 결정 + 게임 시작
    if not recv_queue.empty(): # 비어있지 않은지 확인하기 위해 .empty() 사용
        message = recv_queue.get()

        # 게임 시작 

        if message.startswith("게임시작"):  # message 변수의 첫 문자열이 "게임시작"으로 시작 시 True를, 그렇지 않을 시 False 반환
            my_color = message.split(" ")[1]    # split는 str.split(sep=None, maxsplit=-1) 로 sep를 구분자로, 단어의 리스트를 돌려줌
            print(f"my color: {my_color}")
            print("클라이언트 2명 참가 확인 완료. 게임이 시작됩니다.")
            game.player_color = my_color

            # 다른 파일 간 큐 공유를 위해 인자로 넘겨주기
            game.chess(send_queue, recv_queue)

client_socket.close()
