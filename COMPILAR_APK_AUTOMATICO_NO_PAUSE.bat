@echo off
title GENERAL - Compilador Automatico de APK Nativo (Android)
cd /d "%~dp0"
echo Sincronizando arquivos e gerando APK nativo Android...
powershell -ExecutionPolicy Bypass -File "%~dp0sync_android.ps1"

set "JAVA_HOME=C:\Program Files\Android\Android Studio\jbr"
cd /d "%~dp0android"
call gradlew.bat assembleDebug

echo.
echo ============================================================
echo  APK GERADO COM SUCESSO!
echo  Caminho do arquivo APK:
echo  "%~dp0android\app\build\outputs\apk\debug\app-debug.apk"
echo ============================================================
echo.

exit
