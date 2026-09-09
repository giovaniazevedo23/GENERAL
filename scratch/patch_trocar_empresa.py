# -*- coding: utf-8 -*-
html_path = r'C:\Users\giova\.gemini\antigravity\scratch\general-app\motorista.html'
js_path = r'C:\Users\giova\.gemini\antigravity\scratch\general-app\js\app_motorista.js'

with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

btn_trocar = '''
          <button id="btn-trocar-empresa" onclick="App.promptChangeCompany(); App.toggleMobileDrawer();" class="hidden w-full bg-blue-500/10 hover:bg-blue-500/20 border border-blue-500/30 text-blue-300 font-bold py-2.5 rounded-xl text-xs transition-all flex items-center justify-center gap-2 mb-3">
            <i data-lucide="building-2" class="w-4 h-4 text-blue-400"></i>
            Trocar Empresa (CNPJ)
          </button>
'''
btn_trocar_desktop = '''
        <button id="btn-trocar-empresa-desktop" onclick="App.promptChangeCompany()" class="hidden w-full bg-blue-500/10 hover:bg-blue-500/20 border border-blue-500/30 text-blue-300 px-3 py-2.5 rounded-xl text-xs font-bold transition-all flex items-center gap-3">
          <i data-lucide="building-2" class="w-4 h-4 text-blue-400"></i>
          Trocar Empresa
        </button>
'''

if 'id="btn-trocar-empresa"' not in html_content:
    # mobile
    html_content = html_content.replace(
        '''          <button onclick="App.logout(); App.toggleMobileDrawer();" class="w-full bg-rose-500/10 ''',
        btn_trocar + '''          <button onclick="App.logout(); App.toggleMobileDrawer();" class="w-full bg-rose-500/10 '''
    )
    # desktop
    html_content = html_content.replace(
        '''        <button onclick="App.logout()" class="flex-shrink-0 flex items-center gap-2 ''',
        btn_trocar_desktop + '''        <button onclick="App.logout()" class="flex-shrink-0 flex items-center gap-2 '''
    )
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)


with open(js_path, 'r', encoding='utf-8') as f:
    js_content = f.read()

change_company_func = '''
  async promptChangeCompany() {
      if(!appState.currentUser || appState.currentUser.driverType !== 'autonomo') return;
      
      const newCnpj = prompt('Digite o novo CNPJ da empresa que voc\\u00ea vai atender:');
      if(newCnpj) {
          const cnpjClean = newCnpj.replace(/\\D/g, '');
          if(cnpjClean.length > 0) {
              try {
                  await window.db.collection('users').doc(appState.currentUser.id).update({
                      companyCnpj: cnpjClean
                  });
                  appState.currentUser.companyCnpj = cnpjClean;
                  localStorage.setItem('general_user', JSON.stringify(appState.currentUser));
                  this.showToast('CNPJ atualizado com sucesso! Nova rota pronta.', 'success');
                  // Update UI if necessary
                  const companyInput = document.getElementById('motorista-company');
                  if(companyInput) companyInput.value = cnpjClean;
              } catch(e) {
                  console.error(e);
                  this.showToast('Erro ao atualizar empresa.', 'error');
              }
          }
      }
  },
'''

if 'promptChangeCompany()' not in js_content:
    js_content = js_content.replace(
        '''  logout() {''',
        change_company_func + '''\n  logout() {'''
    )
    
    # CheckAuth should show the button if autonomo
    # Let's inject logic in checkAuth
    auth_logic = '''
      const btnTrocar = document.getElementById('btn-trocar-empresa');
      const btnTrocarDesk = document.getElementById('btn-trocar-empresa-desktop');
      if(appState.currentUser && appState.currentUser.driverType === 'autonomo') {
          if(btnTrocar) btnTrocar.classList.remove('hidden');
          if(btnTrocarDesk) btnTrocarDesk.classList.remove('hidden');
      } else {
          if(btnTrocar) btnTrocar.classList.add('hidden');
          if(btnTrocarDesk) btnTrocarDesk.classList.add('hidden');
      }
    '''
    js_content = js_content.replace(
        '''document.getElementById('motorista-cpf').value = appState.currentUser.cpf || appState.currentUser.id;''',
        '''document.getElementById('motorista-cpf').value = appState.currentUser.cpf || appState.currentUser.id;''' + auth_logic
    )
    
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(js_content)
        
print("Trocar empresa implemented.")
