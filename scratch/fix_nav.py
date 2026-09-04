import re

def fix_motorista():
    with open('../motorista.html', 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()

    # Find the mobile bottom nav
    start_tag = '<nav class="mobile-bottom-nav'
    end_tag = '</nav>'
    
    start_idx = html.find(start_tag)
    end_idx = html.find(end_tag, start_idx) + len(end_tag)
    
    new_nav = """<nav class="mobile-bottom-nav no-print fixed bottom-0 left-0 right-0 z-40 lg:hidden flex items-center justify-around px-2 py-1.5 pb-safe">
    <button data-tab="dashboard" onclick="App.switchTab('dashboard')" class="nav-button mobile-nav-btn flex-1 flex flex-col items-center justify-center py-1 text-slate-400">
      <i data-lucide="layout-dashboard" class="w-5 h-5"></i>
      <span class="text-[10px] font-medium">Início</span>
    </button>
    <button data-tab="indicators" onclick="App.switchTab('indicators')" class="nav-button mobile-nav-btn flex-1 flex flex-col items-center justify-center py-1 text-slate-400">
      <i data-lucide="bar-chart-2" class="w-5 h-5 text-indigo-400"></i>
      <span class="text-[10px] font-medium">KPIs</span>
    </button>
    <button data-tab="saved-plans" onclick="App.switchTab('saved-plans')" class="nav-button mobile-nav-btn flex-1 flex flex-col items-center justify-center py-1 text-slate-400">
      <i data-lucide="saveAll" class="w-5 h-5 text-emerald-400"></i>
      <span class="text-[10px] font-medium">Salvos</span>
    </button>
    <button data-tab="wizard" onclick="App.switchTab('wizard')" class="nav-button mobile-nav-btn flex-1 flex flex-col items-center justify-center py-1 text-slate-400">
      <i data-lucide="shield-alert" class="w-5 h-5"></i>
      <span class="text-[10px] font-medium">Golden Hour</span>
    </button>
    <button data-tab="feedback" onclick="App.switchTab('feedback')" class="nav-button mobile-nav-btn flex-1 flex flex-col items-center justify-center py-1 text-slate-400">
      <i data-lucide="message-square" class="w-5 h-5 text-amber-400"></i>
      <span class="text-[10px] font-medium">Avaliação</span>
    </button>
  </nav>"""

    html = html[:start_idx] + new_nav + html[end_idx:]

    with open('../motorista.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Fixed motorista.html")

fix_motorista()
