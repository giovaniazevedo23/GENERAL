import sys

def modify_motorista_html():
    file_path = r"c:\Users\giova\.gemini\antigravity\scratch\general-app\motorista.html"
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Modify Login Form
    old_login_company = """          <div class="mt-4">
            <label class="block text-xs font-bold text-slate-300 mb-1">Empresa Logística</label>
            <!-- Será preenchido via Firebase dinamicamente -->
            <select id="motorista-company" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-slate-200 font-mono focus:border-blue-500 outline-none transition-all">
               <option value="">Carregando empresas...</option>
            </select>
          </div>"""
    
    new_login_company = """          <div class="mt-4">
            <label class="block text-xs font-bold text-slate-300 mb-1">Empresa Logística</label>
            <input type="text" id="motorista-company" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-slate-200 font-mono focus:border-blue-500 outline-none transition-all" placeholder="Nome da empresa" />
          </div>
          <div class="mt-4">
            <label class="block text-xs font-bold text-slate-300 mb-1">CNPJ da Empresa</label>
            <input type="text" id="motorista-cnpj" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-slate-200 font-mono focus:border-blue-500 outline-none transition-all" placeholder="00.000.000/0001-00" oninput="this.value = this.value.replace(/[^0-9]/g, '').replace(/^(\\d{2})(\\d{3})(\\d{3})(\\d{4})(\\d{2}).*/, '$1.$2.$3/$4-$5');" />
          </div>
          <div class="mt-4">
            <label class="block text-xs font-bold text-slate-300 mb-1">Cargo</label>
            <input type="text" id="motorista-cargo" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-slate-200 font-mono focus:border-blue-500 outline-none transition-all" placeholder="Seu cargo (ex: Motorista)" value="Motorista" />
          </div>"""
          
    content = content.replace(old_login_company, new_login_company)
    
    # Modify Profile Modal
    old_profile_fields = """        <div>
          <label class="block text-xs font-bold text-slate-400 mb-1">Empresa</label>
          <input type="text" id="profile-company" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-blue-500 transition-all" />
        </div>
        <div>
          <label class="block text-xs font-bold text-slate-400 mb-1">Cargo</label>
          <input type="text" id="profile-role" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-blue-500 transition-all" />
        </div>"""
        
    new_profile_fields = """        <div>
          <label class="block text-xs font-bold text-slate-400 mb-1">Empresa</label>
          <input type="text" id="profile-company" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-blue-500 transition-all" />
        </div>
        <div>
          <label class="block text-xs font-bold text-slate-400 mb-1">CNPJ da Empresa</label>
          <input type="text" id="profile-cnpj" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-blue-500 transition-all" placeholder="00.000.000/0001-00" oninput="this.value = this.value.replace(/[^0-9]/g, '').replace(/^(\\d{2})(\\d{3})(\\d{3})(\\d{4})(\\d{2}).*/, '$1.$2.$3/$4-$5');" />
        </div>
        <div>
          <label class="block text-xs font-bold text-slate-400 mb-1">Cargo</label>
          <input type="text" id="profile-role" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-blue-500 transition-all" />
        </div>"""
        
    content = content.replace(old_profile_fields, new_profile_fields)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
        
