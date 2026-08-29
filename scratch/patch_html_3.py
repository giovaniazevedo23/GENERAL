import sys
import re

file_path = "index.html"
try:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
except UnicodeDecodeError:
    with open(file_path, "r", encoding="latin-1") as f:
        content = f.read()

# 1. Parecer - Remove oninput and add submit button
parecer_re = re.compile(r'(<textarea id="docs-parecer"[^>]*?) oninput="App\.saveParecer\(\)"([^>]*>.*?</textarea>)', re.DOTALL)
content = parecer_re.sub(r'\1\2', content)

# Insert the button right after the textarea.
parecer_textarea = re.compile(r'(<textarea id="docs-parecer"[^>]*>.*?</textarea>)', re.DOTALL)
submit_button = r'''\1
            <button onclick="App.submitParecer()" class="w-full mt-4 bg-blue-600 hover:bg-blue-500 text-white font-bold py-3 rounded-xl transition-all shadow-lg flex items-center justify-center gap-2 text-sm">
              <i data-lucide="send" class="w-4 h-4"></i> Enviar Informação (Salvar Parecer)
            </button>'''
content = parecer_textarea.sub(submit_button, content)


# 2. Ishikawa Save Button
ishikawa_save_re = re.compile(r'onclick="App\.showToast\(\'Investigação de Causa Raiz salva com sucesso!\', \'success\'\)"')
content = ishikawa_save_re.sub('onclick="App.saveIshikawa()"', content)


# 3. Add Catálogo de Cargas View
cargo_catalog_view = '''
      <!-- ============================================== -->
      <!-- VIEW: CATÁLOGO DE CARGAS E RISCOS -->
      <!-- ============================================== -->
      <div id="view-cargo-catalog" class="tab-view hidden space-y-6">
        <div class="bg-gradient-to-r from-amber-950 via-slate-900 to-yellow-950 border border-amber-800/40 p-6 rounded-2xl flex items-center justify-between">
          <div>
            <h2 class="text-xl font-black text-white flex items-center gap-2">
              <i data-lucide="package" class="w-6 h-6 text-amber-400"></i>
              Catálogo de Cargas
            </h2>
            <p class="text-xs text-slate-400 mt-1">
              Gerencie os tipos de cargas e suas notas de risco inerentes para as simulações de viagem.
            </p>
          </div>
          <button onclick="App.openAddCargoModal()" class="bg-amber-600 hover:bg-amber-500 text-white font-bold py-2 px-4 rounded-xl transition-all shadow-lg flex items-center gap-2 text-xs">
            <i data-lucide="plus" class="w-4 h-4"></i> Nova Carga
          </button>
        </div>

        <div class="grid grid-cols-1 gap-4" id="cargo-catalog-list">
          <!-- Populated by JS -->
        </div>
      </div>
'''

view_reverse_logistics_marker = '<div id="view-reverse-logistics"'
idx_rev = content.find(view_reverse_logistics_marker)
if idx_rev != -1:
    content = content[:idx_rev] + cargo_catalog_view + "\n" + content[idx_rev:]

# Add "Catálogo de Cargas" to sidebar menu (before Logística Reversa)
sidebar_rev_btn_re = re.compile(r'(<button data-tab="reverse-logistics"[^>]+>.*?Logística Reversa\s*</button>)', re.DOTALL)
cargo_sidebar_btn = '''
          <button data-tab="cargo-catalog" onclick="App.switchTab('cargo-catalog')" class="nav-button w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-bold text-slate-400 hover:bg-slate-800 hover:text-slate-200 transition-all">
            <i data-lucide="package" class="w-4 h-4 text-amber-400"></i>
            Catálogo de Cargas
          </button>
'''
match_s = sidebar_rev_btn_re.search(content)
if match_s:
    content = content[:match_s.start()] + cargo_sidebar_btn + content[match_s.start():]

# Add to drawer menu
drawer_rev_btn_re = re.compile(r'(<button data-tab="reverse-logistics"[^>]+>.*?Logística Reversa\s*</button>)', re.DOTALL)
matches = list(drawer_rev_btn_re.finditer(content))
if len(matches) > 1:
    match_d = matches[-1]
    cargo_drawer_btn = '''
              <button data-tab="cargo-catalog" onclick="App.switchTab('cargo-catalog'); App.toggleMobileDrawer();" class="nav-button w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-bold text-slate-400 hover:bg-slate-800 transition-all">
                <i data-lucide="package" class="w-4 h-4 text-amber-400"></i>
                Catálogo de Cargas
              </button>
'''
    content = content[:match_d.start()] + cargo_drawer_btn + content[match_d.start():]

# 4. Modal for adding Cargo
modal_html = '''
  <!-- MODAL: NOVA CARGA -->
  <div id="add-cargo-modal" class="hidden fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
    <div class="bg-slate-900 border border-slate-800 w-full max-w-md rounded-2xl shadow-2xl flex flex-col overflow-hidden">
      <div class="flex items-center justify-between p-5 border-b border-slate-800 bg-slate-800/50">
        <h3 class="font-bold text-white flex items-center gap-2"><i data-lucide="package-plus" class="w-5 h-5 text-amber-400"></i> Cadastrar Carga</h3>
        <button onclick="document.getElementById('add-cargo-modal').classList.add('hidden')" class="text-slate-400 hover:text-white transition-colors">
          <i data-lucide="x" class="w-5 h-5"></i>
        </button>
      </div>
      <div class="p-6 space-y-4">
        <div>
          <label class="block text-xs font-bold text-slate-400 mb-1">Nome/Descrição da Carga</label>
          <input type="text" id="new-cargo-name" class="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-xs text-white outline-none focus:border-amber-500" placeholder="Ex: Soja a Granel">
        </div>
        <div>
          <label class="block text-xs font-bold text-slate-400 mb-1">Categoria</label>
          <select id="new-cargo-category" class="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-xs text-white outline-none focus:border-amber-500" onchange="App.updateCargoRiskEstimate()">
            <option value="Cargas Gerais">Cargas Gerais (Caixas, Fardos, Pallets)</option>
            <option value="Carga Frigorífica">Carga Frigorífica (Alimentos, Remédios)</option>
            <option value="Cargas Vivas">Cargas Vivas (Animais)</option>
            <option value="Carga Indivisível">Carga Indivisível (Máquinas Grandes)</option>
            <option value="Carga a Granéis">Carga a Granéis (Sólidos, Líquidos)</option>
          </select>
        </div>
        <div>
          <label class="block text-xs font-bold text-slate-400 mb-1">Nota de Risco (0-100)</label>
          <input type="number" id="new-cargo-risk" class="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-xs text-white outline-none focus:border-amber-500 font-mono" value="20">
          <span class="text-[10px] text-slate-500 mt-1 block">A nota é sugerida baseada na categoria, mas pode ser ajustada manualmente.</span>
        </div>
        <button onclick="App.saveNewCargo()" class="w-full bg-amber-600 hover:bg-amber-500 text-white font-bold py-3 rounded-xl transition-all shadow-lg flex items-center justify-center gap-2 mt-4 text-sm">
          Salvar no Catálogo
        </button>
      </div>
    </div>
  </div>
'''

modals_marker = '<!-- MODAL DE CENTRAL DE AJUDA -->'
idx_modal = content.find(modals_marker)
if idx_modal != -1:
    content = content[:idx_modal] + modal_html + "\n" + content[idx_modal:]


try:
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
except Exception:
    with open(file_path, "w", encoding="latin-1") as f:
        f.write(content)

print("index.html patched again for phase 2.")
