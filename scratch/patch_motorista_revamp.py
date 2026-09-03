import re
import os

def refactor_motorista_html():
    html_file = 'motorista.html'
    if not os.path.exists(html_file):
        print("motorista.html not found!")
        return

    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace the entire <aside> menu
    aside_start = content.find('<aside')
    aside_end = content.find('</aside>', aside_start) + len('</aside>')
    
    if aside_start != -1 and aside_end != -1:
        new_aside = """    <aside class="no-print hidden md:flex flex-col w-64 bg-slate-900/60 border-r border-slate-800/80 p-4 space-y-6 flex-shrink-0">
      
      <!-- Logo -->
      <div class="flex items-center justify-between mt-2 mb-4">
        <div class="flex items-center gap-2">
          <div class="w-8 h-8 rounded-xl bg-rose-600 flex items-center justify-center text-white font-bold">
            <i data-lucide="shield-alert" class="w-5 h-5"></i>
          </div>
          <div>
            <h1 class="text-sm font-black text-white leading-none tracking-wider">MOTORISTA</h1>
            <p class="text-[9px] text-slate-400 font-bold tracking-widest uppercase">Segurança Ativa</p>
          </div>
        </div>
      </div>

      <!-- Menu Simplificado do Motorista -->
      <div>
        <nav class="space-y-2">
          <button data-tab="dashboard" onclick="App.switchTab('dashboard')" class="nav-button w-full flex items-center gap-3 px-3 py-3 rounded-xl text-xs font-bold transition-all bg-rose-600 text-white shadow-md shadow-rose-600/20">
            <i data-lucide="siren" class="w-4 h-4"></i>
            Painel de Perigo
          </button>
          
          <button data-tab="saved-plans" onclick="App.switchTab('saved-plans')" class="nav-button w-full flex items-center gap-3 px-3 py-3 rounded-xl text-xs font-bold text-slate-400 hover:bg-slate-800 hover:text-slate-200 transition-all">
            <i data-lucide="clipboard-list" class="w-4 h-4 text-emerald-400"></i>
            Planos da Empresa
          </button>
          
          <button data-tab="indicators" onclick="App.switchTab('indicators')" class="nav-button w-full flex items-center gap-3 px-3 py-3 rounded-xl text-xs font-bold text-slate-400 hover:bg-slate-800 hover:text-slate-200 transition-all">
            <i data-lucide="user-check" class="w-4 h-4 text-indigo-400"></i>
            Meu Desempenho
          </button>
          
          <button data-tab="wizard" onclick="App.switchTab('wizard')" class="nav-button w-full flex items-center gap-3 px-3 py-3 rounded-xl text-xs font-bold text-slate-400 hover:bg-slate-800 hover:text-slate-200 transition-all">
            <i data-lucide="phone-call" class="w-4 h-4 text-rose-400"></i>
            Emergência Rápida
          </button>

          <button data-tab="history" onclick="App.switchTab('history')" class="nav-button w-full flex items-center gap-3 px-3 py-3 rounded-xl text-xs font-bold text-slate-400 hover:bg-slate-800 hover:text-slate-200 transition-all">
            <i data-lucide="star" class="w-4 h-4 text-amber-400"></i>
            Avaliar Rota
          </button>
        </nav>
      </div>

    </aside>"""
        content = content[:aside_start] + new_aside + content[aside_end:]
        print("Updated Aside Menu.")

    # 2. Modify Mobile Menu to match
    mobile_nav_start = content.find('<nav class="md:hidden')
    mobile_nav_end = content.find('</nav>', mobile_nav_start) + len('</nav>')
    if mobile_nav_start != -1 and mobile_nav_end != -1:
        new_mobile_nav = """    <nav class="md:hidden no-print fixed bottom-0 w-full bg-slate-900 border-t border-slate-800 z-40 pb-safe">
      <div class="flex justify-between items-center px-6 py-2 max-w-md mx-auto">
        <button data-tab="dashboard" onclick="App.switchTab('dashboard')" class="mobile-nav-btn active flex flex-col items-center p-2 text-slate-400">
          <i data-lucide="siren" class="w-5 h-5 mb-1 text-rose-500"></i>
          <span class="text-[10px] font-bold text-rose-500">Perigo</span>
        </button>
        <button data-tab="saved-plans" onclick="App.switchTab('saved-plans')" class="mobile-nav-btn flex flex-col items-center p-2 text-slate-400">
          <i data-lucide="clipboard-list" class="w-5 h-5 mb-1"></i>
          <span class="text-[10px] font-bold">Planos</span>
        </button>
        <button data-tab="wizard" onclick="App.switchTab('wizard')" class="mobile-nav-btn flex flex-col items-center p-2 text-slate-400">
          <i data-lucide="phone-call" class="w-5 h-5 mb-1 text-rose-400"></i>
          <span class="text-[10px] font-bold">SOS</span>
        </button>
        <button data-tab="history" onclick="App.switchTab('history')" class="mobile-nav-btn flex flex-col items-center p-2 text-slate-400">
          <i data-lucide="star" class="w-5 h-5 mb-1"></i>
          <span class="text-[10px] font-bold">Avaliar</span>
        </button>
      </div>
    </nav>"""
        content = content[:mobile_nav_start] + new_mobile_nav + content[mobile_nav_end:]
        print("Updated Mobile Nav.")
        
    # 3. Add the Danger Panel to Dashboard
    dashboard_div_start = content.find('<div id="view-dashboard"')
    if dashboard_div_start != -1:
        # Replace up to the end of the dashboard view
        next_view = content.find('<!-- ============================================== -->', dashboard_div_start + 30)
        
        danger_ui = """<div id="view-dashboard" class="tab-view block space-y-6">
        <!-- MOTORISTA DANGER UI -->
        <div class="flex flex-col items-center justify-center min-h-[70vh] text-center w-full max-w-2xl mx-auto space-y-8 px-4">
            <div>
                <h2 class="text-3xl font-black text-white mb-2">Painel de Resgate</h2>
                <p class="text-slate-400">Em caso de acidente, assalto ou perigo iminente, pressione o botão abaixo. Sua localização exata será enviada para a central de emergência.</p>
            </div>
            
            <button id="btn-danger-motorista" onclick="App.acionarPerigo()" class="w-64 h-64 md:w-80 md:h-80 rounded-full bg-rose-600 hover:bg-rose-500 shadow-[0_0_80px_rgba(225,29,72,0.6)] flex items-center justify-center flex-col gap-4 border-[12px] border-rose-900/50 transition-all hover:scale-105 active:scale-95 group">
                <i data-lucide="siren" class="w-24 h-24 text-white animate-pulse"></i>
                <span class="text-4xl font-black text-white tracking-widest uppercase">PERIGO</span>
            </button>
            
            <div id="danger-status-msg" class="hidden text-emerald-400 font-bold bg-emerald-900/30 px-6 py-3 rounded-full border border-emerald-500/50 flex items-center gap-2">
                <i data-lucide="check-circle-2" class="w-5 h-5"></i>
                Alerta de Perigo e Localização Enviados!
            </div>
        </div>
        </div>
        
        <!-- ============================================== -->"""
        
        if next_view != -1:
            content = content[:dashboard_div_start] + danger_ui + content[next_view:]
            print("Updated Dashboard with Danger Button.")

    # 4. Overhaul Golden Hour (wizard) Tab
    wizard_start = content.find('<div id="view-wizard"')
    if wizard_start != -1:
        wizard_end = content.find('<!-- ============================================== -->', wizard_start + 30)
        new_wizard = """<div id="view-wizard" class="tab-view hidden space-y-6">
          <div class="bg-slate-900 border border-slate-800 p-6 rounded-2xl mb-6">
            <h2 class="text-xl font-black text-white flex items-center gap-2 mb-2">
              <i data-lucide="phone-call" class="w-6 h-6 text-rose-500"></i> Ligações Rápidas de Emergência
            </h2>
            <p class="text-sm text-slate-400">Toque nos botões abaixo para acionar ajuda imediatamente. Não hesite em ligar se estiver em perigo.</p>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
             <a href="tel:192" class="flex items-center gap-4 bg-rose-600/20 border border-rose-500/50 p-6 rounded-2xl hover:bg-rose-600/30 transition-all">
                <div class="w-16 h-16 rounded-full bg-rose-600 flex items-center justify-center shrink-0 shadow-lg shadow-rose-600/50">
                    <i data-lucide="ambulance" class="w-8 h-8 text-white"></i>
                </div>
                <div>
                    <h3 class="text-xl font-black text-white">SAMU (Resgate)</h3>
                    <p class="text-rose-200">Ligue 192 para emergências médicas urgentes.</p>
                </div>
             </a>
             
             <a href="tel:190" class="flex items-center gap-4 bg-blue-600/20 border border-blue-500/50 p-6 rounded-2xl hover:bg-blue-600/30 transition-all">
                <div class="w-16 h-16 rounded-full bg-blue-600 flex items-center justify-center shrink-0 shadow-lg shadow-blue-600/50">
                    <i data-lucide="shield-alert" class="w-8 h-8 text-white"></i>
                </div>
                <div>
                    <h3 class="text-xl font-black text-white">Polícia Militar</h3>
                    <p class="text-blue-200">Ligue 190 para assaltos ou riscos de segurança.</p>
                </div>
             </a>
             
             <a href="tel:193" class="flex items-center gap-4 bg-orange-600/20 border border-orange-500/50 p-6 rounded-2xl hover:bg-orange-600/30 transition-all text-left">
                <div class="w-16 h-16 rounded-full bg-orange-600 flex items-center justify-center shrink-0 shadow-lg shadow-orange-600/50">
                    <i data-lucide="flame" class="w-8 h-8 text-white"></i>
                </div>
                <div>
                    <h3 class="text-xl font-black text-white">Bombeiros</h3>
                    <p class="text-orange-200">Ligue 193 para incêndios ou presos nas ferragens.</p>
                </div>
             </a>
             
             <button onclick="App.showToast('Ligando para a Central de Comando...')" class="flex items-center gap-4 bg-emerald-600/20 border border-emerald-500/50 p-6 rounded-2xl hover:bg-emerald-600/30 transition-all text-left">
                <div class="w-16 h-16 rounded-full bg-emerald-600 flex items-center justify-center shrink-0 shadow-lg shadow-emerald-600/50">
                    <i data-lucide="building-2" class="w-8 h-8 text-white"></i>
                </div>
                <div>
                    <h3 class="text-xl font-black text-white">Central (Gestor)</h3>
                    <p class="text-emerald-200">Avisar a sua base de operações logísticas.</p>
                </div>
             </button>
             
             <button onclick="App.showToast('Acionando Seguradora...')" class="md:col-span-2 flex items-center gap-4 bg-purple-600/20 border border-purple-500/50 p-6 rounded-2xl hover:bg-purple-600/30 transition-all text-left">
                <div class="w-16 h-16 rounded-full bg-purple-600 flex items-center justify-center shrink-0 shadow-lg shadow-purple-600/50">
                    <i data-lucide="shield-check" class="w-8 h-8 text-white"></i>
                </div>
                <div>
                    <h3 class="text-xl font-black text-white">Acionar Seguradora</h3>
                    <p class="text-purple-200">Informar sinistro ou danos à carga.</p>
                </div>
             </button>
          </div>
        </div>
        
        <!-- ============================================== -->"""
        if wizard_end != -1:
            content = content[:wizard_start] + new_wizard + content[wizard_end:]
            print("Updated Golden Hour UI.")

    # 5. Full Screen Danger Overlay (Before body end)
    overlay = """
    <!-- DANGER RED FLASHING OVERLAY -->
    <div id="danger-overlay" class="hidden fixed inset-0 z-[9999] bg-rose-600 flex flex-col items-center justify-center p-6 text-center overflow-hidden">
        <div class="absolute inset-0 bg-black/20 animate-pulse-fast"></div>
        <div class="relative z-10 flex flex-col items-center">
            <i data-lucide="siren" class="w-32 h-32 text-white mb-6 animate-bounce"></i>
            <h1 class="text-4xl md:text-6xl font-black text-white mb-4 uppercase tracking-widest text-shadow-lg">ALERTA ENVIADO!</h1>
            <p class="text-xl text-white font-bold max-w-xl mx-auto mb-10 drop-shadow-md">Mantenha a calma e afaste-se do perigo, se possível. Sua localização exata (GPS) foi enviada para o Gestor e o resgate já foi notificado.</p>
            
            <div class="flex flex-col gap-4 w-full max-w-md">
                <a href="tel:190" class="w-full bg-white text-rose-700 font-black py-4 rounded-2xl text-xl hover:bg-slate-100 transition-all shadow-2xl flex items-center justify-center gap-3">
                    <i data-lucide="phone" class="w-6 h-6"></i> LIGAR 190 (Polícia)
                </a>
                <button onclick="document.getElementById('danger-overlay').classList.add('hidden')" class="w-full bg-rose-800/80 text-rose-200 font-bold py-4 rounded-2xl text-sm hover:bg-rose-900 transition-all border border-rose-400 mt-4">
                    Esconder Painel de Alerta (O Resgate Continua)
                </button>
            </div>
        </div>
    </div>
    """
    if "danger-overlay" not in content:
        body_end = content.find('</body>')
        content = content[:body_end] + overlay + "\n" + content[body_end:]
        print("Added Danger Overlay.")

    # 6. Add CSS Animation Pulse Fast (if not present)
    style_end = content.find('</style>')
    if style_end != -1 and 'animate-pulse-fast' not in content:
        extra_css = """
        .animate-pulse-fast { animation: pulse-fast 0.8s cubic-bezier(0.4, 0, 0.6, 1) infinite; }
        @keyframes pulse-fast { 0%, 100% { opacity: 1; } 50% { opacity: .5; } }
        .text-shadow-lg { text-shadow: 0 4px 10px rgba(0,0,0,0.5); }
        """
        content = content[:style_end] + extra_css + content[style_end:]

    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)
        print("motorista.html updated successfully!")


