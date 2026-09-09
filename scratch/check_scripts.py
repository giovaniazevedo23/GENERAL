with open('../gestor-app/index.html', 'r', encoding='utf-8') as f:
    content = f.read()
import re
for match in re.finditer(r'<script[^>]*src="([^"]+)"', content):
    print(match.group(1))
