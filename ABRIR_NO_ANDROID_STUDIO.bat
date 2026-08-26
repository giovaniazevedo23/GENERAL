@echo off
title GENERAL - Abrir Projeto Nativo no Android Studio
cd /d "%~dp0"
echo Sincronizando arquivos e abrindo no Android Studio...
powershell -ExecutionPolicy Bypass -File "%~dp0sync_android.ps1"
cmd /c npx cap open android
exit
