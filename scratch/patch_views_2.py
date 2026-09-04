import re

def patch_motorista_html():
    with open('../motorista.html', 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()

    # 1. Add view-profile section
    profile_html = """
    <!-- VIEW: PERFIL E PATENTE -->
    <div id="view-profile" class="tab-view hidden space-y-6">
      <h2 class="text-xl font-black text-white flex items-center gap-2">
        <i data-lucide="award" class="w-6 h-6 text-amber-500"></i>
        Meu Perfil & Currículo de Honra
      </h2>
      <p class="text-xs text-slate-400 mt-1">Sua patente e histórico militar de excelência operacional.</p>
      
      <!-- Patente Card -->
      <div class="bg-slate-900 border border-slate-800 p-5 rounded-2xl flex items-center gap-4 relative overflow-hidden">
        <div class="absolute top-0 right-0 w-32 h-32 bg-amber-500/5 rounded-bl-full pointer-events-none"></div>
        <div class="w-16 h-16 rounded-full bg-slate-800 border-2 border-amber-500 flex items-center justify-center shadow-lg shadow-amber-500/20">
          <i data-lucide="shield" class="w-8 h-8 text-amber-500"></i>
        </div>
        <div>
          <p class="text-[10px] text-slate-400 font-bold uppercase tracking-widest">Patente Atual</p>
          <h3 id="profile-rank" class="text-2xl font-black text-white">Elite</h3>
          <p id="profile-xp" class="text-xs text-amber-400 mt-1">1250 XP acumulados</p>
        </div>
      </div>

      <!-- Stats Grid -->
      <div class="grid grid-cols-2 gap-4">
        <div class="bg-slate-900 border border-slate-800 p-4 rounded-xl text-center">
          <i data-lucide="package-check" class="w-5 h-5 text-emerald-400 mx-auto mb-2"></i>
          <p class="text-2xl font-black text-white" id="stat-deliveries">42</p>
          <p class="text-[9px] text-slate-400 uppercase tracking-widest">Entregas Perfeitas</p>
        </div>
        <div class="bg-slate-900 border border-slate-800 p-4 rounded-xl text-center">
          <i data-lucide="clock" class="w-5 h-5 text-blue-400 mx-auto mb-2"></i>
          <p class="text-2xl font-black text-white" id="stat-hours">120h</p>
          <p class="text-[9px] text-slate-400 uppercase tracking-widest">Jornada na Lei</p>
        </div>
      </div>

      <!-- Currículo de Honra -->
      <div class="bg-slate-900 border border-slate-800 p-5 rounded-2xl">
        <h3 class="text-sm font-bold text-white mb-4 flex items-center gap-2">
          <i data-lucide="medal" class="w-4 h-4 text-amber-500"></i>
          Currículo de Honra
        </h3>
        <div class="space-y-3" id="honor-curriculum-list">
          <div class="flex items-center gap-3 p-3 bg-slate-800/50 rounded-xl border border-slate-700/50">
            <i data-lucide="star" class="w-4 h-4 text-amber-400"></i>
            <div>
              <p class="text-xs font-bold text-slate-200">Conduta Defensiva Exemplar</p>
              <p class="text-[10px] text-slate-400">Reconhecimento do Gestor</p>
            </div>
          </div>
          <div class="flex items-center gap-3 p-3 bg-slate-800/50 rounded-xl border border-slate-700/50">
            <i data-lucide="clock" class="w-4 h-4 text-emerald-400"></i>
            <div>
              <p class="text-xs font-bold text-slate-200">Pontualidade Militar</p>
              <p class="text-[10px] text-slate-400">100% de Horários Cumpridos</p>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- /VIEW: PERFIL E PATENTE -->
    """
    
    if 'id="view-profile"' not in html:
        # Insert before <!-- MODAL: WIZARD / GOLDEN HOUR --> or another view
        idx = html.find('<!-- MODAL:')
        if idx == -1:
            idx = html.find('<!-- BARRA DE NAVEGA')
        if idx != -1:
            html = html[:idx] + profile_html + '\n\n' + html[idx:]

    # 2. Add Profile button to sidebar
    sidebar_btn = """
          <button data-tab="profile" onclick="App.switchTab('profile')" class="nav-button w-full flex items-center gap-3 px-3 py-3 rounded-xl text-xs font-bold text-slate-400 hover:bg-slate-800 hover:text-slate-200 transition-all">
            <i data-lucide="user-check" class="w-4 h-4 text-indigo-400"></i>
            Meu Perfil
          </button>
"""
    if 'data-tab="profile"' not in html:
        # Replace 'Meu Desempenho' which is data-tab="indicators" to avoid duplicates
        # or just add it after indicators
        html = html.replace('<!-- Menu Simplificado do Motorista -->', '<!-- Menu Simplificado do Motorista -->\n' + sidebar_btn)
        
    with open('../motorista.html', 'w', encoding='utf-8') as f:
        f.write(html)
        
    print("HTML patched for view-profile")

if __name__ == '__main__':
    patch_motorista_html()
