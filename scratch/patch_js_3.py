import re

def patch_app_motorista_js():
    with open('../js/app_motorista.js', 'r', encoding='utf-8', errors='ignore') as f:
        js = f.read()

    # Add Shift Tracking Logic
    shift_logic = """
  startShift() {
      if (appState.shiftActive) {
          this.showToast('Sua jornada já está ativa!');
          return;
      }
      appState.shiftActive = true;
      appState.shiftStartTime = new Date().getTime();
      localStorage.setItem('general_shift_active', 'true');
      localStorage.setItem('general_shift_start', appState.shiftStartTime);
      this.showToast('Jornada iniciada com sucesso. Dirija com cuidado!');
      this.updateShiftUI();
  },

  endShift() {
      if (!appState.shiftActive) return;
      appState.shiftActive = false;
      appState.shiftStartTime = null;
      localStorage.removeItem('general_shift_active');
      localStorage.removeItem('general_shift_start');
      this.showToast('Jornada encerrada. Bom descanso!');
      this.updateShiftUI();
  },

  checkShiftLimit() {
      if (!appState.shiftActive) return false;
      const now = new Date().getTime();
      const diffHours = (now - appState.shiftStartTime) / (1000 * 60 * 60);
      
      // Limite militar de 12h
      if (diffHours >= 12) {
          this.showToast('ALERTA: Tempo limite de jornada (12h) excedido. Bloqueio preventivo ativado.');
          return true; // Bloqueado
      } else if (diffHours >= 11) {
          this.showToast('AVISO: Faltam menos de 1h para o limite da jornada legal.');
      }
      return false; // OK
  },

  updateShiftUI() {
      const btnStart = document.getElementById('btn-start-shift');
      const btnEnd = document.getElementById('btn-end-shift');
      const shiftStatus = document.getElementById('shift-status');
      
      if (appState.shiftActive) {
          if (btnStart) btnStart.classList.add('hidden');
          if (btnEnd) btnEnd.classList.remove('hidden');
          if (shiftStatus) {
              shiftStatus.textContent = 'Jornada Ativa (Em Serviço)';
              shiftStatus.className = 'text-[10px] font-bold text-emerald-400 mt-1 uppercase tracking-wider block';
          }
      } else {
          if (btnStart) btnStart.classList.remove('hidden');
          if (btnEnd) btnEnd.classList.add('hidden');
          if (shiftStatus) {
              shiftStatus.textContent = 'Fora de Serviço';
              shiftStatus.className = 'text-[10px] font-bold text-slate-400 mt-1 uppercase tracking-wider block';
          }
      }
  },
"""
    if 'startShift()' not in js:
        js = js.replace('methods: {', 'methods: {\n' + shift_logic)

    # Inject updateShiftUI into init
    if 'this.updateShiftUI();' not in js:
        js = js.replace('this.bindEvents();', 'this.bindEvents();\n    this.updateShiftUI();')

    # Load shift state in checkAuth
    if 'appState.shiftActive = ' not in js:
        js = js.replace('appState.currentUser = user;', "appState.currentUser = user;\n      appState.shiftActive = localStorage.getItem('general_shift_active') === 'true';\n      appState.shiftStartTime = localStorage.getItem('general_shift_start') ? parseInt(localStorage.getItem('general_shift_start')) : null;")
        
    with open('../js/app_motorista.js', 'w', encoding='utf-8') as f:
        f.write(js)
    
    print("app_motorista.js patched with shift tracking.")

def patch_motorista_html():
    with open('../motorista.html', 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()

    # Add Journey Control Widget in Dashboard
    journey_html = """
        <!-- CONTROLE DE JORNADA MILITAR -->
        <div class="bg-slate-900 border border-slate-800 p-5 rounded-2xl relative overflow-hidden mb-6 mt-4">
          <div class="absolute top-0 right-0 w-32 h-32 bg-blue-500/5 rounded-bl-full pointer-events-none"></div>
          <div class="flex items-center justify-between mb-4">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 rounded-xl bg-blue-500/10 flex items-center justify-center border border-blue-500/20">
                <i data-lucide="clock" class="w-5 h-5 text-blue-400"></i>
              </div>
              <div>
                <h3 class="text-sm font-black text-white uppercase tracking-wider">Controle de Jornada</h3>
                <span id="shift-status" class="text-[10px] font-bold text-slate-400 mt-1 uppercase tracking-wider block">Fora de Serviço</span>
              </div>
            </div>
          </div>
          
          <button id="btn-start-shift" onclick="App.startShift()" class="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-3 rounded-xl transition-all shadow-lg shadow-blue-500/20 flex items-center justify-center gap-2">
            <i data-lucide="play-circle" class="w-5 h-5"></i> Iniciar Expediente
          </button>
          
          <button id="btn-end-shift" onclick="App.endShift()" class="w-full hidden bg-rose-600 hover:bg-rose-500 text-white font-bold py-3 rounded-xl transition-all shadow-lg shadow-rose-500/20 flex items-center justify-center gap-2">
            <i data-lucide="stop-circle" class="w-5 h-5"></i> Encerrar Jornada (Descanso)
          </button>
        </div>
    """
    
    if 'CONTROLE DE JORNADA MILITAR' not in html:
        # Insert after "Painel de Ações Rápidas" or at the top of view-dashboard
        idx = html.find('<div id="view-dashboard"')
        if idx != -1:
            idx = html.find('>', idx) + 1
            html = html[:idx] + journey_html + html[idx:]

    with open('../motorista.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print("motorista.html patched with journey control.")

if __name__ == '__main__':
    patch_app_motorista_js()
    patch_motorista_html()
