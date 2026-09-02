@echo off
title Baixador-X
color 0A

echo.
echo  ========================================
echo       BAIXADOR-X - Twitter Downloader
echo  ========================================
echo.

echo Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado!
    echo Instale o Python em: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Verificando dependencias...
pip install yt-dlp >nul 2>&1

echo Iniciando aplicativo...
python baixar_twitter.py

if errorlevel 1 (
    echo.
    echo [ERRO] Ocorreu um problema ao iniciar o programa.
    pause
)
