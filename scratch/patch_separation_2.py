import sys
import re

def patch_motorista_html():
    file_path = r"c:\Users\giova\.gemini\antigravity\scratch\general-app\motorista.html"
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Add Select to Monitoramento Tático
    old_monitoramento_header = """          <div class="flex items-center justify-between mb-6">
            <div>
              <h3 class="text-white font-bold text-lg">Monitoramento Tático do Plano</h3>
              <p class="text-xs text-slate-400">Acompanhamento em tempo real da execução e auditoria de atividades.</p>
            </div>
            <button onclick="App.advancePlanStatus()" class="bg-emerald-600 hover:bg-emerald-700 text-white px-4 py-2 rounded-lg text-xs font-bold shadow-lg shadow-emerald-900/20 transition-all flex items-center gap-2">
              Avançar Etapa <i data-lucide="arrow-right" class="w-4 h-4"></i>
            </button>
          </div>"""
          
    new_monitoramento_header = """          <div class="flex items-center justify-between mb-4">
            <div>
              <h3 class="text-white font-bold text-lg">Monitoramento Tático do Plano</h3>
              <p class="text-xs text-slate-400">Acompanhamento em tempo real da execução e auditoria de atividades.</p>
            </div>
            <button onclick="App.advancePlanStatus()" class="bg-emerald-600 hover:bg-emerald-700 text-white px-4 py-2 rounded-lg text-xs font-bold shadow-lg shadow-emerald-900/20 transition-all flex items-center gap-2">
              Avançar Etapa <i data-lucide="arrow-right" class="w-4 h-4"></i>
            </button>
          </div>
          
          <div class="mb-8 p-4 bg-slate-950/50 border border-slate-800 rounded-xl">
            <label class="block text-xs font-bold text-emerald-400 mb-2 uppercase tracking-wider">Selecionar Plano para Monitorar</label>
            <select id="tactical-plan-selector" onchange="App.loadTacticalMonitoring()" class="w-full bg-slate-900 border border-emerald-900/50 rounded-lg px-4 py-3 text-sm text-white focus:outline-none focus:border-emerald-500 transition-all cursor-pointer">
              <option value="">Selecione um plano aprovado...</option>
            </select>
          </div>"""
    content = content.replace(old_monitoramento_header, new_monitoramento_header)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

def patch_app_js():
    file_path = r"c:\Users\giova\.gemini\antigravity\scratch\general-app\js\app.js"
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Update Cargo Catalog Initialization to use CNPJ
    old_init_cargo = """  initCargoCatalog() {
    let catalog = JSON.parse(localStorage.getItem('GENERAL_CARGO_CATALOG') || 'null');"""
    new_init_cargo = """  initCargoCatalog() {
    const cnpj = (appState.currentUser && appState.currentUser.companyCnpj) ? appState.currentUser.companyCnpj : 'default';
    let catalog = JSON.parse(localStorage.getItem(`GENERAL_CARGO_CATALOG_${cnpj}`) || 'null');"""
    content = content.replace(old_init_cargo, new_init_cargo)
    
    old_save_catalog_1 = """localStorage.setItem('GENERAL_CARGO_CATALOG', JSON.stringify(catalog));"""
    new_save_catalog_1 = """localStorage.setItem(`GENERAL_CARGO_CATALOG_${(appState.currentUser && appState.currentUser.companyCnpj) ? appState.currentUser.companyCnpj : 'default'}`, JSON.stringify(catalog));"""
    content = content.replace(old_save_catalog_1, new_save_catalog_1)
    
    old_save_catalog_2 = """localStorage.setItem('GENERAL_CARGO_CATALOG', JSON.stringify(this.cargoCatalog));"""
    new_save_catalog_2 = """const cnpj = (appState.currentUser && appState.currentUser.companyCnpj) ? appState.currentUser.companyCnpj : 'default';
    localStorage.setItem(`GENERAL_CARGO_CATALOG_${cnpj}`, JSON.stringify(this.cargoCatalog));"""
    content = content.replace(old_save_catalog_2, new_save_catalog_2)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

def patch_app_motorista_js():
    file_path = r"c:\Users\giova\.gemini\antigravity\scratch\general-app\js\app_motorista.js"
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Add Tactical monitoring select and renderIndicatorsTab logic
    additional_code = """
  loadTacticalMonitoring() {
    const selector = document.getElementById('tactical-plan-selector');
    if (!selector || !selector.value) return;
    
    this.showToast('Plano carregado para monitoramento tático.', 'success');
    // Here we would normally fetch steps specific to this plan.
    // For demo purposes, we just reset the stepper to step 1.
    this.planStatusStep = 1;
    this.updateStepperUI();
    const log = document.getElementById('plan-activity-log');
    if (log) log.innerHTML = `<div class="text-[10px] text-slate-500 text-center italic">Aguardando início das atividades para ${selector.value}.</div>`;
  },
  
  renderIndicatorsTab() {
    // Driver-specific KPIs
    const plans = appState.savedPlans || [];
    const incidents = (appState.incidents || []).filter(i => i.status !== 'CONCLUIDA');
    
    const kpiIncidents = document.getElementById('kpi-total-incidents');
    const kpiFreq = document.getElementById('kpi-freq-incidents');
    const kpiCost = document.getElementById('kpi-total-cost');
    const kpiAffected = document.getElementById('kpi-affected-deliveries');
    
    if (kpiIncidents) kpiIncidents.textContent = incidents.length;
    if (kpiFreq) kpiFreq.textContent = plans.length > 0 ? Math.round((incidents.length / plans.length) * 100) + '%' : '0%';
    if (kpiCost) kpiCost.textContent = (incidents.length * 1500).toLocaleString('pt-BR');
    if (kpiAffected) kpiAffected.textContent = plans.length > 0 ? Math.round((incidents.length / plans.length) * 100) + '%' : '0%';
    
    // Simulate updating bars
    const setBar = (id, percent) => {
        const bar = document.getElementById(`bar-grav-${id}`);
        const val = document.getElementById(`val-grav-${id}`);
        if(bar) bar.style.width = percent + '%';
        if(val) val.textContent = percent + '%';
    };
    
    if (incidents.length === 0) {
        setBar('critical', 0);
        setBar('high', 0);
        setBar('medium', 0);
    } else {
        setBar('critical', 10);
        setBar('high', 30);
        setBar('medium', 60);
    }
  },
"""

    # We will inject this before the last closing brace.
    closing_brace = content.rfind('}')
    if content.rfind('}') != -1:
        content = content[:content.rfind('}')] + additional_code + "\n}"

    # We also need to populate the tactical-plan-selector inside renderSavedPlansTab or switchTab
    old_switch_tab = """  switchTab(tabId) {"""
    new_switch_tab = """  switchTab(tabId) {
    if (tabId === 'monitoring') {
        const selector = document.getElementById('tactical-plan-selector');
        if (selector && appState.savedPlans) {
            const currentVal = selector.value;
            selector.innerHTML = '<option value="">Selecione um plano aprovado...</option>' + 
                appState.savedPlans.map(p => `<option value="${p.id}">${p.id} - ${p.destination}</option>`).join('');
            selector.value = currentVal;
        }
    }
    if (tabId === 'indicators') {
        this.renderIndicatorsTab();
    }"""
    content = content.replace(old_switch_tab, new_switch_tab)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    patch_motorista_html()
    patch_app_js()
    patch_app_motorista_js()
    print("Patch 2 applied.")
