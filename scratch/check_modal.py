with open('../gestor-app/index.html', 'r', encoding='utf-8') as f:
    content = f.read()
import re
match = re.search(r'<div id="profile-modal"(.+?)<!-- Salvar button -->', content, re.DOTALL)
if match:
    print(match.group(1))
else:
    print('Modal not found')
