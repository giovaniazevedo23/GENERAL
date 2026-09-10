import os
import re

def fix_cpf_mask(filepath):
    if not os.path.exists(filepath): return
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Fix the oninput regex
    old_mask = r"let v = this.value.replace(/\D/g, ''); v = v.replace(/\(\\d\{3\}\)\(\\d\)/, '\$1\.\$2'); v = v.replace(/\(\\d\{3\}\)\(\\d\)/, '\$1\.\$2'); v = v.replace(/\(\\d\{3\}\)\(\\d\{1,2\}\)\$/, '\$1-\$2'); this.value = v;"
    new_mask = r"let v = this.value.replace(/\\D/g, '').substring(0, 11); if(v.length>9) v=v.replace(/(\\d{3})(\\d{3})(\\d{3})(\\d{1,2})/, '$1.$2.$3-$4'); else if(v.length>6) v=v.replace(/(\\d{3})(\\d{3})(\\d{1,3})/, '$1.$2.$3'); else if(v.length>3) v=v.replace(/(\\d{3})(\\d{1,3})/, '$1.$2'); this.value = v;"
    
    # We can just replace the whole attribute because there might be slight variations
    content = re.sub(r'oninput="let v = this\.value\.replace\([^"]+"', f'oninput="{new_mask}"', content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)


def fix_toast_zindex(filepath):
    if not os.path.exists(filepath): return
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    content = content.replace('z-50', 'z-[9999]')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)


