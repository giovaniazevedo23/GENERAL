import re

files = ['../gestor-app/index.html', '../gestor-app/motorista.html']
for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add ?v=4.4.0 to app.js and app_motorista.js
    content = re.sub(r'src="js/app\.js(\?v=[\d\.]+)?', 'src="js/app.js?v=4.4.0', content)
    content = re.sub(r'src="js/app_motorista\.js(\?v=[\d\.]+)?', 'src="js/app_motorista.js?v=4.4.0', content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
print('Updated HTML files cache busting query parameters')
