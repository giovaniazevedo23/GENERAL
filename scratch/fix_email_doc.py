import re
files = [
    r'C:\Users\giova\.gemini\antigravity\scratch\gestor-app\js\app.js',
    r'C:\Users\giova\.gemini\antigravity\scratch\general-app\js\app.js'
]
for file_path in files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        pattern = r"window\.db\.collection\('users'\)\.doc\(window\.tempGoogleUser\.email\)\.set\("
        repl = r"window.db.collection('users').doc(window.tempGoogleUser.email || window.tempGoogleUser.id).set("
        content = re.sub(pattern, repl, content)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {file_path}")
    except Exception as e:
        print(f"Error in {file_path}: {e}")
