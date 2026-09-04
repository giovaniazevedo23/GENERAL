Copy-Item index.html index_gestor_temp.html -Force
Copy-Item motorista.html index.html -Force

Write-Host "Syncing files..."
.\sync_android.ps1

Write-Host "Building APK..."
$env:JAVA_HOME = "C:\Program Files\Android\Android Studio\jbr"
Set-Location android
.\gradlew.bat assembleDebug
Set-Location ..

Write-Host "Copying APK to landing page..."
Copy-Item android\app\build\outputs\apk\debug\app-debug.apk landing-page\GENERAL_Motorista_v5_1_Militar.apk -Force

Write-Host "Restoring index.html (Manager app)..."
Copy-Item index_gestor_temp.html index.html -Force
Remove-Item index_gestor_temp.html

Write-Host "Syncing back original state..."
.\sync_android.ps1

Write-Host "Done!"
