@echo off
REM Verificar si el entorno virtual existe
IF NOT EXIST .venv (
    echo Creando entorno virtual...
    python -m venv .venv
)

REM Activar el entorno virtual
echo Activando entorno virtual...
call .\.venv\Scripts\activate

REM Instalar dependencias desde requirements.txt
echo Instalando dependencias...
pip install -r requirements.txt

echo Configuración completa. El entorno virtual ha sido configurado.
pause
