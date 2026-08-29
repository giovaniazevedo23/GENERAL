import sys
import re

file_path = "js/risk-engine.js"
try:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
except UnicodeDecodeError:
    with open(file_path, "r", encoding="latin-1") as f:
        content = f.read()

cargo_logic = '''
    // 2. Fator: Tipo de Carga e Periculosidade
    if (incident.cargoType === "PRODUTO_PERIGOSO") {
      score += 25;
      factors.push({ name: "Carga de Produto Perigoso (HazMat / ONU)", points: 25, type: "danger" });
      if (incident.damageCondition === "PERDA_PARCIAL_VAZAMENTO" || incident.damageCondition === "TOTAL") {
        score += 15;
        factors.push({ name: "Vazamento ativo de produto químico/inflamável", points: 15, type: "danger" });
        if (!incident.checklists.isolated) {
          actions.push({ priority: 2, title: "Isolar perímetro conforme Ficha de Emergência ONU", category: "SEGURANÇA" });
        }
        if (!incident.checklists.cetesbNotified) {
          actions.push({ priority: 3, title: "Notificar Órgão Ambiental e Empresa de Pronta Resposta", category: "AMBIENTAL" });
        }
      }
    } else {
      try {
        const catalog = JSON.parse(localStorage.getItem('GENERAL_CARGO_CATALOG') || '[]');
        const cargo = catalog.find(c => c.name === incident.cargoType);
        if (cargo) {
          score += cargo.risk;
          factors.push({ name: `Carga: ${cargo.name} (${cargo.category})`, points: cargo.risk, type: cargo.risk > 40 ? "danger" : "warning" });
        } else if (incident.cargoType === "ALTO_VALOR") {
          score += 15;
          factors.push({ name: "Carga de Alto Valor Agregado (Risco de Saque/Roubo)", points: 15, type: "warning" });
          if (!incident.checklists.isolated) {
            actions.push({ priority: 2, title: "Posicionar Escolta Armada / Preservação no Local", category: "PATRIMÔNIO" });
          }
        }
      } catch(e) {}
    }
'''

# Find the start and end of the Fator 2 block to replace it
start_idx = content.find('// 2. Fator: Tipo de Carga e Periculosidade')
end_idx = content.find('// 3. Fator: Condições da Pista e Clima')

if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + cargo_logic + "\n    " + content[end_idx:]

try:
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
except Exception:
    with open(file_path, "w", encoding="latin-1") as f:
        f.write(content)

print("js/risk-engine.js patched for dynamic cargo risk.")
