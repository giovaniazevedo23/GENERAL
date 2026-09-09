def fix_html(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace("App.setTheme(\\'", "App.setTheme('").replace("\\')", "')")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
fix_html('../gestor-app/index.html')
fix_html('../gestor-app/motorista.html')
