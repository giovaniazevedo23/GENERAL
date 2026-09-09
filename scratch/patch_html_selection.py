import re

def patch_html(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # We need to add 'theme-btn' and 'data-theme="..."' to the buttons,
    # and 'theme-ring' to the div containing the colors.
    
    # 1. Padrão
    content = re.sub(
        r'<button onclick="if\(window.App\) App.setTheme\(\'default\'\)" class="([^"]*)">(\s*)<div class="([^"]*)">',
        r'<button onclick="if(window.App) App.setTheme(\'default\')" class="\1 theme-btn" data-theme="default">\2<div class="\3 theme-ring">',
        content
    )
    
    # 2. Superhero (Cheesecake)
    content = re.sub(
        r'<button onclick="if\(window.App\) App.setTheme\(\'superhero\'\)" class="([^"]*)">(\s*)<div class="([^"]*)" style="background-color: #1F2605;">',
        r'<button onclick="if(window.App) App.setTheme(\'superhero\')" class="\1 theme-btn" data-theme="superhero">\2<div class="\3 theme-ring" style="background-color: #0a3314;">',
        content
    )
    # Also update the inner halves for Superhero
    content = re.sub(r'<div class="w-1/2 h-full" style="background-color: #1F6521;"></div>', r'<div class="w-1/2 h-full" style="background-color: #1a7a34;"></div>', content)
    
    # 3. Nurture
    content = re.sub(
        r'<button onclick="if\(window.App\) App.setTheme\(\'nurture\'\)" class="([^"]*)">(\s*)<div class="([^"]*)" style="background-color: #182628;">',
        r'<button onclick="if(window.App) App.setTheme(\'nurture\')" class="\1 theme-btn" data-theme="nurture">\2<div class="\3 theme-ring" style="background-color: #0a3133;">',
        content
    )
    # Also update the inner halves for Nurture
    content = re.sub(r'<div class="w-1/2 h-full" style="background-color: #2a4043;"></div>', r'<div class="w-1/2 h-full" style="background-color: #1a7a7e;"></div>', content)

    # 4. Five Hundred
    content = re.sub(
        r'<button onclick="if\(window.App\) App.setTheme\(\'fivehundred\'\)" class="([^"]*)">(\s*)<div class="([^"]*)" style="background-color: #2D1A3C;">',
        r'<button onclick="if(window.App) App.setTheme(\'fivehundred\')" class="\1 theme-btn" data-theme="fivehundred">\2<div class="\3 theme-ring" style="background-color: #1c0d2e;">',
        content
    )
    # Also update the inner halves for Five Hundred
    content = re.sub(r'<div class="w-1/2 h-full" style="background-color: #4b2663;"></div>', r'<div class="w-1/2 h-full" style="background-color: #4f2680;"></div>', content)

    # 5. Umwelt
    content = re.sub(
        r'<button onclick="if\(window.App\) App.setTheme\(\'umwelt\'\)" class="([^"]*)">(\s*)<div class="([^"]*)" style="background-color: #0d1619;">',
        r'<button onclick="if(window.App) App.setTheme(\'umwelt\')" class="\1 theme-btn" data-theme="umwelt">\2<div class="\3 theme-ring" style="background-color: #092a33;">',
        content
    )
    # Also update the inner halves for Umwelt
    content = re.sub(r'<div class="w-1/2 h-full" style="background-color: #17252A;"></div>', r'<div class="w-1/2 h-full" style="background-color: #176e82;"></div>', content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Patched HTML in {filepath}")

patch_html('../gestor-app/index.html')
patch_html('../gestor-app/motorista.html')
