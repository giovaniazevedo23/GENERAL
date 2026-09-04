import re

def patch_index_html():
    with open('../index.html', 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()

    # 1. Add sidebar button
    sidebar_btn = """
          <button data-tab="driver-evaluations" onclick="App.switchTab('driver-evaluations')" class="nav-button w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-bold text-slate-400 hover:bg-slate-800 hover:text-slate-200 transition-all">
            <i data-lucide="clipboard-check" class="w-4 h-4 text-emerald-400"></i>
            Avaliações de Rota
          </button>
    """
    if 'data-tab="driver-evaluations"' not in html:
        idx = html.find('Painel do Gestor')
        if idx != -1:
            idx = html.find('</button>', idx) + 9
            html = html[:idx] + sidebar_btn + html[idx:]

    # 2. Add view container
    view_html = """
    <!-- VIEW: AVALIAÇÕES DE ROTA (GESTOR) -->
    <div id="view-driver-evaluations" class="tab-view hidden space-y-6">
      <h2 class="text-xl font-black text-white flex items-center gap-2">
        <i data-lucide="clipboard-check" class="w-6 h-6 text-emerald-400"></i>
        Avaliações de Rota (Motoristas)
      </h2>
      <p class="text-xs text-slate-400 mt-1">Laudos de infraestrutura e paradas avaliadas pelos motoristas.</p>
      
      <div id="driver-evaluations-container" class="space-y-4">
         <!-- Renderizado via JS -->
      </div>
    </div>
    """
    if 'id="view-driver-evaluations"' not in html:
        idx = html.find('<!-- CONTENT AREA -->')
        if idx != -1:
            idx = html.find('>', html.find('<main', idx)) + 1
            html = html[:idx] + '\n' + view_html + '\n' + html[idx:]

    with open('../index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("index.html patched for driver evaluations.")

def patch_app_js():
    with open('../js/app.js', 'r', encoding='utf-8', errors='ignore') as f:
        js = f.read()

    render_func = """
  renderDriverEvaluations() {
      const container = document.getElementById('driver-evaluations-container');
      if (!container) return;
      if (!window.db) {
          container.innerHTML = '<div class="p-4 bg-slate-900 border border-slate-800 rounded-xl text-center text-slate-400 text-sm">Banco de dados offline.</div>';
          return;
      }
      
      container.innerHTML = '<div class="p-4 bg-slate-900 border border-slate-800 rounded-xl text-center text-slate-400 text-sm"><i data-lucide="loader" class="w-5 h-5 animate-spin mx-auto mb-2"></i>Carregando avaliações...</div>';
      
      window.db.collection('route_evaluations').orderBy('timestamp', 'desc').limit(20).get().then(snapshot => {
          if (snapshot.empty) {
              container.innerHTML = '<div class="p-4 bg-slate-900 border border-slate-800 rounded-xl text-center text-slate-400 text-sm">Nenhuma avaliação encontrada.</div>';
              return;
          }
          
          let html = '';
          snapshot.forEach(doc => {
              const data = doc.data();
              const date = data.timestamp ? new Date(data.timestamp).toLocaleString() : 'Sem data';
              html += `
                <div class="bg-slate-900 border border-slate-800 p-5 rounded-2xl flex flex-col gap-3">
                  <div class="flex items-center justify-between">
                    <div>
                      <h4 class="text-sm font-bold text-white">${data.driverName || 'Motorista'} (${data.company || 'Sem empresa'})</h4>
                      <span class="text-xs text-slate-400">${date}</span>
                    </div>
                    <span class="px-2 py-1 bg-emerald-500/10 text-emerald-400 text-[10px] font-bold rounded-lg uppercase">Nota: ${data.rating || 5} <i data-lucide="star" class="w-3 h-3 inline"></i></span>
                  </div>
                  <p class="text-xs text-slate-300 bg-slate-950 p-3 rounded-xl border border-slate-800">${data.feedback || 'Sem comentários adicionais.'}</p>
                </div>
              `;
          });
          container.innerHTML = html;
          if (window.lucide) window.lucide.createIcons();
      }).catch(err => {
          console.error("Erro ao carregar avaliações", err);
          container.innerHTML = '<div class="p-4 bg-slate-900 border-red-500/20 rounded-xl text-center text-red-400 text-sm">Erro ao carregar avaliações.</div>';
      });
  },
"""
    if 'renderDriverEvaluations()' not in js:
        js = js.replace('methods: {', 'methods: {\n' + render_func)

    if 'if (this.currentTab === \'driver-evaluations\') this.renderDriverEvaluations();' not in js:
        # inject in appState.subscribe
        js = js.replace('if (this.currentTab === \'indicators\') this.renderIndicatorsTab();', 
                        "if (this.currentTab === 'indicators') this.renderIndicatorsTab();\n      if (this.currentTab === 'driver-evaluations') this.renderDriverEvaluations();")
        
    with open('../js/app.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("app.js patched for driver evaluations.")

if __name__ == '__main__':
    patch_index_html()
    patch_app_js()