def modify_app_motorista_js():
    file_path = r"c:\Users\giova\.gemini\antigravity\scratch\general-app\js\app_motorista.js"
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Update loadCompanies to no longer do anything since it's an input now (optional, but good to clean)
    old_load_companies = """    async loadCompanies() {
        const select = document.getElementById('motorista-company');
        if (!select || !window.db) return;
        
        try {
            const companies = new Set();
            
            // 1. Tenta buscar da coleção dedicada 'companies' (criada no cadastro)
            try {
                const compSnap = await window.db.collection('companies').get();
                compSnap.forEach(doc => companies.add(doc.id));
            } catch (err) {
                console.warn("Aviso ao ler companies, tentando saved_plans...", err);
            }
            
            // 2. Busca também do saved_plans (fallback/garantia)
            try {
                const snap = await window.db.collection('saved_plans').get();
                snap.forEach(doc => {
                    const data = doc.data();
                    if (data.approvedByCompany) companies.add(data.approvedByCompany);
                });
            } catch (err) {
                console.warn("Aviso ao ler saved_plans...", err);
            }
            
            if (companies.size === 0) {
                select.innerHTML = '<option value="">Nenhuma empresa cadastrada no sistema ainda.</option>';
                return;
            }
            
            select.innerHTML = '<option value="">Selecione a empresa...</option>';
            Array.from(companies).sort().forEach(company => {
                select.innerHTML += `<option value="${company}">${company}</option>`;
            });
        } catch (e) {
            console.error("Erro geral ao carregar empresas:", e);
            select.innerHTML = '<option value="">Erro ao carregar. Tente novamente.</option>';
        }
    },"""
    new_load_companies = """    async loadCompanies() {
        // Companies is now a text input, no need to load options.
    },"""
    content = content.replace(old_load_companies, new_load_companies)
    
    # 2. Update loadPlansForCompany to use CNPJ
    old_load_plans = """    async loadPlansForCompany(companyName) {
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
    },"""
    new_load_plans = """    async loadPlansForCompany(companyName) {
        if (!window.db) return;
        try {
            let snap;
            if (appState.currentUser && appState.currentUser.companyCnpj) {
                snap = await window.db.collection('saved_plans').where('carrierCnpj', '==', appState.currentUser.companyCnpj).get();
            } else {
                snap = await window.db.collection('saved_plans').where('approvedByCompany', '==', companyName).get();
            }
            appState.savedPlans = [];
            snap.forEach(doc => appState.savedPlans.push(doc.data()));
            this.renderMonitoringTab();
            this.showToast('Planos da empresa carregados.');
        } catch(e) {
            console.error("Erro ao carregar planos", e);
        }
    },"""
    content = content.replace(old_load_plans, new_load_plans)

    # 3. Update login()
    old_login = """  login() {
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
  },"""
    new_login = """  login() {
      const name = document.getElementById('motorista-name') ? document.getElementById('motorista-name').value.trim() : '';
      const company = document.getElementById('motorista-company') ? document.getElementById('motorista-company').value.trim() : '';
      const cnpj = document.getElementById('motorista-cnpj') ? document.getElementById('motorista-cnpj').value.trim() : '';
      const role = document.getElementById('motorista-cargo') ? document.getElementById('motorista-cargo').value.trim() : 'Motorista';
      
      if (!name || !company || !cnpj) {
          this.showToast('Preencha seu nome, empresa e CNPJ!');
          return;
      }
      
      const id = 'MOT-' + Math.floor(Math.random() * 90000 + 10000);
      appState.currentUser = { id, name, company, companyCnpj: cnpj, role: role, provider: 'manual' };
      localStorage.setItem('general_user', JSON.stringify(appState.currentUser));
      this.checkAuth();
      this.showToast(`Bem-vindo, ${name}!`);
  },"""
    content = content.replace(old_login, new_login)
    
    # 4. Update updateProfileUI() and saveProfile()
    old_update_ui = """  updateProfileUI() {
    if (!appState.currentUser) return;
    const { name, email, phone, company, role } = appState.currentUser;
    const setVal = (id, val) => { const el = document.getElementById(id); if (el) el.value = val || ''; };
    setVal('profile-name', name);
    setVal('profile-email', email);
    setVal('profile-phone', phone);
    setVal('profile-company', company);
    setVal('profile-role', role);
  },"""
    new_update_ui = """  updateProfileUI() {
    if (!appState.currentUser) return;
    const { name, email, phone, company, companyCnpj, role } = appState.currentUser;
    const setVal = (id, val) => { const el = document.getElementById(id); if (el) el.value = val || ''; };
    setVal('profile-name', name);
    setVal('profile-email', email);
    setVal('profile-phone', phone);
    setVal('profile-company', company);
    setVal('profile-cnpj', companyCnpj);
    setVal('profile-role', role);
  },"""
    content = content.replace(old_update_ui, new_update_ui)
    
    old_save_profile = """  saveProfile() {
    const getVal = id => { const el = document.getElementById(id); return el ? el.value : ''; };
    if (!appState.currentUser) appState.currentUser = {};
    appState.currentUser.name = getVal('profile-name');
    appState.currentUser.email = getVal('profile-email');
    appState.currentUser.phone = getVal('profile-phone');
    appState.currentUser.company = getVal('profile-company');
    appState.currentUser.role = getVal('profile-role');
    
    localStorage.setItem('general_user', JSON.stringify(appState.currentUser));
    this.closeProfileModal();
    this.showToast('Perfil atualizado com sucesso!');
    this.syncToFirebase();
  },"""
    new_save_profile = """  saveProfile() {
    const getVal = id => { const el = document.getElementById(id); return el ? el.value : ''; };
    if (!appState.currentUser) appState.currentUser = {};
    const oldCnpj = appState.currentUser.companyCnpj;
    
    appState.currentUser.name = getVal('profile-name');
    appState.currentUser.email = getVal('profile-email');
    appState.currentUser.phone = getVal('profile-phone');
    appState.currentUser.company = getVal('profile-company');
    appState.currentUser.companyCnpj = getVal('profile-cnpj');
    appState.currentUser.role = getVal('profile-role');
    
    localStorage.setItem('general_user', JSON.stringify(appState.currentUser));
    this.closeProfileModal();
    this.showToast('Perfil atualizado com sucesso!');
    this.syncToFirebase();
    
    if (oldCnpj !== appState.currentUser.companyCnpj) {
        this.loadPlansForCompany(appState.currentUser.company);
        this.showToast('Empresa alterada. Atualizando planos...');
    }
  },"""
    content = content.replace(old_save_profile, new_save_profile)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    modify_motorista_html()
    modify_app_motorista_js()
    print("Modifications applied successfully.")
