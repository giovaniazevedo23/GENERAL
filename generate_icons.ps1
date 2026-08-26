Add-Type -AssemblyName System.Drawing

$iconsDir = "C:\Users\giova\.gemini\antigravity\scratch\general-app\icons"
if (-not (Test-Path $iconsDir)) { New-Item -ItemType Directory -Path $iconsDir -Force }

$sizes = @(192, 512, 180)

foreach ($size in $sizes) {
    $bmp = New-Object System.Drawing.Bitmap($size, $size)
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    $g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
    $g.Clear([System.Drawing.Color]::Transparent)

    # 1. Background Rounded Square Gradient (#0a1422 -> #060b14)
    $rect = New-Object System.Drawing.Rectangle(0, 0, $size, $size)
    $bgBrush = New-Object System.Drawing.Drawing2D.LinearGradientBrush(
        $rect,
        [System.Drawing.Color]::FromArgb(255, 10, 20, 34),
        [System.Drawing.Color]::FromArgb(255, 6, 12, 20),
        [System.Drawing.Drawing2D.LinearGradientMode]::Vertical
    )
    $bgPath = New-Object System.Drawing.Drawing2D.GraphicsPath
    $r = [float]($size * 0.20)
    $bgPath.AddArc(0, 0, $r*2, $r*2, 180, 90)
    $bgPath.AddArc([float]($size - $r*2), 0, $r*2, $r*2, 270, 90)
    $bgPath.AddArc([float]($size - $r*2), [float]($size - $r*2), $r*2, $r*2, 0, 90)
    $bgPath.AddArc(0, [float]($size - $r*2), $r*2, $r*2, 90, 90)
    $bgPath.CloseFigure()
    $g.FillPath($bgBrush, $bgPath)

    # Outer border for icon tile
    $tilePen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(255, 40, 65, 95), [float]($size * 0.015))
    $g.DrawPath($tilePen, $bgPath)

    # 2. Outer Shield Outline
    $cx = [float]($size / 2)
    $cy = [float]($size * 0.46)
    $sw = [float]($size * 0.65)
    $sh = [float]($size * 0.70)

    $shieldPath = New-Object System.Drawing.Drawing2D.GraphicsPath
    $shieldPath.AddBezier(
        [float]($cx - $sw/2), [float]($cy - $sh/2 + $sh*0.1),
        [float]($cx - $sw/4), [float]($cy - $sh/2),
        [float]($cx + $sw/4), [float]($cy - $sh/2),
        [float]($cx + $sw/2), [float]($cy - $sh/2 + $sh*0.1)
    )
    $shieldPath.AddBezier(
        [float]($cx + $sw/2), [float]($cy - $sh/2 + $sh*0.1),
        [float]($cx + $sw*0.52), [float]($cy + $sh*0.2),
        [float]($cx + $sw*0.35), [float]($cy + $sh*0.42),
        [float]($cx), [float]($cy + $sh/2)
    )
    $shieldPath.AddBezier(
        [float]($cx), [float]($cy + $sh/2),
        [float]($cx - $sw*0.35), [float]($cy + $sh*0.42),
        [float]($cx - $sw*0.52), [float]($cy + $sh*0.2),
        [float]($cx - $sw/2), [float]($cy - $sh/2 + $sh*0.1)
    )
    $shieldPath.CloseFigure()

    $shieldFill = New-Object System.Drawing.Drawing2D.LinearGradientBrush(
        $rect,
        [System.Drawing.Color]::FromArgb(255, 16, 32, 53),
        [System.Drawing.Color]::FromArgb(255, 7, 15, 27),
        [System.Drawing.Drawing2D.LinearGradientMode]::Vertical
    )
    $g.FillPath($shieldFill, $shieldPath)

    $shieldPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(255, 141, 169, 196), [float]($size * 0.045))
    $g.DrawPath($shieldPen, $shieldPath)

    # 3. Military Cap (Quepe)
    # Crown
    $capPath = New-Object System.Drawing.Drawing2D.GraphicsPath
    $capPath.AddBezier(
        [float]($cx - $size*0.18), [float]($cy - $size*0.06),
        [float]($cx - $size*0.12), [float]($cy - $size*0.24),
        [float]($cx + $size*0.12), [float]($cy - $size*0.24),
        [float]($cx + $size*0.18), [float]($cy - $size*0.06)
    )
    $capPath.AddBezier(
        [float]($cx + $size*0.18), [float]($cy - $size*0.06),
        [float]($cx + $size*0.10), [float]($cy - $size*0.01),
        [float]($cx - $size*0.10), [float]($cy - $size*0.01),
        [float]($cx - $size*0.18), [float]($cy - $size*0.06)
    )
    $capPath.CloseFigure()

    $capBrush = New-Object System.Drawing.Drawing2D.LinearGradientBrush(
        $rect,
        [System.Drawing.Color]::FromArgb(255, 155, 179, 204),
        [System.Drawing.Color]::FromArgb(255, 45, 72, 99),
        [System.Drawing.Drawing2D.LinearGradientMode]::Vertical
    )
    $g.FillPath($capBrush, $capPath)
    $capPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(255, 33, 53, 74), [float]($size * 0.012))
    $g.DrawPath($capPen, $capPath)

    # Visor
    $visorPath = New-Object System.Drawing.Drawing2D.GraphicsPath
    $visorPath.AddBezier(
        [float]($cx - $size*0.17), [float]($cy - $size*0.02),
        [float]($cx), [float]($cy + $size*0.09),
        [float]($cx), [float]($cy + $size*0.09),
        [float]($cx + $size*0.17), [float]($cy - $size*0.02)
    )
    $visorPath.AddBezier(
        [float]($cx + $size*0.17), [float]($cy - $size*0.02),
        [float]($cx), [float]($cy + $size*0.04),
        [float]($cx), [float]($cy + $size*0.04),
        [float]($cx - $size*0.17), [float]($cy - $size*0.02)
    )
    $visorPath.CloseFigure()
    $visorBrush = New-Object System.Drawing.Drawing2D.LinearGradientBrush(
        $rect,
        [System.Drawing.Color]::FromArgb(255, 74, 99, 125),
        [System.Drawing.Color]::FromArgb(255, 13, 23, 36),
        [System.Drawing.Drawing2D.LinearGradientMode]::Vertical
    )
    $g.FillPath($visorBrush, $visorPath)

    # 4. Three White Stars
    $starBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::White)
    
    function Draw-Star([System.Drawing.Graphics]$g, [float]$x, [float]$y, [float]$r) {
        $pts = @()
        for ($i = 0; $i -lt 10; $i++) {
            $angle = $i * [Math]::PI / 5 - [Math]::PI / 2
            $rad = if ($i % 2 -eq 0) { $r } else { $r * 0.4 }
            $px = $x + $rad * [Math]::Cos($angle)
            $py = $y + $rad * [Math]::Sin($angle)
            $pts += New-Object System.Drawing.PointF([float]$px, [float]$py)
        }
        $g.FillPolygon($starBrush, $pts)
    }

    $starRadius = [float]($size * 0.028)
    Draw-Star $g ($cx - $size*0.10) ($cy + $size*0.15) $starRadius
    Draw-Star $g ($cx + $size*0.10) ($cy + $size*0.15) $starRadius
    Draw-Star $g ($cx) ($cy + $size*0.23) $starRadius

    $targetFile = "$iconsDir\icon-$size.png"
    if ($size -eq 180) { $targetFile = "$iconsDir\apple-touch-icon.png" }
    $bmp.Save($targetFile, [System.Drawing.Imaging.ImageFormat]::Png)
    $g.Dispose()
    $bmp.Dispose()
    Write-Host "Gerado com sucesso: $targetFile"
}
