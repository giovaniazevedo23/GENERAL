$WScriptShell = New-Object -ComObject WScript.Shell
$DesktopPath = [System.IO.Path]::Combine([System.Environment]::GetFolderPath("Desktop"), "GENERAL.lnk")
$AppDir = "C:\Users\giova\.gemini\antigravity\scratch\general-app"
$TargetPath = [System.IO.Path]::Combine($AppDir, "ABRIR_APP_GENERAL.bat")

$Shortcut = $WScriptShell.CreateShortcut($DesktopPath)
$Shortcut.TargetPath = $TargetPath
$Shortcut.WorkingDirectory = $AppDir
$Shortcut.WindowStyle = 1
$Shortcut.Description = "GENERAL - Aplicativo Nativo de Gestao Logistica e IA"
$Shortcut.Save()

Write-Host "Atalho do aplicativo nativo criado com sucesso na Area de Trabalho: $DesktopPath"
