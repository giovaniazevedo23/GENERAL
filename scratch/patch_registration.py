import os

def fix_sync():
    # 1. Patch app.js to save company to 'companies' on login (cadastro)
    app_js_path = 'js/app.js'
    with open(app_js_path, 'r', encoding='utf-8') as f:
        app_js = f.read()

    login_str = """          if (name && company && role) {
            appState.currentUser = { id, name, company, role, provider: 'manual' };
            usersDb[id] = appState.currentUser;
            localStorage.setItem('general_users_db', JSON.stringify(usersDb));
            localStorage.setItem('general_user', JSON.stringify(appState.currentUser));
            this.checkAuth();"""
            
    new_login_str = """          if (name && company && role) {
            appState.currentUser = { id, name, company, role, provider: 'manual' };
            usersDb[id] = appState.currentUser;
            localStorage.setItem('general_users_db', JSON.stringify(usersDb));
            localStorage.setItem('general_user', JSON.stringify(appState.currentUser));
            
            // Registra a empresa no Firebase instantaneamente
            if (window.db) {
                window.db.collection('companies').doc(company).set({ name: company }).catch(e => console.error(e));
                // Força a sincronização do usuário também
                this.syncToFirebase();
            }
            
            this.checkAuth();"""
            
    if login_str in app_js:
        app_js = app_js.replace(login_str, new_login_str)
        with open(app_js_path, 'w', encoding='utf-8') as f:
            f.write(app_js)
        print("js/app.js patched to save company on registration.")
    else:
        print("Could not find the login string in app.js")

    # 2. Patch app_motorista.js to read from both 'companies' and 'saved_plans' (to be safe and comprehensive)
    app_mot_path = 'js/app_motorista.js'
    with open(app_mot_path, 'r', encoding='utf-8') as f:
        app_mot = f.read()

    old_load = """    async loadCompanies() {
        const select = document.getElementById('motorista-company');
        if (!select || !window.db) return;
        
        try {
            // Buscando de saved_plans para evitar problemas de permissões em novas coleções
            const snap = await window.db.collection('saved_plans').get();
            const companies = new Set();
            snap.forEach(doc => {
                const data = doc.data();
                if (data.approvedByCompany) {
                    companies.add(data.approvedByCompany);
                }
            });
            
            if (companies.size === 0) {
                select.innerHTML = '<option value="">Nenhum plano com empresa cadastrado.</option>';
                return;
            }
            
            select.innerHTML = '<option value="">Selecione a empresa...</option>';
            companies.forEach(company => {
                select.innerHTML += `<option value="${company}">${company}</option>`;
            });
        } catch (e) {
            console.error("Erro ao carregar empresas:", e);
            select.innerHTML = '<option value="">Erro de permissão. Tente novamente.</option>';
        }
    },"""

    new_load = """    async loadCompanies() {
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

    if old_load in app_mot:
        app_mot = app_mot.replace(old_load, new_load)
        with open(app_mot_path, 'w', encoding='utf-8') as f:
            f.write(app_mot)
        print("js/app_motorista.js patched to load companies comprehensively.")
    else:
        print("Could not find the loadCompanies string in app_motorista.js")

if __name__ == '__main__':
    fix_sync()
