import sys
import re

def patch_index_html():
    file_path = r"c:\Users\giova\.gemini\antigravity\scratch\general-app\index.html"
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Add CNPJ to login fields
    old_login_role = """          <div>
            <label class="block text-xs font-bold text-slate-300 mb-1">Cargo</label>
            <input type="text" id="login-role" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-blue-500 transition-all placeholder:text-slate-600" placeholder="Ex: Gestor de Frota" />
          </div>"""
    
    new_login_role = """          <div>
            <label class="block text-xs font-bold text-slate-300 mb-1">Cargo</label>
            <input type="text" id="login-role" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-blue-500 transition-all placeholder:text-slate-600" placeholder="Ex: Gestor de Frota" />
          </div>
          <div>
            <label class="block text-xs font-bold text-slate-300 mb-1">CNPJ da Empresa</label>
            <input type="text" id="login-cnpj" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-blue-500 transition-all placeholder:text-slate-600" placeholder="00.000.000/0001-00" oninput="this.value = this.value.replace(/[^0-9]/g, '').replace(/^(\\d{2})(\\d{3})(\\d{3})(\\d{4})(\\d{2}).*/, '$1.$2.$3/$4-$5');" />
          </div>"""
    content = content.replace(old_login_role, new_login_role)

    # 2. Add CNPJ to Profile Modal
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

    # 3. Remove "Perigo!" button
    perigo_btn_regex = re.compile(r'<!-- Botão de Reporte Rápido -->.*?<button onclick="App\.submitQuickReport\(\)".*?<span class="inline">Perigo!</span>.*?^\s*</button>', re.DOTALL | re.MULTILINE)
    content = perigo_btn_regex.sub('', content)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

def patch_app_js():
    file_path = r"c:\Users\giova\.gemini\antigravity\scratch\general-app\js\app.js"
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Read login-cnpj in login()
    old_login = """    const name = document.getElementById('login-name') ? document.getElementById('login-name').value : '';
    const company = document.getElementById('login-company') ? document.getElementById('login-company').value : '';
    const role = document.getElementById('login-role') ? document.getElementById('login-role').value : '';"""
    
    new_login = """    const name = document.getElementById('login-name') ? document.getElementById('login-name').value.trim() : '';
    const company = document.getElementById('login-company') ? document.getElementById('login-company').value.trim() : '';
    const role = document.getElementById('login-role') ? document.getElementById('login-role').value.trim() : '';
    const cnpj = document.getElementById('login-cnpj') ? document.getElementById('login-cnpj').value.trim() : '';"""
    content = content.replace(old_login, new_login)
    
    # 2. Update appState.currentUser assignment
    old_user_assign = """appState.currentUser = { id, name, company, role, provider: 'manual' };"""
    new_user_assign = """appState.currentUser = { id, name, company, role, companyCnpj: cnpj, provider: 'manual' };"""
    content = content.replace(old_user_assign, new_user_assign)

    # 3. Update profile functions
    old_update_ui = """    setVal('profile-company', company);
    setVal('profile-role', role);"""
    new_update_ui = """    setVal('profile-company', company);
    setVal('profile-role', role);
    setVal('profile-cnpj', appState.currentUser.companyCnpj);"""
    content = content.replace(old_update_ui, new_update_ui)
    
    old_save_profile = """    appState.currentUser.company = getVal('profile-company');
    appState.currentUser.role = getVal('profile-role');"""
    new_save_profile = """    appState.currentUser.company = getVal('profile-company');
    appState.currentUser.role = getVal('profile-role');
    appState.currentUser.companyCnpj = getVal('profile-cnpj');"""
    content = content.replace(old_save_profile, new_save_profile)

    # 4. Remove "Avaliar Rota" button from renderSavedPlans
    avaliar_btn_regex = re.compile(r'<button onclick="App\.openRouteEvaluation\([^)]+\)" class="[^"]*Avaliar Rota[^<]*</button>', re.DOTALL | re.IGNORECASE)
    content = avaliar_btn_regex.sub('', content)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    patch_index_html()
    patch_app_js()
    print("Patch 1 applied.")
