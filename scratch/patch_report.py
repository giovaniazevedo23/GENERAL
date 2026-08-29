import sys
import re

file_path = "js/report-pdf.js"
try:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
except UnicodeDecodeError:
    with open(file_path, "r", encoding="latin-1") as f:
        content = f.read()

# 1. Update Parecer Text
parecer_re = re.compile(r'const parecerText = incident\.parecerTecnico \|\| \'Nenhum parecer t[^\']*?\'\s*;')
content = parecer_re.sub("const parecerText = incident.docsParecer || incident.parecerTecnico || 'Nenhum parecer técnico adicional foi anexado pelo gestor até o momento da emissão deste dossiê.';", content)

# 2. Update vistoria fields
content = content.replace("document.getElementById('vistoria-clima')?.value", "(incident.vistoria && incident.vistoria.clima)")
content = content.replace("document.getElementById('vistoria-pista')?.value", "(incident.vistoria && incident.vistoria.pista)")
content = content.replace("document.getElementById('vistoria-veiculo')?.value", "(incident.vistoria && incident.vistoria.veiculo)")
content = content.replace("document.getElementById('vistoria-condutor')?.value", "(incident.vistoria && incident.vistoria.condutor)")
content = content.replace("document.getElementById('vistoria-lacre')?.value", "(incident.vistoria && incident.vistoria.lacre)")

try:
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
except Exception:
    with open(file_path, "w", encoding="latin-1") as f:
        f.write(content)

print("js/report-pdf.js patched.")
