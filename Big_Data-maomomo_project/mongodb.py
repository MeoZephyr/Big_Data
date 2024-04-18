@echo off
cd / d %~dp0
set loop_count = 3
set/a current_loop = 0

:loop
python producer.py
python consumer.py
set / a current_loop+=1
echo comleted iteration: %current_loop%

timeout /t 30 /nobreak >nul
if %current_loop% lss %loop_count% goto loop 

python MongoDB.py
echo dataBase succesfully run B10502129