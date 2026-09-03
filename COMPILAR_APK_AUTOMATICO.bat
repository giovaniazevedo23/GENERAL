@echo off
title GENERAL - Compilador Automatico de APK Nativo (Android)
cd /d "%~dp0"
echo Sincronizando arquivos e gerando APK nativo Android...
powershell -ExecutionPolicy Bypass -File "%~dp0scratch\build_motorista.ps1"

echo.
echo ============================================================
echo  APK DO MOTORISTA GERADO COM SUCESSO NA PASTA LANDING-PAGE!
echo ============================================================
echo.
pause
exit
