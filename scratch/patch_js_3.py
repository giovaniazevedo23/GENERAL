import sys
import re

file_path = "js/app.js"
try:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
except UnicodeDecodeError:
    with open(file_path, "r", encoding="latin-1") as f:
        content = f.read()

# 1. Update renderDossierTab
render_dossier_re = re.compile(r'(renderDossierTab\(\) \{)(.*?)(if \(!inc\) \{)(.*?)(return;\n\s*\})', re.DOTALL)
def replace_render_dossier(match):
    return '''renderDossierTab() {
      const sel = document.getElementById('dossier-incident-select');
      const inc = (sel && sel.value) ? appState.incidents.find(i => i.id === sel.value) : null;
      const container = document.getElementById('dossier-preview-container');
      if (!container) return;
      
      if (!inc) {''' + match.group(4) + match.group(5)
content = render_dossier_re.sub(replace_render_dossier, content)

# 2. Add submitParecer and saveIshikawa
methods_to_add = '''

  submitParecer() {
    const inc = appState.getCurrentIncident();
    if (!inc) return;
    const textarea = document.getElementById('docs-parecer');
    if (!textarea) return;
    appState.updateCurrentIncident({ docsParecer: textarea.value });
    textarea.value = '';
    this.showToast('Parecer Técnico salvo e enviado para o Dossiê!', 'success');
  },

  saveIshikawa() {
    const inc = appState.getCurrentIncident();
    if (!inc) return;
    
    // Pegar dados da vistoria
    const vistoria = {
      clima: document.getElementById('vistoria-clima')?.value || '',
      pista: document.getElementById('vistoria-pista')?.value || '',
      lacre: document.getElementById('vistoria-lacre')?.value || '',
      condutor: document.getElementById('vistoria-condutor')?.value || '',
      veiculo: document.getElementById('vistoria-veiculo')?.value || ''
    };
    
    appState.updateCurrentIncident({ vistoria });
    this.showToast('Investigação de Causa Raiz e Vistoria salvas com sucesso!', 'success');
  },

  // CATÁLOGO DE CARGAS
  initCargoCatalog() {
    let catalog = JSON.parse(localStorage.getItem('GENERAL_CARGO_CATALOG') || 'null');
    if (!catalog) {
      catalog = [
        { id: 1, name: 'Caixas de Eletrônicos', category: 'Cargas Gerais', risk: 20 },
        { id: 2, name: 'Carnes e Congelados', category: 'Carga Frigorífica', risk: 40 },
        { id: 3, name: 'Gado de Corte', category: 'Cargas Vivas', risk: 50 },
        { id: 4, name: 'Turbina Eólica', category: 'Carga Indivisível', risk: 60 },
        { id: 5, name: 'Soja a Granel', category: 'Carga a Granéis', risk: 70 }
      ];
      localStorage.setItem('GENERAL_CARGO_CATALOG', JSON.stringify(catalog));
    }
    this.cargoCatalog = catalog;
  },

  renderCargoCatalog() {
    const container = document.getElementById('cargo-catalog-list');
    if (!container) return;
    
    if (this.cargoCatalog.length === 0) {
      container.innerHTML = '<div class="text-center text-slate-500 py-10">Nenhuma carga cadastrada.</div>';
      return;
    }
    
    container.innerHTML = this.cargoCatalog.map(c => `
      <div class="bg-slate-900 border border-slate-800 p-4 rounded-xl flex items-center justify-between hover:border-amber-500/50 transition-all">
        <div class="flex items-center gap-4">
          <div class="w-10 h-10 rounded-full bg-amber-500/10 text-amber-500 flex items-center justify-center font-bold">
            ${c.risk}
          </div>
          <div>
            <h4 class="font-bold text-white text-sm">${c.name}</h4>
            <p class="text-[10px] text-slate-400 uppercase">${c.category}</p>
          </div>
        </div>
        <button onclick="App.deleteCargo(${c.id})" class="text-slate-500 hover:text-red-500 transition-colors">
          <i data-lucide="trash-2" class="w-4 h-4"></i>
        </button>
      </div>
    `).join('');
    
    if (typeof lucide !== 'undefined') lucide.createIcons();
    this.populateCargoDropdowns();
  },

  openAddCargoModal() {
    document.getElementById('add-cargo-modal').classList.remove('hidden');
    document.getElementById('new-cargo-name').value = '';
    this.updateCargoRiskEstimate();
  },

  updateCargoRiskEstimate() {
    const cat = document.getElementById('new-cargo-category').value;
    const riskInput = document.getElementById('new-cargo-risk');
    let risk = 20;
    if (cat === 'Carga Frigorífica') risk = 40;
    if (cat === 'Cargas Vivas') risk = 50;
    if (cat === 'Carga Indivisível') risk = 60;
    if (cat === 'Carga a Granéis') risk = 70;
    riskInput.value = risk;
  },

  saveNewCargo() {
    const name = document.getElementById('new-cargo-name').value;
    const category = document.getElementById('new-cargo-category').value;
    const risk = parseInt(document.getElementById('new-cargo-risk').value, 10);
    
    if (!name) {
      this.showToast('Preencha o nome da carga', 'error');
      return;
    }
    
    const newCargo = { id: Date.now(), name, category, risk };
    this.cargoCatalog.push(newCargo);
    localStorage.setItem('GENERAL_CARGO_CATALOG', JSON.stringify(this.cargoCatalog));
    
    document.getElementById('add-cargo-modal').classList.add('hidden');
    this.showToast('Carga adicionada ao catálogo!', 'success');
    this.renderCargoCatalog();
  },

  deleteCargo(id) {
    if (confirm('Deseja realmente remover esta carga?')) {
      this.cargoCatalog = this.cargoCatalog.filter(c => c.id !== id);
      localStorage.setItem('GENERAL_CARGO_CATALOG', JSON.stringify(this.cargoCatalog));
      this.renderCargoCatalog();
    }
  },

  populateCargoDropdowns() {
    const opts = '<option value="">Selecione o tipo de carga...</option>' + 
                 this.cargoCatalog.map(c => `<option value="${c.name}">${c.name} (Risco ${c.risk})</option>`).join('');
    const els = ['plan-cargo', 'incident-cargo', 'select-cargo'];
    els.forEach(id => {
      const el = document.getElementById(id);
      if (el) el.innerHTML = opts;
    });
  },

'''

init_re = re.compile(r'(init\(\) \{.*?\n  \},)', re.DOTALL)
match_init = init_re.search(content)
if match_init:
    content = content[:match_init.end()] + methods_to_add + content[match_init.end():]

init_content_re = re.compile(r'(init\(\) \{)')
content = init_content_re.sub(r'\1\n    this.initCargoCatalog();\n    this.populateCargoDropdowns();', content)

switchTab_re = re.compile(r'(if \(\[\'investigation\', \'dossier\', \'reverse-logistics\'\]\.includes\(tabId\)\) \{ this\.populateIncidentSelectors\(\); \})', re.DOTALL)
content = switchTab_re.sub(r"\1\n    if (tabId === 'cargo-catalog') { this.renderCargoCatalog(); }", content)

try:
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
except Exception:
    with open(file_path, "w", encoding="latin-1") as f:
        f.write(content)

print("js/app.js patched for cargo and dossier logic.")
