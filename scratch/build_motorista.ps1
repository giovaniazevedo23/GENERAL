$AppDir = "C:\Users\giova\.gemini\antigravity\scratch\general-app"
$WwwDir = Join-Path $AppDir "www"

Write-Host "Preparando arquivos para build do Motorista..."
# Sync normal stuff first
Copy-Item -Path (Join-Path $AppDir "motorista.html") -Destination (Join-Path $WwwDir "index.html") -Force
Copy-Item -Path (Join-Path $AppDir "manifest.json") -Destination $WwwDir -Force
Copy-Item -Path (Join-Path $AppDir "sw.js") -Destination $WwwDir -Force
Copy-Item -Path (Join-Path $AppDir "css") -Destination $WwwDir -Recurse -Force
Copy-Item -Path (Join-Path $AppDir "js") -Destination $WwwDir -Recurse -Force
Copy-Item -Path (Join-Path $AppDir "icons") -Destination $WwwDir -Recurse -Force

# Change appName in capacitor config temporarily
$configPath = Join-Path $AppDir "capacitor.config.json"
$config = Get-Content $configPath | ConvertFrom-Json
$origName = $config.appName
$config.appName = "GENERAL Motorista"
$config.appId = "com.general.motorista"
$config | ConvertTo-Json -Depth 10 | Set-Content $configPath

Write-Host "Executando npx cap sync android..."
cmd /c npx cap sync android

Write-Host "Compilando APK..."
$env:JAVA_HOME="C:\Program Files\Android\Android Studio\jbr"
Set-Location (Join-Path $AppDir "android")
cmd /c gradlew.bat assembleDebug

$apkOut = Join-Path $AppDir "android\app\build\outputs\apk\debug\app-debug.apk"
if (Test-Path $apkOut) {
    Copy-Item $apkOut -Destination (Join-Path $AppDir "landing-page\GENERAL_Motorista.apk") -Force
    Write-Host "APK do Motorista gerado na landing-page!"
} else {
    Write-Host "Erro: APK nao foi gerado."
}

Write-Host "Restaurando configurações do Gestor..."
Set-Location $AppDir
$config.appName = $origName
$config.appId = "com.general.logistica"
$config | ConvertTo-Json -Depth 10 | Set-Content $configPath
Copy-Item -Path (Join-Path $AppDir "index.html") -Destination (Join-Path $WwwDir "index.html") -Force
cmd /c npx cap sync android

Write-Host "Processo concluído."
