import re

files = [
    r'C:\Users\giova\.gemini\antigravity\scratch\gestor-app\js\app.js',
    r'C:\Users\giova\.gemini\antigravity\scratch\general-app\js\app.js'
]

for file_path in files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Fix 1: submitGoogleExtraInfo
        pattern1 = r"window\.db\.collection\('companies'\)\.doc\(cnpj\)\.set\(\{ name: company, cnpj: cnpj \}\)"
        repl1 = r"window.db.collection('companies').doc(cnpj.replace(/\\D/g, '')).set({ name: company, cnpj: cnpj })"
        content = re.sub(pattern1, repl1, content)
        
        # Fix 2: saveProfile
        pattern2 = r"let cDoc = newCnpj \? newCnpj : newCompany;"
        repl2 = r"let cDoc = newCnpj ? newCnpj.replace(/\\D/g, '') : newCompany.replace(/\\//g, '-');"
        content = re.sub(pattern2, repl2, content)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {file_path}")
    except Exception as e:
        print(f"Error in {file_path}: {e}")
