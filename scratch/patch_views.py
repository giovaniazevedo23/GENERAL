import sys
import re

file_path = "index.html"

try:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
except UnicodeDecodeError:
    with open(file_path, "r", encoding="latin-1") as f:
        content = f.read()

# 1. Ishikawa & Dossiê Selectors
ishikawa_select = '''
        <!-- Seleção de Ocorrência -->
        <div class="bg-slate-900/60 border border-slate-800 p-5 rounded-2xl">
          <label class="block text-xs font-bold text-slate-300 mb-2">Selecione a Ocorrência (Necessário para avaliação):</label>
          <select id="ishikawa-incident-select" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-3 text-sm text-slate-200 focus:border-purple-500 outline-none transition-all" onchange="App.handleIshikawaIncidentSelect()">
            <option value="">Selecione uma ocorrência ativa...</option>
          </select>
        </div>
'''
# Find <div id="view-investigation" class="tab-view hidden space-y-6"> and insert
content = content.replace('<div id="view-investigation" class="tab-view hidden space-y-6">', 
                          '<div id="view-investigation" class="tab-view hidden space-y-6">\n' + ishikawa_select)


dossier_select = '''
        <!-- Seleção de Ocorrência -->
        <div class="bg-slate-900/60 border border-slate-800 p-5 rounded-2xl">
          <label class="block text-xs font-bold text-slate-300 mb-2">Selecione a Ocorrência (Necessário para avaliação):</label>
          <select id="dossier-incident-select" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-3 text-sm text-slate-200 focus:border-blue-500 outline-none transition-all" onchange="App.handleDossierIncidentSelect()">
            <option value="">Selecione uma ocorrência ativa...</option>
          </select>
        </div>
'''
content = content.replace('<div id="view-dossier" class="tab-view hidden space-y-6">', 
                          '<div id="view-dossier" class="tab-view hidden space-y-6">\n' + dossier_select)


# 2. Copilot Tático replacing Manual de Uso
manual_de_uso_re = re.compile(r'<a href="#" onclick="App\.showToast\(\'Em breve:[^"]+"\)\s*class="bg-blue-950/30[^>]+>.*?Manual de Uso.*?</a>', re.DOTALL)
copilot_card = '''
          <a href="#" onclick="App.toggleCopilot()" class="bg-purple-950/30 border border-purple-900/50 rounded-xl p-4 flex flex-col items-center justify-center gap-2 hover:bg-purple-900/40 transition-colors relative">
            <span class="absolute -top-2 -right-2 flex h-4 w-4">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-purple-400 opacity-75"></span>
              <span class="relative inline-flex rounded-full h-4 w-4 bg-purple-500"></span>
            </span>
            <i data-lucide="bot" class="w-6 h-6 text-purple-400"></i>
            <span class="text-xs font-bold text-purple-300">Copilot Tático 24h</span>
            <span class="text-[9px] text-slate-400 text-center">IA Auxiliar</span>
          </a>
'''
content = manual_de_uso_re.sub(copilot_card, content, 1)

