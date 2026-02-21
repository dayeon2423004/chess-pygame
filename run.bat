@echo off
:: Ctrl + ` 
:: .\run.bat
:: 서버 새 창 실행 
start "CHESS SERVER" cmd /k "python -m server.server_main"
timeout /t 2

:: 클라이언트 새 창에서 실행
start "PLAYER 1" cmd /k "python -m client.client_main"
start "PLAYER 2" cmd /k "python -m client.client_main"