import re

with open('../gestor-app/index.html', 'r', encoding='utf-8') as f:
    content = f.read()
    
for match in re.finditer(r'<button[^>]*data-theme="([^"]*)"[^>]*>.*?<div[^>]*class="[^"]*theme-ring[^"]*"', content, re.DOTALL):
    print(match.group(1), 'has theme-ring')
