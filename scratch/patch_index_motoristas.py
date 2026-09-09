import re

with open('index.html', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# 1. Add to Desktop Sidebar
desktop_btn = """
          <!-- Motoristas Vinculados -->
          <button data-tab="motoristas" onclick="App.switchTab('motoristas')" class="nav-button w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-bold text-slate-400 hover:text-white hover:bg-slate-800/50 transition-all group">
            <i data-lucide="users" class="w-4 h-4 opacity-50 group-hover:opacity-100 group-[.active]:opacity-100 group-[.active]:text-blue-400 transition-opacity"></i>
            Motoristas
          </button>
"""
if 'data-tab="motoristas"' not in content:
    content = content.replace(
        '<button data-tab="driver-evaluations"',
        desktop_btn + '\n          <button data-tab="driver-evaluations"'
    )

# 2. Add to Mobile Drawer
mobile_btn = """
            <!-- Motoristas Vinculados -->
            <button data-tab="motoristas" onclick="App.switchTab('motoristas'); App.toggleMobileDrawer();" class="nav-button w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-bold text-slate-400 hover:text-white hover:bg-slate-800/50 transition-all group">
              <i data-lucide="users" class="w-4 h-4 opacity-50 group-hover:opacity-100 group-[.active]:text-blue-400 transition-opacity"></i>
              Motoristas
            </button>
"""
# The mobile drawer has the same buttons but with App.toggleMobileDrawer()
# To replace correctly, we look for the mobile driver-evaluations if it exists, or just risk-dashboard
if 'data-tab="motoristas" onclick="App.switchTab(\'motoristas\');' not in content:
    content = content.replace(
        '<button data-tab="driver-evaluations" onclick="App.switchTab(\'driver-evaluations\'); App.toggleMobileDrawer();"',
        mobile_btn + '\n            <button data-tab="driver-evaluations" onclick="App.switchTab(\'driver-evaluations\'); App.toggleMobileDrawer();"'
    )

# 3. Add the Tab Content View
tab_content = """
      <!-- TAB MOTORISTAS VINCULADOS -->
      <div id="tab-motoristas" class="tab-content hidden space-y-6">
        <header class="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900 p-6 rounded-2xl border border-slate-800 shadow-xl relative overflow-hidden">
          <div class="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCI+PHBhdGggZD0iTTAgMGgyMHYyMEgwem0xMCAxMGgxMHYxMEgxMHoiIGZpbGw9IiMzMzMiIGZpbGwtb3BhY2l0eT0iLjA1IiBmaWxsLXJ1bGU9ImV2ZW5vZGQiLz48L3N2Zz4=')] opacity-20 pointer-events-none"></div>
          <div class="relative z-10">
            <h1 class="text-2xl font-black text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-indigo-500 flex items-center gap-3">
              <i data-lucide="users" class="w-8 h-8 text-blue-500"></i>
              Gestão de Motoristas
            </h1>
            <p class="text-slate-400 mt-1">Gerencie os motoristas vinculados e acompanhe sinais vitais em tempo real.</p>
          </div>
          <div class="relative z-10 flex gap-3">
            <button onclick="App.showDriverModal()" class="bg-blue-600 hover:bg-blue-500 text-white px-4 py-2 rounded-xl font-bold transition-colors flex items-center gap-2 text-sm shadow-lg shadow-blue-500/20">
              <i data-lucide="plus" class="w-4 h-4"></i>
              Novo Motorista
            </button>
          </div>
        </header>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <!-- Lista de Motoristas -->
          <div class="lg:col-span-2 space-y-4">
            <h2 class="text-lg font-bold text-slate-200 flex items-center gap-2">
              <i data-lucide="list" class="w-5 h-5 text-blue-400"></i>
              Motoristas Cadastrados
            </h2>
            <div id="drivers-list" class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <!-- Gerado via JS -->
              <div class="p-4 border border-slate-800 rounded-xl text-center text-slate-500 text-sm">Carregando motoristas...</div>
            </div>
          </div>

          <!-- Câmera ao Vivo / Monitoramento -->
          <div class="space-y-4">
            <h2 class="text-lg font-bold text-slate-200 flex items-center gap-2">
              <i data-lucide="video" class="w-5 h-5 text-emerald-400"></i>
              Monitoramento ao Vivo
            </h2>
            <div id="live-monitoring-container" class="bg-slate-950 border border-slate-800 rounded-2xl p-4 relative overflow-hidden hidden">
               <div id="live-vital-alert" class="absolute top-2 left-2 right-2 bg-rose-500/90 text-white text-xs font-bold px-3 py-1.5 rounded-lg flex items-center gap-2 justify-center z-20 hidden animate-pulse">
                  <i data-lucide="alert-triangle" class="w-4 h-4"></i> ALERTA CRÍTICO: SINAIS VITAIS EM QUEDA
               </div>
               
               <div class="relative rounded-xl overflow-hidden bg-black aspect-[3/4] mb-3">
                 <video id="manager-live-video" class="w-full h-full object-cover" autoplay playsinline muted></video>
                 <div id="no-signal-overlay" class="absolute inset-0 flex flex-col items-center justify-center bg-slate-900/80 z-10">
                    <i data-lucide="wifi-off" class="w-8 h-8 text-slate-500 mb-2"></i>
                    <span class="text-xs text-slate-400 font-medium">Sem sinal de vídeo</span>
                 </div>
               </div>

               <div class="space-y-3">
                 <div class="flex items-center justify-between">
                   <div class="flex items-center gap-2">
                     <div class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></div>
                     <span id="live-driver-name" class="text-sm font-bold text-slate-200">Aguardando...</span>
                   </div>
                   <span id="live-route-code" class="text-[10px] font-mono bg-slate-800 px-2 py-1 rounded text-slate-400">---</span>
                 </div>
                 
                 <div class="grid grid-cols-2 gap-2">
                    <div class="bg-slate-900 p-2 rounded-xl border border-slate-800/50 flex flex-col items-center justify-center">
                      <i data-lucide="heart" class="w-4 h-4 text-rose-500 mb-1 animate-pulse"></i>
                      <span id="live-heart-rate" class="text-lg font-black text-white">-- <span class="text-[10px] font-normal text-slate-500">BPM</span></span>
                    </div>
                    <div class="bg-slate-900 p-2 rounded-xl border border-slate-800/50 flex flex-col items-center justify-center text-center">
                      <i data-lucide="map-pin" class="w-4 h-4 text-blue-400 mb-1"></i>
                      <span id="live-location" class="text-[10px] font-medium text-slate-300 line-clamp-2">Aguardando GPS...</span>
                    </div>
                 </div>
               </div>
            </div>
            
            <div id="idle-monitoring-container" class="bg-slate-900 border border-slate-800 border-dashed rounded-2xl p-8 flex flex-col items-center justify-center text-center">
              <i data-lucide="camera-off" class="w-12 h-12 text-slate-700 mb-3"></i>
              <h3 class="text-slate-400 font-bold text-sm">Nenhum stream ativo</h3>
              <p class="text-slate-500 text-xs mt-1">A câmera dos motoristas aparecerá aqui quando eles iniciarem uma rota e ativarem o vídeo.</p>
            </div>

          </div>
        </div>
      </div>
"""

# Insert the tab view right after the dashboard tab or driver-evaluations tab
if 'id="tab-motoristas"' not in content:
    # Find a good place to insert, e.g., right before <!-- MODAIS GLOBAIS -->
    content = content.replace(
        '<!-- MODAIS GLOBAIS -->',
        tab_content + '\n      <!-- MODAIS GLOBAIS -->'
    )

# 4. Add Driver Modal
driver_modal = """
  <!-- Modal de Cadastro de Motorista -->
  <div id="driver-modal" class="fixed inset-0 z-[100] bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4 transition-all duration-300 opacity-0 pointer-events-none">
    <div class="bg-slate-900 w-full max-w-md rounded-2xl border border-slate-800 shadow-2xl overflow-hidden transform scale-95 transition-transform duration-300" id="driver-modal-content">
      <div class="p-4 border-b border-slate-800 flex items-center justify-between bg-slate-950/50">
        <h2 class="text-lg font-bold text-white flex items-center gap-2">
          <i data-lucide="user-plus" class="w-5 h-5 text-blue-400"></i>
          Cadastrar Motorista
        </h2>
        <button onclick="App.hideDriverModal()" class="text-slate-500 hover:text-white transition-colors p-1">
          <i data-lucide="x" class="w-5 h-5"></i>
        </button>
      </div>
      
      <div class="p-5 space-y-4">
        <div>
          <label class="block text-xs font-bold text-slate-400 mb-1 uppercase tracking-wider">Tipo de Motorista</label>
          <div class="grid grid-cols-2 gap-2">
            <button type="button" id="btn-driver-type-vinculado" onclick="App.setDriverType('vinculado')" class="bg-blue-600 text-white text-sm font-bold py-2 rounded-lg border border-blue-500 transition-all">Vinculado</button>
            <button type="button" id="btn-driver-type-autonomo" onclick="App.setDriverType('autonomo')" class="bg-slate-800 text-slate-400 text-sm font-bold py-2 rounded-lg border border-slate-700 transition-all hover:bg-slate-700 hover:text-slate-300">Autônomo</button>
          </div>
        </div>

        <div>
          <label class="block text-xs font-bold text-slate-400 mb-1 uppercase tracking-wider">Nome Completo</label>
          <input type="text" id="driver-name" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:border-blue-500 transition-colors placeholder:text-slate-600" placeholder="Ex: João da Silva">
        </div>
        
        <div>
          <label class="block text-xs font-bold text-slate-400 mb-1 uppercase tracking-wider">CPF</label>
          <input type="text" id="driver-cpf" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:border-blue-500 transition-colors placeholder:text-slate-600 font-mono" placeholder="000.000.000-00">
        </div>
        
        <div>
          <label id="label-driver-cnpj" class="block text-xs font-bold text-slate-400 mb-1 uppercase tracking-wider">CNPJ da Empresa</label>
          <input type="text" id="driver-cnpj" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:border-blue-500 transition-colors placeholder:text-slate-600 font-mono" placeholder="00.000.000/0000-00">
        </div>
      </div>
      
      <div class="p-4 border-t border-slate-800 bg-slate-950/30 flex justify-end gap-3">
        <button type="button" onclick="App.hideDriverModal()" class="px-4 py-2 text-sm font-bold text-slate-400 hover:text-white transition-colors">Cancelar</button>
        <button type="button" onclick="App.saveDriver()" class="px-6 py-2 bg-blue-600 hover:bg-blue-500 text-white text-sm font-bold rounded-xl shadow-lg shadow-blue-500/20 transition-all">Salvar Motorista</button>
      </div>
    </div>
  </div>
"""

if 'id="driver-modal"' not in content:
    content = content.replace(
        '<!-- MODAIS GLOBAIS -->',
        driver_modal + '\n  <!-- MODAIS GLOBAIS -->'
    )

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("index.html patched with Gestão de Motoristas UI successfully.")
