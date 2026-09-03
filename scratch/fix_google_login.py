import sys
import re

def patch_index_html():
    file_path = r"c:\Users\giova\.gemini\antigravity\scratch\general-app\index.html"
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Add Google Meta tag and script
    if 'google-signin-client_id' not in content:
        head_insert = """  <!-- Google Auth Web -->
  <meta name="google-signin-client_id" content="148525185065-bqmkog5bfdj7ed9gol94d3d3mhfr6i8v.apps.googleusercontent.com">
  <script src="https://apis.google.com/js/platform.js" async defer></script>
  
  <!-- Tailwind CSS CDN -->"""
        content = content.replace("  <!-- Tailwind CSS CDN -->", head_insert)

    # 2. Add Complete Registration Modal
    if 'google-extra-modal' not in content:
        extra_modal = """
  <!-- MODAL COMPLETAR CADASTRO GOOGLE -->
  <div id="google-extra-modal" class="hidden fixed inset-0 z-[110] bg-slate-950/90 backdrop-blur-sm flex items-center justify-center p-4">
    <div class="bg-slate-900 border border-slate-800 p-8 rounded-2xl shadow-2xl max-w-sm w-full space-y-6">
      <div class="flex flex-col items-center justify-center text-center">
        <div class="w-16 h-16 bg-blue-500/20 text-blue-400 rounded-full flex items-center justify-center mb-3">
          <i data-lucide="building" class="w-8 h-8"></i>
        </div>
        <h3 class="text-xl font-bold text-white">Completar Cadastro</h3>
        <p class="text-xs text-slate-400 mt-1">Sua conta Google foi vinculada. Agora, precisamos dos dados da sua empresa.</p>
      </div>
      
      <div class="space-y-4">
        <div>
          <label class="block text-xs font-bold text-slate-300 mb-1">Empresa</label>
          <input type="text" id="google-extra-company" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-blue-500 transition-all placeholder:text-slate-600" placeholder="Ex: Transportes S.A." />
        </div>
        <div>
          <label class="block text-xs font-bold text-slate-300 mb-1">CNPJ da Empresa</label>
          <input type="text" id="google-extra-cnpj" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-blue-500 transition-all placeholder:text-slate-600" placeholder="00.000.000/0001-00" oninput="this.value = this.value.replace(/[^0-9]/g, '').replace(/^(\\d{2})(\\d{3})(\\d{3})(\\d{4})(\\d{2}).*/, '$1.$2.$3/$4-$5');" />
        </div>
        <div>
          <label class="block text-xs font-bold text-slate-300 mb-1">Cargo</label>
          <input type="text" id="google-extra-role" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-blue-500 transition-all placeholder:text-slate-600" placeholder="Ex: Gestor de Frota" />
        </div>
        <button onclick="App.submitGoogleExtraInfo()" class="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-2.5 rounded-xl shadow-lg shadow-blue-500/30 transition-all flex items-center justify-center gap-2 mt-2">
          Finalizar
        </button>
      </div>
    </div>
  </div>
"""
        # Insert before </body>
        content = content.replace("</body>", extra_modal + "\n</body>")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

def patch_app_js():
    file_path = r"c:\Users\giova\.gemini\antigravity\scratch\general-app\js\app.js"
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Update loginWithGoogle in app.js
    old_google_check = """      if (!window.Capacitor || !window.Capacitor.Plugins.GoogleAuth) {
        this.showToast('Plugin GoogleAuth não encontrado ou rodando fora do Capacitor.');
        return;
      }"""
      
    new_google_check = """      if (!window.Capacitor || !window.Capacitor.Plugins.GoogleAuth) {
        // Fallback for Web if Plugin is missing but we want to simulate
        console.warn('Plugin GoogleAuth missing. Simulando no Web.');
      }"""
    content = content.replace(old_google_check, new_google_check)

    old_login_google_end = """      appState.currentUser = googleUser;
      localStorage.setItem('general_user', JSON.stringify(googleUser));
      this.checkAuth();
      this.showToast(`ðŸ”‘ Bem-vindo(a) via Google, ${googleUser.name}!`);"""
      
    new_login_google_end = """      // Guardar temporariamente e pedir dados extras
      window.tempGoogleUser = googleUser;
      
      // Mostrar Modal
      const modal = document.getElementById('google-extra-modal');
      if (modal) {
         modal.classList.remove('hidden');
         if(window.lucide) window.lucide.createIcons();
      } else {
         // Fallback if modal doesn't exist
         appState.currentUser = googleUser;
         localStorage.setItem('general_user', JSON.stringify(googleUser));
         this.checkAuth();
      }"""
    # Note: Using regex or split might be safer due to the special characters in toast.
    
    # We will find the assignment to appState.currentUser and replace to the end of the try block.
    # Actually, simpler regex:
    content = re.sub(r"appState\.currentUser = googleUser;.*?this\.showToast\([^)]+\);", new_login_google_end, content, flags=re.DOTALL)

    # 2. Add submitGoogleExtraInfo function
    additional_code = """
  submitGoogleExtraInfo() {
    const company = document.getElementById('google-extra-company')?.value.trim();
    const cnpj = document.getElementById('google-extra-cnpj')?.value.trim();
    const role = document.getElementById('google-extra-role')?.value.trim();
    
    if (!company || !cnpj || !role) {
      this.showToast('Por favor, preencha todos os campos da empresa.');
      return;
    }
    
    if (window.tempGoogleUser) {
       window.tempGoogleUser.company = company;
       window.tempGoogleUser.companyCnpj = cnpj;
       window.tempGoogleUser.role = role;
       
       appState.currentUser = window.tempGoogleUser;
       localStorage.setItem('general_user', JSON.stringify(window.tempGoogleUser));
       
       document.getElementById('google-extra-modal').classList.add('hidden');
       this.checkAuth();
       this.showToast(`ðŸ”‘ Bem-vindo(a) via Google, ${window.tempGoogleUser.name}!`);
    }
  },
"""
    # Insert before the last closing brace
    last_brace = content.rfind('}')
    if last_brace != -1:
        content = content[:last_brace] + additional_code + "\n}"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    patch_index_html()
    patch_app_js()
    print("Google Login Fix Applied.")
