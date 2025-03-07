@echo off
REM 
IF NOT EXIST .venv (
    echo Creating virtual environment...
    python -m venv .venv
)

REM 
echo Activating virtual environment...
call .\.venv\Scripts\activate

REM Install dependencies from requirements.txt
echo Installing dependencies...
pip install -r requirements.txt

echo Setup complete. The virtual environment has been configured.
pause
