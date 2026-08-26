$AppDir = "C:\Users\giova\.gemini\antigravity\scratch\general-app"
$WwwDir = Join-Path $AppDir "www"

if (-not (Test-Path $WwwDir)) {
    New-Item -ItemType Directory -Path $WwwDir -Force
}

Copy-Item -Path (Join-Path $AppDir "index.html") -Destination $WwwDir -Force
Copy-Item -Path (Join-Path $AppDir "manifest.json") -Destination $WwwDir -Force
Copy-Item -Path (Join-Path $AppDir "sw.js") -Destination $WwwDir -Force
Copy-Item -Path (Join-Path $AppDir "css") -Destination $WwwDir -Recurse -Force
Copy-Item -Path (Join-Path $AppDir "js") -Destination $WwwDir -Recurse -Force
Copy-Item -Path (Join-Path $AppDir "icons") -Destination $WwwDir -Recurse -Force

Write-Host "✅ Arquivos compilados na pasta www/"
cmd /c npx cap sync android
Write-Host "🚀 Projeto Android Studio sincronizado com sucesso!"
