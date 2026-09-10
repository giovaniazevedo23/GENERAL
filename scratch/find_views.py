# -*- coding: utf-8 -*-
import re
html_path = r'C:\Users\giova\.gemini\antigravity\scratch\gestor-app\index.html'

with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

views = re.findall(r'<div\s+id="([^"]+-view)"\s+class="[^"]*view', html_content)
print(views)
