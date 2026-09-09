import re

with open('../gestor-app/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# find the button for Umwelt
idx = content.find("'umwelt'")
if idx != -1:
    print(content[idx-100:idx+100])
