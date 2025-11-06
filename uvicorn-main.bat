@echo off
REM ✅ Activate Anaconda base environment
CALL "%USERPROFILE%\miniconda3\Scripts\activate.bat"

REM ✅ Activate conda environment
call conda activate hobby

uvicorn backend_fastapi.main:app --reload