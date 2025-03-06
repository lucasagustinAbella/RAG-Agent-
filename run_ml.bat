@echo off
REM Activar el entorno virtual
call .\.venv\Scripts\activate

REM Ejecutar el script Python
echo Ejecutando main_runner.py...
python main_runner.py

pause
