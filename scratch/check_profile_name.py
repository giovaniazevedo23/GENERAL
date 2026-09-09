with open('../gestor-app/index.html', 'r', encoding='utf-8') as f:
    content = f.read()
import re
match = re.search(r'<input[^>]*id="profile-name"', content)
if match:
    print('profile-name exists!')
else:
    print('profile-name DOES NOT EXIST!')
