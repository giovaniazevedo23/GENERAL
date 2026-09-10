# -*- coding: utf-8 -*-
html_path = r'C:\Users\giova\.gemini\antigravity\scratch\gestor-app\index.html'

with open(html_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'id="reg-driver-cpf"' in line:
        lines[i] = '            <input type="text" id="reg-driver-cpf" required oninput="let v = this.value.replace(/\\\\D/g, \\'\\'); v = v.replace(/(\\\\d{3})(\\\\d)/, \\'.\\'); v = v.replace(/(\\\\d{3})(\\\\d)/, \\'.\\'); v = v.replace(/(\\\\d{3})(\\\\d{1,2})$/, \\'-\\'); this.value = v;" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2 text-white outline-none focus:border-blue-500 font-mono" placeholder="000.000.000-00" />\n'
        break

with open(html_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Fixed CPF input.")
