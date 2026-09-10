# -*- coding: utf-8 -*-
js_path = r'C:\Users\giova\.gemini\antigravity\scratch\gestor-app\js\app.js'

with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

func_code = '''
  async saveLinkedDriver(e) {
      e.preventDefault();
      
      const btn = e.target.querySelector('button[type="submit"]');
      const oldHtml = btn.innerHTML;
      btn.innerHTML = '<div class="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div> Salvando...';
      btn.disabled = true;

      try {
          const name = document.getElementById('reg-driver-name').value.trim();
          const cpf = document.getElementById('reg-driver-cpf').value.trim();
          const phone = document.getElementById('reg-driver-phone').value.trim();
          
          if(!name || !cpf) {
              this.showToast('Nome e CPF são obrigatórios.', 'error');
              return;
          }
          
          const cpfClean = cpf.replace(/\D/g, '');
          if(cpfClean.length !== 11) {
              this.showToast('CPF inválido.', 'error');
              return;
          }
          
          // Current Gestor's CNPJ
          const companyCnpj = appState.currentUser?.companyCnpj || 'GENERIC_CNPJ';
          
          const driverData = {
              id: cpfClean,
              name: name,
              cpf: cpf,
              phone: phone,
              companyCnpj: companyCnpj,
              role: 'motorista',
              driverType: 'vinculado',
              registeredBy: appState.currentUser?.id || 'gestor',
              createdAt: firebase.firestore.FieldValue.serverTimestamp()
          };
          
          await window.db.collection('users').doc(cpfClean).set(driverData, { merge: true });
          
          this.showToast('Motorista vinculado cadastrado com sucesso!', 'success');
          e.target.reset();
          
          // Optionally switch back to planner or dashboard
          this.switchTab('planner');
      } catch(err) {
          console.error(err);
          this.showToast('Erro ao cadastrar motorista.', 'error');
      } finally {
          btn.innerHTML = oldHtml;
          btn.disabled = false;
      }
  },
'''

if 'saveLinkedDriver(e)' not in content:
    content = content.replace(
        '''  saveCompanyExtra() {''',
        func_code + '''\n  saveCompanyExtra() {'''
    )
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Injected saveLinkedDriver successfully.")
else:
    print("saveLinkedDriver already exists.")
