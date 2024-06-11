@echo off
cd /d %~dp0 
python producer.py
python consumer.py
pause
