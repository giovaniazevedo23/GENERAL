import os

def patch_app_motorista():
    file_path = 'js/app_motorista.js'
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    old_func = """    async loadCompanies() {
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
    },"""

    new_func = """    async loadCompanies() {
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

    if old_func in content:
        content = content.replace(old_func, new_func)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("js/app_motorista.js patched successfully.")
    else:
        print("Could not find the old loadCompanies function in js/app_motorista.js")

if __name__ == '__main__':
    patch_app_motorista()
