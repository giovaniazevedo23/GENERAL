import re

file_path = r'C:\Users\giova\.gemini\antigravity\scratch\gestor-app\js\app.js'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the specific syntax error
pattern = r"    let css = '';\n \} catch\(e\) \{ console\.warn\('localStorage denied'\); \}\n    let styleEl = document\.getElementById\('dynamic-theme'\);\n    if \(\!styleEl\) \{\n      styleEl = document\.createElement\('style'\);\n      styleEl\.id = 'dynamic-theme';\n      document\.head\.appendChild\(styleEl\);\n    \}\n    \n    let css = '';"
replacement = "    let css = '';"
new_content = re.sub(pattern, replacement, content, count=1)

if content != new_content:
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Fixed!")
else:
    print("Pattern not found!")
