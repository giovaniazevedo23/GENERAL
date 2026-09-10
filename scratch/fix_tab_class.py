# -*- coding: utf-8 -*-
html_path = r'C:\Users\giova\.gemini\antigravity\scratch\gestor-app\index.html'

with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

html_content = html_content.replace(
    '''<div id="view-driver-registration" class="view hidden space-y-6">''',
    '''<div id="view-driver-registration" class="tab-view hidden space-y-6">'''
)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Fixed class to tab-view.")
