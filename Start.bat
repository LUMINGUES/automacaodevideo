@echo off
title Corretor e Gerador de Videos
echo ======================================================
echo   Verificando ambiente...
echo ======================================================

:: 1. Tenta achar o Python no Windows
set "PYTHON_CMD=python"
python --version >nul 2>&1
if %errorlevel% neq 0 (
    set "PYTHON_CMD=py"
)

:: 2. Cria a pasta 'dependencias' (Ambiente Virtual)
if not exist "dependencias" (
    echo [1/3] Criando ambiente virtual seguro...
    %PYTHON_CMD% -m venv dependencias
)

:: 3. Instala a biblioteca correta automaticamente
echo [2/3] Instalando moviepy (isso pode demorar um pouco na primeira vez)...
.\dependencias\Scripts\python -m pip install "moviepy<2.0"

:: 4. Roda o script
echo.
echo [3/3] Iniciando o gerador...
echo ======================================================
.\dependencias\Scripts\python criar_videos.py

echo.
echo Finalizado.
pause