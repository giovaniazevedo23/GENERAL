import os

def patch_motorista_html():
    html_file = 'motorista.html'
    if not os.path.exists(html_file):
        print("motorista.html not found!")
        return

    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix the Header
    header_start = content.find('<header')
    header_end = content.find('</header>', header_start) + len('</header>')
    
    new_header = """  <header class="no-print sticky top-0 z-40 bg-slate-900/90 backdrop-blur-md border-b border-slate-800 px-3 lg:px-6 py-2.5 flex flex-col md:flex-row items-stretch md:items-center justify-between gap-3 pt-safe">
      <!-- Top Row on Mobile: Logo -->
      <div class="flex items-center justify-between w-full md:w-auto gap-2">
        <div class="flex items-center gap-2">
          <button onclick="App.toggleMobileDrawer()" class="lg:hidden p-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition-all touch-active" title="Menu Mobile">
            <i data-lucide="menu" class="w-5 h-5"></i>
          </button>
  
          <div class="flex items-center gap-2 cursor-pointer" onclick="App.switchTab('dashboard')">
            <div class="w-8 h-8 sm:w-9 sm:h-9 rounded-xl overflow-hidden shadow-md shadow-blue-900/20 border border-slate-800/80 flex-shrink-0">
              <img src="icons/logo.png" alt="GENERAL Emblem" class="w-full h-full object-cover" />
            </div>
            <div class="flex flex-col">
              <div class="flex items-center gap-1.5">
                <span class="font-extrabold text-white text-sm lg:text-base tracking-wider">GENERAL</span>
              </div>
              <p class="text-[9px] lg:text-[10px] text-slate-400 font-medium whitespace-nowrap hidden sm:block">Motorista de Frotas</p>
            </div>
          </div>
        </div>
        
        <!-- Mobile only top buttons (Help) -->
        <div class="flex items-center gap-2 md:hidden">
          <button onclick="document.getElementById('help-modal').classList.remove('hidden')" class="text-slate-400 hover:text-white transition-all p-2 bg-slate-800 rounded-full" title="Ajuda">
            <i data-lucide="help-circle" class="w-5 h-5"></i>
          </button>
        </div>
      </div>
  
      <!-- Actions: Perfil, Sair, Ajuda -->
      <div class="flex items-center gap-2 overflow-x-auto no-scrollbar w-full md:w-auto pb-1 md:pb-0 justify-end hidden md:flex">
        <button onclick="document.getElementById('help-modal').classList.remove('hidden')" class="flex-shrink-0 flex items-center gap-2 bg-slate-800 hover:bg-slate-700 text-slate-300 px-3 py-2 rounded-xl text-xs font-bold transition-all touch-active">
          <i data-lucide="help-circle" class="w-4 h-4"></i>
          <span class="hidden sm:inline">Ajuda</span>
        </button>

        <button onclick="App.openProfileModal()" class="flex-shrink-0 flex items-center gap-2 bg-slate-800 hover:bg-slate-700 text-slate-300 px-3 py-2 rounded-xl text-xs font-bold transition-all touch-active">
          <i data-lucide="user" class="w-4 h-4 text-blue-400"></i>
          <span class="hidden sm:inline">Perfil</span>
        </button>

        <button onclick="App.logout()" class="flex-shrink-0 flex items-center gap-2 bg-rose-500/10 hover:bg-rose-500/20 border border-rose-500/30 text-rose-400 px-3 py-2 rounded-xl text-xs font-bold transition-all touch-active">
          <i data-lucide="log-out" class="w-4 h-4"></i>
          <span class="hidden sm:inline">Sair</span>
        </button>
      </div>
  </header>"""
    if header_start != -1 and header_end != -1:
        content = content[:header_start] + new_header + content[header_end:]
        print("Updated Header.")

    # 2. Fix the Mobile Drawer
    drawer_start = content.find('<div id="mobile-drawer"')
    drawer_end = content.find('</div>\n    </div>\n  \n    <!-- MODAL DE', drawer_start)
    if drawer_end == -1: # Try another way to find end of drawer
        drawer_end = content.find('<!-- MODAL DE INSTRUÇÕES DE INSTALAÇÃO NO IOS -->')
    
    if drawer_start != -1 and drawer_end != -1:
        new_drawer = """<div id="mobile-drawer" class="fixed inset-y-0 left-0 w-64 bg-slate-900 border-r border-slate-800 z-50 transform -translate-x-full transition-transform duration-300 flex flex-col no-print shadow-2xl">
      <div class="flex items-center justify-between p-4 border-b border-slate-800">
        <div class="flex items-center gap-2">
          <div class="w-8 h-8 rounded-xl bg-blue-600 flex items-center justify-center text-white font-bold shadow-md shadow-blue-600/30">
            <i data-lucide="shield-alert" class="w-4 h-4"></i>
          </div>
          <span class="font-bold text-white text-sm tracking-wider">MOTORISTA</span>
        </div>
        <button onclick="App.toggleMobileDrawer()" class="p-2 text-slate-400 hover:text-white bg-slate-800 rounded-lg transition-colors">
          <i data-lucide="x" class="w-4 h-4"></i>
        </button>
      </div>
  
      <div class="flex-1 overflow-y-auto p-4 flex flex-col justify-between">
        <div class="space-y-6">
          <!-- Menu do Motorista -->
          <div>
            <span class="text-[10px] font-bold text-slate-500 uppercase tracking-wider block mb-2 px-2">Menu Principal</span>
            <nav class="space-y-1">
              <button data-tab="dashboard" onclick="App.switchTab('dashboard'); App.toggleMobileDrawer();" class="nav-button w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-bold text-slate-400 hover:bg-slate-800 transition-all">
                <i data-lucide="siren" class="w-4 h-4 text-rose-500"></i>
                Painel de Perigo
              </button>
              <button data-tab="saved-plans" onclick="App.switchTab('saved-plans'); App.toggleMobileDrawer();" class="nav-button w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-bold text-slate-400 hover:bg-slate-800 transition-all">
                <i data-lucide="clipboard-list" class="w-4 h-4 text-emerald-400"></i>
                Planos da Empresa
              </button>
              <button data-tab="indicators" onclick="App.switchTab('indicators'); App.toggleMobileDrawer();" class="nav-button w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-bold text-slate-400 hover:bg-slate-800 transition-all">
                <i data-lucide="user-check" class="w-4 h-4 text-indigo-400"></i>
                Meu Desempenho
              </button>
              <button data-tab="wizard" onclick="App.switchTab('wizard'); App.toggleMobileDrawer();" class="nav-button w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-bold text-slate-400 hover:bg-slate-800 transition-all">
                <i data-lucide="phone-call" class="w-4 h-4 text-rose-400"></i>
                Emergência Rápida
              </button>
              <button data-tab="history" onclick="App.switchTab('history'); App.toggleMobileDrawer();" class="nav-button w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-bold text-slate-400 hover:bg-slate-800 transition-all">
                <i data-lucide="star" class="w-4 h-4 text-amber-400"></i>
                Avaliar Rota
              </button>
            </nav>
          </div>
        </div>
  
        <!-- Rodapé do Menu Mobile -->
        <div class="flex flex-col gap-2 pt-2 border-t border-slate-800 mt-2">
          <button onclick="App.openProfileModal(); App.toggleMobileDrawer();" class="w-full bg-slate-800 hover:bg-slate-700 text-slate-300 font-bold py-2.5 rounded-xl text-xs transition-all flex items-center justify-center gap-2">
            <i data-lucide="user" class="w-4 h-4 text-blue-400"></i>
            Perfil do Motorista
          </button>
          <button onclick="App.logout(); App.toggleMobileDrawer();" class="w-full bg-rose-500/10 hover:bg-rose-500/20 border border-rose-500/30 text-rose-300 font-bold py-2.5 rounded-xl text-xs transition-all flex items-center justify-center gap-2">
            <i data-lucide="log-out" class="w-4 h-4 text-rose-400"></i>
            Sair do Sistema
          </button>
        </div>
      </div>
    </div>
    """
        # Find the end of the mobile drawer wrapper
        drawer_wrapper_end = content.find('</div>', drawer_start)
        # Actually I can just replace everything up to the iOS install modal
        ios_modal_start = content.find('<!-- MODAL DE INSTRUÇÕES DE INSTALAÇÃO NO IOS -->')
        if ios_modal_start != -1:
            # Let's find the drawer overlay which wraps the mobile drawer, wait, there's no overlay, it's just the drawer itself.
            content = content[:drawer_start] + new_drawer + "\n\n  " + content[ios_modal_start:]
            print("Updated Mobile Drawer.")

    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)
        print("Done!")

if __name__ == "__main__":
    patch_motorista_html()
