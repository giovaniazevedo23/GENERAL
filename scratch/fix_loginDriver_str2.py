# -*- coding: utf-8 -*-
js_path = r'C:\Users\giova\.gemini\antigravity\scratch\general-app\js\app_motorista.js'

with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

new_login_driver = '''  async loginDriver() {
    const type = this.loginType || 'vinculado';
    const cpf = document.getElementById('login-cpf').value.trim();
    
    if(!cpf) {
        this.showToast('Por favor, digite seu CPF.', 'error');
        return;
    }
    
    const cpfClean = cpf.replace(/\\D/g, '');
    if(cpfClean.length !== 11) {
        this.showToast('CPF invalido.', 'error');
        return;
    }
    
    const btn = document.getElementById('btn-action-login-motorista');
    const oldHtml = btn.innerHTML;
    btn.innerHTML = '<div class="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div> Entrando...';
    btn.disabled = true;
    
    try {
        let driverData = null;
        if(type === 'vinculado') {
            const doc = await window.db.collection('users').doc(cpfClean).get();
            if(doc.exists) {
                const data = doc.data();
                if(data.driverType === 'vinculado' || data.type === 'vinculado' || data.role === 'motorista') {
                    driverData = data;
                } else {
                    this.showToast('Este CPF não está registrado como motorista vinculado.', 'error');
                    return;
                }
            } else {
                this.showToast('CPF não encontrado. A transportadora já realizou seu cadastro?', 'error');
                return;
            }
        } else {
            const name = document.getElementById('login-name').value.trim();
            const cnpj = document.getElementById('login-cnpj').value.trim();
            if(!name || !cnpj) {
                this.showToast('Preencha Nome e CNPJ da transportadora.', 'error');
                return;
            }
            const cnpjClean = cnpj.replace(/\\D/g, '');
            
            driverData = { 
                id: cpfClean, 
                name: name, 
                cpf: cpf, 
                companyCnpj: cnpjClean, 
                role: 'motorista',
                driverType: 'autonomo',
                lastLogin: firebase.firestore.FieldValue.serverTimestamp()
            };
            
            await window.db.collection('users').doc(cpfClean).set(driverData, { merge: true });
        }
        
        appState.currentUser = driverData;
        localStorage.setItem('general_user', JSON.stringify(driverData));
        
        document.getElementById('login-overlay').classList.add('hidden');
        this.showToast(Bem-vindo, !);
        this.checkAuth(); 
    } catch(e) {
        console.error(e);
        this.showToast('Erro ao realizar login.', 'error');
    } finally {
        btn.innerHTML = oldHtml;
        btn.disabled = false;
    }
  },'''

start_idx = content.find("  async loginDriver() {")
end_idx = content.find("    startDriverCamera() {")

if start_idx != -1 and end_idx != -1:
    # Need to go back to the previous line (the comment // --- C...)
    line_start = content.rfind("  //", 0, end_idx)
    if line_start != -1:
        end_idx = line_start
    content = content[:start_idx] + new_login_driver + "\n\n" + content[end_idx:]
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fix applied successfully.")
else:
    print("Could not find start or end index.")
