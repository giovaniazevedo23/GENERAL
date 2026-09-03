import os

def patch_app_js():
    with open('js/app.js', 'r', encoding='utf-8') as f:
        content = f.read()
        
    # We need to make Gestor save the company to a companies collection when updating profile
    profile_save_str = "appState.currentUser.company = newCompany;"
    new_profile_save = """appState.currentUser.company = newCompany;
        if (window.db && newCompany) {
            window.db.collection('companies').doc(newCompany).set({ name: newCompany }).catch(console.error);
        }
"""
    if profile_save_str in content:
        content = content.replace(profile_save_str, new_profile_save)

    # We also need to listen for route_evaluations in real time
    # Let's see if we can find where initFirebaseSync is. (It's in state.js or app.js)
    # The user relies on `syncFromFirebase`. Let's add a listener in `syncFromFirebase` or initialization.
    sync_str = "async syncFromFirebase() {"
    new_sync_str = """async syncFromFirebase() {
      if (window.db) {
          window.db.collection('route_evaluations').onSnapshot(snapshot => {
              appState.routeEvaluations = appState.routeEvaluations || [];
              let changed = false;
              snapshot.docChanges().forEach(change => {
                  if (change.type === 'added' || change.type === 'modified') {
                      const data = change.doc.data();
                      const existingIndex = appState.routeEvaluations.findIndex(e => e.id === data.id);
                      if (existingIndex >= 0) appState.routeEvaluations[existingIndex] = data;
                      else appState.routeEvaluations.push(data);
                      changed = true;
                  }
              });
              if (changed) {
                  localStorage.setItem('general_route_evaluations', JSON.stringify(appState.routeEvaluations));
                  // Optionally trigger a re-render of the map or monitoring view
                  if (window.App && typeof window.App.renderMonitoringTab === 'function') {
                      window.App.renderMonitoringTab();
                  }
              }
          });
      }
"""
    if sync_str in content:
        content = content.replace(sync_str, new_sync_str)
        
    with open('js/app.js', 'w', encoding='utf-8') as f:
        f.write(content)
    print("js/app.js patched.")

def patch_app_motorista_js():
    with open('js/app_motorista.js', 'r', encoding='utf-8') as f:
        content = f.read()

    # The motorista app should have a custom login logic
    login_str = "login() {"
    end_login_str = "  logout() {" # We will replace the entire login function
    
    idx_start = content.find(login_str)
    idx_end = content.find(end_login_str)
    
    if idx_start != -1 and idx_end != -1:
        custom_login = """login() {
      const name = document.getElementById('motorista-name') ? document.getElementById('motorista-name').value : '';
      const company = document.getElementById('motorista-company') ? document.getElementById('motorista-company').value : '';
      
      if (!name || !company) {
          this.showToast('Preencha seu nome e selecione a empresa!');
          return;
      }
      
      const id = 'MOT-' + Math.floor(Math.random() * 90000 + 10000);
      appState.currentUser = { id, name, company, role: 'Motorista', provider: 'manual' };
      localStorage.setItem('general_user', JSON.stringify(appState.currentUser));
      this.checkAuth();
      this.showToast(`Bem-vindo, ${name}!`);
  },
"""
        content = content[:idx_start] + custom_login + content[idx_end:]

    # Now we need to modify checkAuth to only load plans for this company
    check_auth_str = "checkAuth() {"
    new_check_auth = """checkAuth() {
      const overlay = document.getElementById('login-overlay');
      if (appState.currentUser) {
        if (overlay) overlay.style.opacity = '0';
        setTimeout(() => { if (overlay) overlay.classList.add('hidden'); }, 300);
        this.updateProfileUI();
        this.loadPlansForCompany(appState.currentUser.company);
        this.switchTab('monitoring'); // Force monitoramento tab
      } else {
        if (overlay) {
            overlay.classList.remove('hidden');
            overlay.style.opacity = '1';
            this.loadCompanies();
        }
      }
    },
    
    async loadCompanies() {
        const select = document.getElementById('motorista-company');
        if (!select || !window.db) return;
        
        try {
            const snap = await window.db.collection('companies').get();
            if (snap.empty) {
                select.innerHTML = '<option value="">Nenhuma empresa cadastrada pelo Gestor ainda.</option>';
                return;
            }
            select.innerHTML = '<option value="">Selecione a empresa...</option>';
            snap.forEach(doc => {
                select.innerHTML += `<option value="${doc.id}">${doc.id}</option>`;
            });
        } catch (e) {
            console.error("Erro ao carregar empresas:", e);
        }
    },
    
    async loadPlansForCompany(companyName) {
        if (!window.db) return;
        try {
            const snap = await window.db.collection('saved_plans').where('approvedByCompany', '==', companyName).get();
            appState.savedPlans = [];
            snap.forEach(doc => appState.savedPlans.push(doc.data()));
            this.renderMonitoringTab(); // or whatever renders the plan selection for monitoring
            this.showToast('Planos da empresa carregados.');
        } catch(e) {
            console.error("Erro ao carregar planos", e);
        }
    },
"""
    if check_auth_str in content:
        content = content.replace(check_auth_str, new_check_auth)

    # We should override the login button event listener. In app.js, the button has id btn-action-login
    # motorista.html uses btn-action-login-motorista
    init_str = "document.getElementById('profile-show-copilot')"
    new_init_str = """
    const btnLoginMot = document.getElementById('btn-action-login-motorista');
    if (btnLoginMot) btnLoginMot.addEventListener('click', () => this.login());
    
    document.getElementById('profile-show-copilot')"""
    if init_str in content:
        content = content.replace(init_str, new_init_str)
        
    with open('js/app_motorista.js', 'w', encoding='utf-8') as f:
        f.write(content)
    print("js/app_motorista.js patched.")

if __name__ == '__main__':
    patch_app_js()
    patch_app_motorista_js()
