import re
js_path = r'C:\Users\giova\.gemini\antigravity\scratch\gestor-app\js\app.js'

with open(js_path, 'r', encoding='utf-8') as f:
    js_content = f.read()

if 'this.loadRegisteredDrivers();' not in js_content:
    js_content = js_content.replace(
        '''this.loadIncidentList();''',
        '''this.loadIncidentList();\n      this.loadRegisteredDrivers();'''
    )

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js_content)
