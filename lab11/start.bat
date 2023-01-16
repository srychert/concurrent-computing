@echo off 

if exist .\.venv\Scripts\python.exe (
    .\.venv\Scripts\python.exe .\board.py
) else (
    python .\board.py
)