# 3. Logística Reversa View
reverse_logistics_view = '''
      <!-- ============================================== -->
      <!-- VIEW: LOGÍSTICA REVERSA E REAPROVEITAMENTO -->
      <!-- ============================================== -->
      <div id="view-reverse-logistics" class="tab-view hidden space-y-6">
        <div class="bg-gradient-to-r from-emerald-950 via-slate-900 to-green-950 border border-emerald-800/40 p-6 rounded-2xl">
          <h2 class="text-xl font-black text-white flex items-center gap-2">
            <i data-lucide="recycle" class="w-6 h-6 text-emerald-400"></i>
            Logística Reversa & Reaproveitamento
          </h2>
          <p class="text-xs text-slate-400 mt-1">
            Processo de avaliação e destinação de mercadorias com perda parcial ou desistência do cliente para reciclagem e recondicionamento.
          </p>
        </div>

        <div class="bg-slate-900/60 border border-slate-800 p-5 rounded-2xl">
          <label class="block text-xs font-bold text-slate-300 mb-2">Selecione a Ocorrência (Necessário para avaliação):</label>
          <select id="reverse-incident-select" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-3 text-sm text-slate-200 focus:border-emerald-500 outline-none transition-all" onchange="App.handleReverseIncidentSelect()">
            <option value="">Selecione uma ocorrência ativa...</option>
          </select>
        </div>

        <div id="reverse-logistics-form" class="bg-slate-900/60 border border-slate-800 p-6 rounded-2xl hidden">
          <h3 class="text-sm font-bold text-white mb-4 flex items-center gap-2">
            <i data-lucide="clipboard-list" class="w-4 h-4 text-emerald-400"></i>
            Avaliação de Estado e Destinação
          </h3>
          
          <div class="space-y-4">
            <div>
              <label class="block text-xs font-bold text-slate-400 mb-1">Situação dos Produtos Rejeitados</label>
              <select id="reverse-status" class="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-xs text-white">
                <option value="REAPROVEITADO">Aprovado para Reaproveitamento</option>
                <option value="CONSERTO">Produto para Conserto / Recondicionamento</option>
                <option value="SUCATA">Descarte / Sucata</option>
              </select>
            </div>
            
            <div>
              <label class="block text-xs font-bold text-slate-400 mb-1">Empresa Parceira Responsável</label>
              <select id="reverse-company" class="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-xs text-white">
                <option value="EcoLogística SA">EcoLogística SA</option>
                <option value="RecondicionaTudo">RecondicionaTudo LTDA</option>
                <option value="CicloVerde Reciclagem">CicloVerde Reciclagem Ambiental</option>
                <option value="DevolveRápido Log">DevolveRápido Logística Reversa</option>
              </select>
            </div>
            
            <button onclick="App.submitReverseLogistics()" class="w-full bg-emerald-600 hover:bg-emerald-500 text-white font-bold rounded-xl py-3 text-sm transition-all shadow-lg flex items-center justify-center gap-2">
              <i data-lucide="check-circle" class="w-4 h-4"></i>
              Processar Logística Reversa
            </button>
          </div>
        </div>
      </div>
'''

view_dashboard_marker = '<div id="view-dashboard"'
idx_dash = content.find(view_dashboard_marker)
if idx_dash != -1:
    content = content[:idx_dash] + reverse_logistics_view + "\n" + content[idx_dash:]

# Add "Logística Reversa" to sidebar menu
sidebar_dossier_btn_re = re.compile(r'(<button data-tab="dossier"[^>]+>.*?Dossiê PDF Oficial\s*</button>)', re.DOTALL)
reverse_sidebar_btn = '''
          <button data-tab="reverse-logistics" onclick="App.switchTab('reverse-logistics')" class="nav-button w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-bold text-slate-400 hover:bg-slate-800 hover:text-slate-200 transition-all">
            <i data-lucide="recycle" class="w-4 h-4 text-emerald-400"></i>
            Logística Reversa
          </button>
'''
match_d = sidebar_dossier_btn_re.search(content)
if match_d:
    content = content[:match_d.end()] + reverse_sidebar_btn + content[match_d.end():]

# Add "Logística Reversa" to drawer menu
drawer_dossier_btn_re = re.compile(r'(<button data-tab="dossier"[^>]+>.*?Dossiê PDF Oficial\s*</button>)', re.DOTALL)
# It will match again, but after the first match. We need to find all matches and append.
matches = list(drawer_dossier_btn_re.finditer(content))
if len(matches) > 1:
    match_d2 = matches[-1]
    reverse_drawer_btn = '''
              <button data-tab="reverse-logistics" onclick="App.switchTab('reverse-logistics'); App.toggleMobileDrawer();" class="nav-button w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-bold text-slate-400 hover:bg-slate-800 transition-all">
                <i data-lucide="recycle" class="w-4 h-4 text-emerald-400"></i>
                Logística Reversa
              </button>
'''
    content = content[:match_d2.end()] + reverse_drawer_btn + content[match_d2.end():]


try:
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
except Exception:
    with open(file_path, "w", encoding="latin-1") as f:
        f.write(content)

print("index.html patched.")
