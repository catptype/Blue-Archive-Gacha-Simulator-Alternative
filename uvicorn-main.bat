@echo off
REM ✅ Activate Anaconda base environment
CALL "%USERPROFILE%\miniconda3\Scripts\activate.bat"

REM ✅ Activate conda environment
call conda activate hobby

REM ✅ Set the environment variable for DEBUG level logging (using .bat syntax)
set LOG_LEVEL=DEBUG

REM ✅ Run Uvicorn
uvicorn backend_fastapi.main:app --reload

pause