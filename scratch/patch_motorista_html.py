import re

with open('motorista.html', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# 1. Update the Login UI
# The current login form has an input with id="login-id"
# We will replace it with a robust UI that lets the user choose their role.
login_replacement = """
        <div id="login-form-motorista" class="space-y-4 w-full">
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
          
          <div id="field-driver-cnpj" class="hidden">
            <label class="block text-sm font-bold text-slate-300 mb-1">CNPJ da Empresa Contratante</label>
            <input type="text" id="login-cnpj" class="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-blue-500 transition-colors font-mono" placeholder="00.000.000/0000-00">
          </div>
          
          <button type="button" id="btn-action-login-motorista" onclick="App.loginDriver()" class="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-3 rounded-xl shadow-lg shadow-blue-500/30 transition-all flex items-center justify-center gap-2 mt-6">
            Acessar Sistema <i data-lucide="arrow-right" class="w-4 h-4"></i>
          </button>
        </div>
"""

# Replace the existing login form inside motorista.html
# We'll use regex to replace from <div id="login-form-motorista"... to the closing </div> of btn-action-login-motorista
if 'id="login-cpf"' not in content:
    content = re.sub(
        r'<div id="login-form-motorista".*?</button>\s*</div>',
        login_replacement,
        content,
        flags=re.DOTALL
    )

# 2. Add Camera UI in Route View
# There is likely a button for route actions. We will insert the camera container at the top right of the route view
camera_ui = """
  <!-- Câmera do Motorista (Picture in Picture) -->
  <div id="driver-camera-container" class="fixed top-20 right-4 w-28 h-36 bg-black rounded-xl border-2 border-blue-500 shadow-2xl overflow-hidden z-[60] hidden flex-col transition-all cursor-move">
    <video id="driver-selfie-video" class="w-full h-full object-cover" autoplay playsinline muted></video>
    <div class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 to-transparent p-1 flex items-center justify-between">
      <div class="flex items-center gap-1 text-[8px] font-bold text-white">
        <div class="w-1.5 h-1.5 rounded-full bg-rose-500 animate-pulse"></div> REC
      </div>
      <span id="driver-local-bpm" class="text-[9px] font-bold text-rose-400">-- bpm</span>
    </div>
  </div>
"""

if 'id="driver-camera-container"' not in content:
    # Just insert it before </body> or inside a main container
    content = content.replace('</body>', camera_ui + '\n</body>')
    
# We also need a button to start the camera in the route view. 
# Let's add it to a floating action button or route info section.
start_cam_btn = """
        <!-- Start Camera Button -->
        <button id="btn-start-camera" onclick="App.startDriverCamera()" class="mt-4 w-full bg-emerald-600 hover:bg-emerald-500 text-white font-bold py-3 rounded-xl shadow-lg shadow-emerald-500/30 transition-all flex items-center justify-center gap-2">
            <i data-lucide="camera" class="w-5 h-5"></i>
            Iniciar Gravação da Rota
        </button>
"""

# Let's just insert this button right below the "Iniciar Deslocamento" button or wherever route details are shown.
if 'id="btn-start-camera"' not in content:
    # Look for button that starts route or an active route panel
    # We will just append it into "active-route-panel" if it exists, or somewhere safe
    if 'id="active-route-panel"' in content:
        content = re.sub(
            r'(<div id="active-route-panel"[^>]*>.*?(?=<div class="mt-4))',
            r'\1\n' + start_cam_btn,
            content,
            flags=re.DOTALL
        )
    else:
        # Just append it to the body, fixed at bottom for demo
        float_btn = start_cam_btn.replace('mt-4 w-full', 'fixed bottom-24 left-4 right-4 z-50 hidden')
        float_btn = float_btn.replace('id="btn-start-camera"', 'id="btn-start-camera-float"')
        content = content.replace('</body>', float_btn + '\n</body>')

with open('motorista.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("motorista.html patched with new Login and Camera UI successfully.")
