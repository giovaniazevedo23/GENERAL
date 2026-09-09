# -*- coding: utf-8 -*-
import re

html_path = r'C:\Users\giova\.gemini\antigravity\scratch\gestor-app\index.html'
js_path = r'C:\Users\giova\.gemini\antigravity\scratch\gestor-app\js\app.js'

with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# 1. Add Navigation Button
nav_button = '''
          <button data-tab="driver-registration" onclick="App.switchTab('driver-registration')" class="nav-button w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-bold text-slate-400 hover:bg-slate-800 hover:text-slate-200 transition-all">
            <i data-lucide="user-plus" class="w-4 h-4 text-orange-400"></i>
            Cadastrar Motorista
          </button>
'''
if 'data-tab="driver-registration"' not in html_content:
    html_content = html_content.replace(
        '''          </button>\n\n\n        </nav>''',
        f'''          </button>\n{nav_button}\n\n        </nav>'''
    )

# 2. Add View HTML
view_html = '''
    <!-- VIEW: CADASTRO DE MOTORISTAS VINCULADOS -->
    <div id="driver-registration-view" class="view hidden space-y-6">
      <div class="flex items-center justify-between mb-2">
        <div>
          <h2 class="text-2xl font-black text-white tracking-tight">Cadastro de Motoristas</h2>
          <p class="text-sm text-slate-400 mt-1">Vincule novos motoristas ao CNPJ da sua empresa.</p>
        </div>
      </div>
      
      <div class="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl">
        <form onsubmit="App.saveLinkedDriver(event)" class="space-y-4">
          <div>
            <label class="block text-xs font-bold text-slate-300 mb-1">Nome Completo</label>
            <input type="text" id="reg-driver-name" required class="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2 text-white outline-none focus:border-blue-500" placeholder="Nome do Motorista" />
          </div>
          <div>
            <label class="block text-xs font-bold text-slate-300 mb-1">CPF</label>
            <input type="text" id="reg-driver-cpf" required oninput="let v = this.value.replace(/\D/g, ''); v = v.replace(/(\d{3})(\d)/, '.'); v = v.replace(/(\d{3})(\d)/, '.'); v = v.replace(/(\d{3})(\d{1,2})$/, '-'); this.value = v;" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2 text-white outline-none focus:border-blue-500 font-mono" placeholder="000.000.000-00" />
          </div>
          <div>
            <label class="block text-xs font-bold text-slate-300 mb-1">Telefone / WhatsApp (Opcional)</label>
            <input type="text" id="reg-driver-phone" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2 text-white outline-none focus:border-blue-500" placeholder="(11) 99999-9999" />
          </div>
          <button type="submit" class="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-3 rounded-xl shadow-lg transition-all flex items-center justify-center gap-2">
            <i data-lucide="save" class="w-5 h-5"></i>
            Salvar Motorista Vinculado
          </button>
        </form>
      </div>
    </div>
'''
if 'id="driver-registration-view"' not in html_content:
    html_content = html_content.replace(
        '''    <!-- VIEW: PLANNER -->''',
        f'''{view_html}\n    <!-- VIEW: PLANNER -->'''
    )

if 'id="plan-driver-name"' in html_content:
    datalist = '''      <datalist id="registered-drivers-list"></datalist>'''
    html_content = html_content.replace(
        '''<input id="plan-driver-name" type="text" placeholder="Nome Completo do Motorista" class="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-white focus:border-blue-500 outline-none transition-all" />''',
        f'''<input id="plan-driver-name" type="text" list="registered-drivers-list" placeholder="Selecione ou digite o nome do motorista" class="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-white focus:border-blue-500 outline-none transition-all" />\n{datalist}'''
    )

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)


with open(js_path, 'r', encoding='utf-8') as f:
    js_content = f.read()

js_code = '''
  async saveLinkedDriver(e) {
    e.preventDefault();
    if(!appState.currentUser || !appState.currentUser.companyCnpj) {
        this.showToast('Voce precisa configurar o CNPJ da sua empresa no seu perfil primeiro.', 'warning');
        return;
    }
    const name = document.getElementById('reg-driver-name').value.trim();
    const cpf = document.getElementById('reg-driver-cpf').value.trim();
    const phone = document.getElementById('reg-driver-phone').value.trim();
    
    if(!name || !cpf) {
        this.showToast('Preencha nome e CPF.', 'warning');
        return;
    }
    
    const cpfClean = cpf.replace(/\\D/g, '');
    if(cpfClean.length !== 11) {
        this.showToast('CPF invalido.', 'warning');
        return;
    }
    
    const btn = e.target.querySelector('button');
    const oldText = btn.innerHTML;
    btn.innerHTML = '<div class="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div> Salvando...';
    btn.disabled = true;
    
    try {
        await window.db.collection('users').doc(cpfClean).set({
            name: name,
            cpf: cpf,
            phone: phone,
            role: 'motorista',
            driverType: 'vinculado',
            companyCnpj: appState.currentUser.companyCnpj,
            createdAt: firebase.firestore.FieldValue.serverTimestamp()
        }, { merge: true });
        
        this.showToast('Motorista vinculado cadastrado com sucesso!', 'success');
        document.getElementById('reg-driver-name').value = '';
        document.getElementById('reg-driver-cpf').value = '';
        document.getElementById('reg-driver-phone').value = '';
        this.loadRegisteredDrivers(); // update datalist
    } catch(err) {
        console.error(err);
        this.showToast('Erro ao salvar motorista.', 'error');
    } finally {
        btn.innerHTML = oldText;
        btn.disabled = false;
    }
  },

  async loadRegisteredDrivers() {
      if(!appState.currentUser || !appState.currentUser.companyCnpj || !window.db) return;
      try {
          const snapshot = await window.db.collection('users')
              .where('role', '==', 'motorista')
              .where('companyCnpj', '==', appState.currentUser.companyCnpj)
              .get();
              
          const datalist = document.getElementById('registered-drivers-list');
          if(datalist) {
              datalist.innerHTML = '';
              snapshot.forEach(doc => {
                  const data = doc.data();
                  const option = document.createElement('option');
                  option.value = data.name;
                  option.textContent = data.cpf;
                  datalist.appendChild(option);
              });
          }
      } catch(e) {
          console.error("Erro ao carregar motoristas:", e);
      }
  },
'''

if 'saveLinkedDriver(' not in js_content:
    js_content = js_content.replace(
        '''  showDriverModal() {''',
        f'''{js_code}\n  showDriverModal() {{'''
    )

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js_content)

print("Gestor-app patched successfully.")