def fix_landing_page():
    path = 'landing-page/index.html'
    if not os.path.exists(path): return
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    content = content.replace('v5.2 Padrão Militar (Pilares & Atividades Rota)', 'Nova Versão já disponível')
    content = content.replace('v5.2 Padrão Militar (Pilares & Atividades Rota)', 'Nova Versão já dispon\u00edvel')
    
    # Remove the first Avaliar Aplicativo button (which is near App Motoristas)
    content = re.sub(r'<a href="[^"]*"[^>]*>\s*<i data-lucide="star"[^>]*></i>\s*Avaliar Aplicativo\s*</a>', '', content, count=1)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def fix_gestor_isolation():
    path = 'www/js/app.js'
    if not os.path.exists(path): return
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # In renderRiskDashboard
    isolation_code = """
    const myCnpj = (appState.currentUser && appState.currentUser.companyCnpj) ? appState.currentUser.companyCnpj.replace(/\\D/g, '') : null;
    if (myCnpj) {
        feedbacks = feedbacks.filter(f => f.companyCnpj && f.companyCnpj.replace(/\\D/g, '') === myCnpj);
        rapidReports = rapidReports.filter(r => r.companyCnpj && r.companyCnpj.replace(/\\D/g, '') === myCnpj);
    }
    """
    
    if "const feedbacks = JSON.parse(localStorage.getItem('GENERAL_FEEDBACKS')" in content:
        content = content.replace("const rapidReports = JSON.parse(localStorage.getItem('GENERAL_RAPID_REPORTS') || '[]');",
                                  "const rapidReports = JSON.parse(localStorage.getItem('GENERAL_RAPID_REPORTS') || '[]');" + isolation_code)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def fix_motorista_logic():
    path = 'www/js/app_motorista.js'
    if not os.path.exists(path): return
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Fix setLoginType completely by replacing it
    pattern_set_login = r"setLoginType\(type\)\s*\{[\s\S]*?\}\s*\},"
    
    new_set_login = """setLoginType(type) {
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
    }
  },"""
    
    content = re.sub(pattern_set_login, new_set_login, content)

    # Fix loginDriver completely
    pattern_login_driver = r"async loginDriver\(\)\s*\{[\s\S]*?\}\s*catch\(e\)\s*\{\s*console\.error\(e\);\s*this\.showToast\('Erro ao realizar login\.', 'error'\);\s*\}\s*finally\s*\{\s*btn\.innerHTML = oldHtml;\s*btn\.disabled = false;\s*\}\s*\}"
    
    new_login_driver = r"""async loginDriver() {
    const type = this.loginType || 'vinculado';
    const cpfEl = document.getElementById('login-cpf');
    const cpf = cpfEl ? cpfEl.value.trim() : '';
    
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
        }
        
        appState.currentUser = driverData;
        localStorage.setItem('general_user', JSON.stringify(driverData));
        
        document.getElementById('login-overlay').classList.add('hidden');
        this.showToast(`Bem-vindo, ${driverData.name}!`);
        this.checkAuth(); 
    } catch(e) {
        console.error(e);
        this.showToast('Erro ao realizar login.', 'error');
    } finally {
        if(btn) {
            btn.innerHTML = oldHtml;
            btn.disabled = false;
        }
    }
  }"""
    
    content = re.sub(pattern_login_driver, new_login_driver, content)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def fix_gestor_theme():
    path = 'index.html'
    if not os.path.exists(path): return
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # 1. Remove profile theme UI
    content = re.sub(r'<div[^>]*>\s*<label[^>]*>Tema de Interface</label>.*?</div>', '', content, flags=re.DOTALL)
    
    # 2. Find "Nenhuma ocorrência ativa" or similar and replace with paintbrush
    content = re.sub(r'<span class="text-xs text-slate-500 font-bold hidden md:inline-block uppercase tracking-widest">Nenhuma ocorrência\w*\s*\w*</span>', '', content, flags=re.IGNORECASE)
    content = re.sub(r'<span class="text-xs font-bold text-slate-500 uppercase tracking-widest bg-slate-900 px-3 py-1 rounded-full hidden md:block">Nenhuma Ocorrência Ativa</span>', '', content, flags=re.IGNORECASE)
    
    # add theme icon to header
    brush_btn = '<button onclick="document.getElementById(\'theme-modal\').classList.remove(\'hidden\')" class="p-2 text-slate-400 hover:text-white transition-colors" title="Tema de Interface"><i data-lucide="paintbrush" class="w-5 h-5"></i></button>'
    
    if brush_btn not in content:
        # inject near the notification bell
        content = content.replace('<button class="p-2', brush_btn + '\n<button class="p-2', 1)
        
    # inject theme modal
    theme_modal = """
    <div id="theme-modal" class="hidden fixed inset-0 z-[100] bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
    <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6 w-full max-w-sm">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-white font-bold text-lg">Escolher Tema</h2>
        <button onclick="document.getElementById('theme-modal').classList.add('hidden')" class="text-slate-400 hover:text-white"><i data-lucide="x" class="w-5 h-5"></i></button>
      </div>
      <div class="grid grid-cols-2 gap-4">
         <button onclick="document.body.classList.remove('light-mode'); document.getElementById('theme-modal').classList.add('hidden'); App.showToast('Modo Escuro Ativado');" class="bg-slate-800 border border-slate-700 rounded-xl p-4 text-center hover:border-blue-500 transition-all">
           <i data-lucide="moon" class="w-6 h-6 text-blue-400 mx-auto mb-2"></i>
           <span class="text-white text-sm font-bold">Escuro</span>
         </button>
         <button onclick="document.body.classList.add('light-mode'); document.getElementById('theme-modal').classList.add('hidden'); App.showToast('Modo Claro Ativado');" class="bg-slate-100 border border-slate-300 rounded-xl p-4 text-center hover:border-blue-500 transition-all">
           <i data-lucide="sun" class="w-6 h-6 text-yellow-500 mx-auto mb-2"></i>
           <span class="text-slate-900 text-sm font-bold">Claro</span>
         </button>
      </div>
    </div>
   </div>
   """
    if 'theme-modal' not in content:
        content = content.replace('</body>', theme_modal + '\n</body>')
        
    # inject CSS for light mode
    light_mode_css = """
    <style>
    body.light-mode { background: #f8fafc; color: #0f172a; }
    body.light-mode .bg-slate-950 { background-color: #f1f5f9 !important; }
    body.light-mode .bg-slate-900 { background-color: #ffffff !important; border-color: #e2e8f0 !important; }
    body.light-mode .text-slate-400 { color: #64748b !important; }
    body.light-mode .text-white { color: #0f172a !important; }
    body.light-mode .border-slate-800, body.light-mode .border-slate-700 { border-color: #e2e8f0 !important; }
    </style>
    """
    if 'body.light-mode' not in content:
        content = content.replace('</head>', light_mode_css + '\n</head>')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
        
    # Apply to www/index.html as well
    if os.path.exists('www/index.html'):
        with open('www/index.html', 'w', encoding='utf-8') as f:
            f.write(content)


if __name__ == "__main__":
    fix_cpf_mask('index.html')
    fix_cpf_mask('www/index.html')
    fix_cpf_mask('motorista.html')
    
    fix_toast_zindex('www/js/app.js')
    fix_toast_zindex('www/js/app_motorista.js')
    
    fix_landing_page()
    fix_gestor_isolation()
    fix_motorista_logic()
    fix_gestor_theme()
    
    print("All fixes applied successfully.")
