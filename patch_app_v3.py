import re

def patch_app_motorista_js():
    with open('js/app_motorista.js', 'r', encoding='utf-8', errors='ignore') as f:
        js = f.read()

    # 1. Update fetchCompanyByCnpj to be more robust
    new_fetch = """  fetchCompanyByCnpj(cnpj) {
    if (!cnpj || cnpj.length < 14) return;
    if (!window.db) return;
    
    const companyInput = document.getElementById('motorista-company');
    if (companyInput) {
        companyInput.value = 'Buscando empresa...';
        companyInput.disabled = true;
    }
    
    // Normalize CNPJ (only numbers) for comparison as well
    const cleanCnpj = cnpj.replace(/[^0-9]/g, '');
    
    // Try multiple possible ways the user might have saved it in Firebase:
    // 1. field 'cnpj' with exact string
    // 2. field 'CNPJ' with exact string
    // 3. Document ID == cnpj
    // 4. field 'cnpj' == cleanCnpj
    
    Promise.all([
      window.db.collection('companies').where('cnpj', '==', cnpj).get(),
      window.db.collection('companies').where('CNPJ', '==', cnpj).get(),
      window.db.collection('companies').where('cnpj', '==', cleanCnpj).get(),
      window.db.collection('companies').doc(cnpj).get(),
      window.db.collection('companies').doc(cleanCnpj).get()
    ]).then(results => {
        let foundData = null;
        
        if (!results[0].empty) foundData = results[0].docs[0].data();
        else if (!results[1].empty) foundData = results[1].docs[0].data();
        else if (!results[2].empty) foundData = results[2].docs[0].data();
        else if (results[3].exists) foundData = results[3].data();
        else if (results[4].exists) foundData = results[4].data();
        
        if (foundData && (foundData.name || foundData.nome)) {
            if (companyInput) {
                companyInput.value = foundData.name || foundData.nome;
                companyInput.disabled = true; // Block manual edit
                this.showToast('Empresa validada no banco de dados!');
            }
        } else {
            if (companyInput) {
                companyInput.value = '';
                companyInput.disabled = false;
                this.showToast('CNPJ não encontrado. Digite manualmente.');
            }
        }
    }).catch(err => {
        console.error("Erro ao buscar empresa:", err);
        if (companyInput) {
            companyInput.value = '';
            companyInput.disabled = false;
        }
    });
  },"""

    # We need to replace the old fetchCompanyByCnpj.
    # The old one starts at fetchCompanyByCnpj(cnpj) { and ends before login() {
    start_idx = js.find('fetchCompanyByCnpj(cnpj)')
    end_idx = js.find('login() {', start_idx)
    if start_idx != -1 and end_idx != -1:
        js = js[:start_idx] + new_fetch + '\n\n' + js[end_idx:]

    # 2. Update Shift Logic for Stopwatch and 5.5h limit
    # Find startShift, endShift, checkShiftLimit, updateShiftUI
    start_shift_idx = js.find('startShift() {')
    end_shift_ui = js.find('fetchCompanyByCnpj(cnpj)', start_shift_idx)
    
    new_shift = """  startShift() {
      if (appState.shiftActive) {
          this.showToast('Sua jornada já está ativa!');
          return;
      }
      // Check rest limit if recently ended
      const lastRestStart = localStorage.getItem('general_rest_start');
      if (lastRestStart) {
          const restDiff = (new Date().getTime() - parseInt(lastRestStart)) / (1000 * 60);
          if (restDiff < 30) {
             this.showToast(`Descanso incompleto. Faltam ${Math.ceil(30 - restDiff)} minutos de pausa legal obrigatória.`);
             return;
          }
      }
      
      appState.shiftActive = true;
      appState.shiftStartTime = new Date().getTime();
      localStorage.setItem('general_shift_active', 'true');
      localStorage.setItem('general_shift_start', appState.shiftStartTime);
      localStorage.removeItem('general_rest_start');
      this.showToast('Jornada iniciada. Dirija com cuidado!');
      this.updateShiftUI();
      this.startShiftTimer();
  },

  endShift() {
      if (!appState.shiftActive) return;
      appState.shiftActive = false;
      appState.shiftStartTime = null;
      localStorage.removeItem('general_shift_active');
      localStorage.removeItem('general_shift_start');
      
      // Start rest timer
      localStorage.setItem('general_rest_start', new Date().getTime());
      
      this.showToast('Jornada pausada/encerrada. Descanso obrigatório de 30 min iniciado.');
      this.updateShiftUI();
      if (this.shiftInterval) clearInterval(this.shiftInterval);
  },

  checkShiftLimit() {
      if (!appState.shiftActive) return false;
      const now = new Date().getTime();
      const diffHours = (now - appState.shiftStartTime) / (1000 * 60 * 60);
      
      if (diffHours >= 5.5) {
          this.showToast('ALERTA MILITAR: Limite de 5h30m ininterruptas atingido. Pausa obrigatória de 30 min necessária.');
          return true; // Bloqueado
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
              shiftStatus.className = 'text-2xl font-black text-emerald-400 mt-1 uppercase tracking-widest block font-mono';
          }
          this.startShiftTimer();
      } else {
          if (btnStart) btnStart.classList.remove('hidden');
          if (btnEnd) btnEnd.classList.add('hidden');
          if (shiftStatus) {
              shiftStatus.textContent = 'Fora de Serviço';
              shiftStatus.className = 'text-[10px] font-bold text-slate-400 mt-1 uppercase tracking-wider block';
          }
          if (this.shiftInterval) clearInterval(this.shiftInterval);
      }
  },

  startShiftTimer() {
      if (this.shiftInterval) clearInterval(this.shiftInterval);
      if (!appState.shiftActive) return;
      
      const updateTimer = () => {
          const shiftStatus = document.getElementById('shift-status');
          if (!shiftStatus || !appState.shiftActive) return;
          
          const now = new Date().getTime();
          const diff = now - appState.shiftStartTime;
          
          const hours = Math.floor(diff / (1000 * 60 * 60));
          const mins = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
          const secs = Math.floor((diff % (1000 * 60)) / 1000);
          
          const formatted = `${String(hours).padStart(2, '0')}:${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
          shiftStatus.textContent = formatted;
          
          if (diff / (1000 * 60 * 60) >= 5.5) {
             shiftStatus.classList.remove('text-emerald-400');
             shiftStatus.classList.add('text-rose-500', 'animate-pulse');
          }
      };
      
      updateTimer();
      this.shiftInterval = setInterval(updateTimer, 1000);
  },
"""
    if start_shift_idx != -1 and end_shift_ui != -1:
        js = js[:start_shift_idx] + new_shift + '\n' + js[end_shift_ui:]
        
    with open('js/app_motorista.js', 'w', encoding='utf-8') as f:
        f.write(js)
    
    print("app_motorista.js patched.")

if __name__ == '__main__':
    patch_app_motorista_js()
