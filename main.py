import subprocess
import time
import sys

def run_chess_project():
    print("--- 체스 프로젝트를 시작합니다 ---")

    # 1. 서버 실행 (백그라운드)
    # python -m server.server_main 실행과 동일
    server_process = subprocess.Popen([sys.executable, "-m", "server.server_main"])
    print("서버 가동 중...")
    
    time.sleep(2)

    # 2. 클라이언트 1 실행 
    print("클라이언트 1 실행...")
    p1 = subprocess.Popen([sys.executable, "-m", "client.client_main"])

    # 3. 클라이언트 2 실행 
    print("클라이언트 2 실행...")
    p2 = subprocess.Popen([sys.executable, "-m", "client.client_main"])

    # 4. 프로세스들이 종료될 때까지 대기
    p1.wait()
    p2.wait()
    
    # 클라이언트 종료시, 서버도 종료 
    server_process.terminate()
    print("모든 프로세스가 종료되었습니다.")

if __name__ == "__main__":
    run_chess_project()