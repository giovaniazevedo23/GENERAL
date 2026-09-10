# -*- coding: utf-8 -*-
import re
html_path = r'C:\Users\giova\.gemini\antigravity\scratch\gestor-app\index.html'

with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Let's find any div that has class containing "view"
views = re.findall(r'<div[^>]*?id="([^"]+)"[^>]*?class="[^"]*\bview\b[^"]*"', html_content)
print("Views:", views)
