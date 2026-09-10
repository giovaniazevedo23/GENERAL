import re
import sys

def patch_html(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(filepath, 'r', encoding='utf-16') as f:
            content = f.read()

    # The block we want to replace starts with: <div id="login-form-motorista" ...
    # And ends before <!-- CHECKLIST PRÉ-MISSÃO OVERLAY --> or the end of login-overlay
    
    pattern = re.compile(r'(<div id="login-form-motorista".*?)(<!-- CHECKLIST PRÉ-MISSÃO OVERLAY -->)', re.DOTALL)
    
    new_html = """<div id="login-form-motorista" class="space-y-4 w-full">
          <div class="mb-4">
            <label class="block text-xs font-bold text-slate-400 mb-2 uppercase tracking-wider">Como você deseja acessar?</label>
            <div class="grid grid-cols-2 gap-2">
              <button type="button" id="btn-login-vinculado" onclick="App.setLoginType('vinculado')" class="bg-blue-600 text-white text-sm font-bold py-2 rounded-lg border border-blue-500 transition-all">Sou Vinculado</button>
              <button type="button" id="btn-login-autonomo" onclick="App.setLoginType('autonomo')" class="bg-slate-800 text-slate-400 text-sm font-bold py-2 rounded-lg border border-slate-700 transition-all hover:bg-slate-700 hover:text-slate-300">Sou Autônomo</button>
            </div>
          </div>
          
          <div id="field-driver-name" class="hidden">
            <label class="block text-sm font-bold text-slate-300 mb-1">Nome Completo</label>
            <input type="text" id="login-name" class="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-blue-500 transition-colors" placeholder="João da Silva">
          </div>
          
          <div>
            <label class="block text-sm font-bold text-slate-300 mb-1">Seu CPF</label>
            <input type="text" id="login-cpf" class="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-blue-500 transition-colors font-mono" placeholder="000.000.000-00">
          </div>
          
          <div id="field-driver-company" class="hidden">
            <label class="block text-sm font-bold text-slate-300 mb-1">Empresa Logística</label>
            <input type="text" id="login-company" class="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-blue-500 transition-colors" placeholder="Nome da sua transportadora">
          </div>

          <div id="field-driver-cnpj" class="hidden">
            <label class="block text-sm font-bold text-slate-300 mb-1">CNPJ da Empresa Contratante</label>
            <input type="text" id="login-cnpj" class="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-blue-500 transition-colors font-mono" placeholder="00.000.000/0000-00">
          </div>

          <div id="field-driver-cargo" class="hidden">
            <label class="block text-sm font-bold text-slate-300 mb-1">Cargo</label>
            <input type="text" id="login-cargo" class="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-blue-500 transition-colors font-mono" placeholder="Seu cargo (ex: Motorista)" value="Motorista">
          </div>
          
          <button type="button" id="btn-action-login-motorista" onclick="App.loginDriver()" class="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-3 rounded-xl shadow-lg shadow-blue-500/30 transition-all flex items-center justify-center gap-2 mt-6">
            Acessar Sistema <i data-lucide="arrow-right" class="w-4 h-4"></i>
          </button>
        </div>
      </div>
    </div>
  </div>

  \\2"""

    match = pattern.search(content)
    if not match:
        print("HTML pattern not found!")
        return False
        
    content = re.sub(pattern, new_html, content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched motorista.html")
    return True


def patch_js(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(filepath, 'r', encoding='utf-16') as f:
            content = f.read()

    # 1. Update setLoginType
    pattern_setLoginType = re.compile(r'(setLoginType\(type\)\s*\{)(.*?)(^\s*\},)', re.MULTILINE | re.DOTALL)
    
    new_setLoginType = r"""\1
    this.loginType = type;
    const btnVinc = document.getElementById('btn-login-vinculado');
    const btnAuto = document.getElementById('btn-login-autonomo');
    const fieldName = document.getElementById('field-driver-name');
    const fieldCnpj = document.getElementById('field-driver-cnpj');
    const fieldCompany = document.getElementById('field-driver-company');
    const fieldCargo = document.getElementById('field-driver-cargo');
    
    if(type === 'vinculado') {
        if(btnVinc) btnVinc.className = 'bg-blue-600 text-white text-sm font-bold py-2 rounded-lg border border-blue-500 transition-all';
        if(btnAuto) btnAuto.className = 'bg-slate-800 text-slate-400 text-sm font-bold py-2 rounded-lg border border-slate-700 transition-all hover:bg-slate-700 hover:text-slate-300';
        if(fieldName) fieldName.classList.add('hidden');
        if(fieldCnpj) fieldCnpj.classList.add('hidden');
        if(fieldCompany) fieldCompany.classList.add('hidden');
        if(fieldCargo) fieldCargo.classList.add('hidden');
    } else {
        if(btnAuto) btnAuto.className = 'bg-blue-600 text-white text-sm font-bold py-2 rounded-lg border border-blue-500 transition-all';
        if(btnVinc) btnVinc.className = 'bg-slate-800 text-slate-400 text-sm font-bold py-2 rounded-lg border border-slate-700 transition-all hover:bg-slate-700 hover:text-slate-300';
        if(fieldName) fieldName.classList.remove('hidden');
        if(fieldCnpj) fieldCnpj.classList.remove('hidden');
        if(fieldCompany) fieldCompany.classList.remove('hidden');
        if(fieldCargo) fieldCargo.classList.remove('hidden');
    }\3"""

    content = re.sub(pattern_setLoginType, new_setLoginType, content)

    # 2. Update loginDriver autonomo part
    pattern_loginDriver = re.compile(r'(} else \{\s*const name = document\.getElementById\(\'login-name\'\)\.value\.trim\(\);\s*const cnpj = document\.getElementById\(\'login-cnpj\'\)\.value\.trim\(\);\s*)(if\(\!name \|\| \!cnpj\))(.*?\})(\s*const cnpjClean = cnpj\.replace\(/\\D/g, \'\'\);\s*)(driverData = \{.*?driverType: \'autonomo\',)(.*?lastLogin: firebase\.firestore\.FieldValue\.serverTimestamp\(\)\s*\};\s*await window\.db\.collection\(\'users\'\)\.doc\(cpfClean\)\.set\(driverData, \{ merge: true \}\);\s*\})', re.DOTALL)

    new_loginDriver = r"""} else {
            const nameEl = document.getElementById('login-name');
            const cnpjEl = document.getElementById('login-cnpj');
            const compEl = document.getElementById('login-company');
            const cargoEl = document.getElementById('login-cargo');
            
            const name = nameEl ? nameEl.value.trim() : '';
            const cnpj = cnpjEl ? cnpjEl.value.trim() : '';
            const company = compEl ? compEl.value.trim() : '';
            const cargo = cargoEl ? cargoEl.value.trim() : 'Motorista';
            
            if(!name || !cnpj || !company) {
                this.showToast('Preencha Nome, Empresa e CNPJ.', 'error');
                return;
            }
            const cnpjClean = cnpj.replace(/\\D/g, '');
            
            driverData = { 
                id: cpfClean, 
                name: name, 
                cpf: cpf, 
                company: company,
                companyCnpj: cnpjClean, 
                role: cargo,
                driverType: 'autonomo',
                lastLogin: firebase.firestore.FieldValue.serverTimestamp()
            };
            
            await window.db.collection('users').doc(cpfClean).set(driverData, { merge: true });
        }"""
        
    content = re.sub(pattern_loginDriver, new_loginDriver, content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched app_motorista.js")


if __name__ == '__main__':
    patch_html('motorista.html')
    patch_js('www/js/app_motorista.js')
