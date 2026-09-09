# -*- coding: utf-8 -*-
import re

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
                if(data.driverType === 'vinculado') {
                    driverData = data;
                } else {
                    this.showToast('Este CPF nao esta registrado como motorista vinculado.', 'error');
                    return;
                }
            } else {
                this.showToast('CPF nao encontrado. A empresa ja realizou seu cadastro?', 'error');
                return;
            }
        } else {
            const name = document.getElementById('login-name').value.trim();
            const cnpj = document.getElementById('login-cnpj').value.trim();
            if(!name || !cnpj) {
                this.showToast('Preencha Nome e CNPJ.', 'error');
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
        this.checkAuth();
        this.showToast('Bem-vindo(a), ' + driverData.name);
    } catch(e) {
        console.error(e);
        this.showToast('Erro ao realizar login.', 'error');
    } finally {
        btn.innerHTML = oldHtml;
        btn.disabled = false;
    }
  },'''

# Replace the loginDriver function using find & string slicing
start_str = "  loginDriver() {"
end_str = "  checkAuth() {"
start_idx = content.find(start_str)
end_idx = content.find(end_str)

if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + new_login_driver + "\n\n" + content[end_idx:]
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched app_motorista.js successfully.")
else:
    print("Failed to find boundaries.")
