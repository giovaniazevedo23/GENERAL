# -*- coding: utf-8 -*-
html_path = r'C:\Users\giova\.gemini\antigravity\scratch\gestor-app\index.html'

with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

html_content = html_content.replace(
    '''v = v.replace(/(\d{3})(\d)/, '.'); v = v.replace(/(\d{3})(\d)/, '.'); v = v.replace(/(\d{3})(\d{1,2})$/, '-');''',
    '''v = v.replace(/(\d{3})(\d)/, '.'); v = v.replace(/(\d{3})(\d)/, '.'); v = v.replace(/(\d{3})(\d{1,2})$/, '-');'''
)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Fixed CPF input.")