def patch_app_motorista_js():
    js_file = 'js/app_motorista.js'
    if not os.path.exists(js_file):
        print(js_file + " not found!")
        return

    with open(js_file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Add acionarPerigo function
    danger_func = """
  async acionarPerigo() {
    this.showToast("Obtendo localização GPS...", "warning");
    const btn = document.getElementById('btn-danger-motorista');
    if (btn) btn.classList.add('opacity-50', 'cursor-not-allowed');
    
    // Mostra o painel imediatamente para tranquilizar, a gravação vai em background
    const overlay = document.getElementById('danger-overlay');
    if (overlay) overlay.classList.remove('hidden');
    
    // Função auxiliar para gravar no Firebase
    const saveToFirebase = async (lat, lng, precisao) => {
        try {
            if (window.db) {
                const incidentData = {
                    id: 'SOS-' + Date.now().toString().slice(-6),
                    type: 'ALERTA_MOTORISTA',
                    status: 'CRÍTICO',
                    date: new Date().toISOString(),
                    location: `GPS: ${lat.toFixed(6)}, ${lng.toFixed(6)}`,
                    latitude: lat,
                    longitude: lng,
                    accuracy: precisao,
                    driverName: appState.currentUser ? appState.currentUser.name : 'Motorista Desconhecido',
                    companyCnpj: appState.currentUser ? appState.currentUser.companyCnpj : '',
                    description: '🚨 PÂNICO ACIONADO PELO MOTORISTA 🚨',
                    createdAt: firebase.firestore.FieldValue.serverTimestamp()
                };
                
                await window.db.collection('incidents').add(incidentData);
                const msg = document.getElementById('danger-status-msg');
                if (msg) msg.classList.remove('hidden');
            }
        } catch (err) {
            console.error("Erro ao enviar pânico:", err);
            this.showToast("Erro de conexão ao enviar alerta! Tente ligar 190.", "error");
        } finally {
            if (btn) btn.classList.remove('opacity-50', 'cursor-not-allowed');
        }
    };

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                saveToFirebase(position.coords.latitude, position.coords.longitude, position.coords.accuracy);
            },
            (error) => {
                console.error("Geolocalização Falhou:", error);
                this.showToast("Localização negada/indisponível. Enviando alerta sem GPS exato.", "error");
                // Envia sem coordenadas exatas, mas envia o alerta!
                saveToFirebase(0, 0, 0);
            },
            { enableHighAccuracy: true, timeout: 15000, maximumAge: 0 }
        );
    } else {
        // Envia alerta mesmo se não suportar
        saveToFirebase(0, 0, 0);
    }
  },
"""
    if "acionarPerigo()" not in content:
        login_idx = content.find('login() {')
        if login_idx != -1:
            content = content[:login_idx] + danger_func + content[login_idx:]
            print("Added acionarPerigo to app_motorista.js")
            
    with open(js_file, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    refactor_motorista_html()
    patch_app_motorista_js()
    print("Done!")
