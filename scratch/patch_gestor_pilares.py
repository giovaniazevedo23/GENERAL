import re

def patch_index():
    with open('../index.html', 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()

    # 1. Adicionar seletor de Patente/Cargo no login
    login_role_html = """        <div class="mt-4">
          <label class="block text-xs font-bold text-slate-300 mb-1">Patente de Comando (Controle de Acesso)</label>
          <select id="login-role" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-slate-200 focus:border-blue-500 outline-none transition-all">
            <option value="Administrador Geral">Administrador Geral</option>
            <option value="Coordenador de Frota">Coordenador de Frota</option>
            <option value="Despachante">Despachante</option>
          </select>
        </div>"""
    
    # Inserir antes de btn-action-login
    if 'id="login-role"' not in html:
        html = re.sub(r'(<button type="button" id="btn-action-login")', login_role_html + r'\n\n        \1', html)

    # 2. Encontrar aba de indicadores e adicionar Tropa de Elite
    elite_html = """
      <!-- TROPA DE ELITE WIDGET -->
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg relative overflow-hidden">
        <div class="absolute top-0 right-0 w-32 h-32 bg-amber-500/5 rounded-bl-full pointer-events-none"></div>
        <div class="flex items-center gap-3 mb-6">
          <div class="w-10 h-10 rounded-xl bg-amber-500/10 flex items-center justify-center border border-amber-500/20">
            <i data-lucide="award" class="w-5 h-5 text-amber-500"></i>
          </div>
          <div>
            <h3 class="text-sm font-black text-white uppercase tracking-wider">Tropa de Elite</h3>
            <p class="text-xs text-slate-400">Ranking dos melhores motoristas</p>
          </div>
        </div>
        <div id="elite-squad-container" class="space-y-3">
          <!-- Renderizado via JS -->
        </div>
      </div>
"""
    if 'TROPA DE ELITE WIDGET' not in html:
        # Se 'view-indicators' existe, achar onde injetar
        if 'id="view-indicators"' in html:
            # Injecting after the first grid container inside view-indicators
            html = re.sub(r'(id="view-indicators".*?<div class="grid grid-cols-1 lg:grid-cols-[2-3] gap-6 mb-6">)', r'\1\n' + elite_html, html, flags=re.DOTALL)
        else:
            print("WARNING: view-indicators not found in HTML")

    with open('../index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("index.html modificado.")

def patch_app_js():
    with open('../js/app.js', 'r', encoding='utf-8', errors='ignore') as f:
        js = f.read()

    # Adicionar verificação no logout
    if 'this.renderEliteSquad();' not in js:
        js = re.sub(r'(renderIndicatorsTab\(\) \{.*?\n)', r'\1    this.renderEliteSquad();\n', js, flags=re.DOTALL)

    # Adicionar a função renderEliteSquad
    if 'renderEliteSquad()' not in js:
        elite_func = """
  renderEliteSquad() {
    const container = document.getElementById('elite-squad-container');
    if (!container) return;

    const drivers = [
      { name: 'Marcos Silva', rank: 'Elite', score: 99, trips: 142 },
      { name: 'João Santos', rank: 'Veterano', score: 95, trips: 110 },
      { name: 'Ana Costa', rank: 'Especialista', score: 89, trips: 75 }
    ];

    container.innerHTML = drivers.map((d, i) => `
      <div class="flex items-center justify-between p-3 rounded-xl border border-slate-800 bg-slate-950/50">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-lg ${i === 0 ? 'bg-amber-500 text-white' : i === 1 ? 'bg-slate-400 text-slate-900' : 'bg-orange-700 text-white'} font-black flex items-center justify-center text-xs">
            #${i+1}
          </div>
          <div class="flex flex-col">
            <span class="text-sm font-bold text-white">${d.name}</span>
            <span class="text-[10px] font-bold text-amber-500 uppercase tracking-widest">${d.rank}</span>
          </div>
        </div>
        <div class="text-right flex flex-col">
          <span class="text-xs font-black text-emerald-400">${d.score} pts</span>
          <span class="text-[9px] text-slate-500">${d.trips} missões</span>
        </div>
      </div>
    `).join('');
  },
"""
        js = re.sub(r'(renderIndicatorsTab\(\) \{)', elite_func + r'\n  \1', js)

    # 3. Restringir acesso a Finalizar Ocorrência
    if 'Acesso Negado: Apenas Administrador' not in js:
        # Achar a função openFinishIncidentModal e injetar a restrição
        restriction = """
    if (appState.currentUser && appState.currentUser.role !== 'Administrador Geral') {
      this.showToast('⚠️ Acesso Negado: Apenas Administrador Geral pode finalizar ocorrências (Cadeia de Comando).');
      return;
    }
"""
        js = re.sub(r'(openFinishIncidentModal\(\) \{)', r'\1' + restriction, js)

    with open('../js/app.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("app.js modificado.")

patch_index()
patch_app_js()
