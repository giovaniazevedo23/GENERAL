import os

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# keep up to line 1226 (index 1225)
good_lines = lines[:1226]

rest_of_file = """            </div>
            <div>
              <label class="block text-xs font-bold text-slate-300 mb-1">Destinatário</label>
              <input type="text" id="comm-target" placeholder="Ex: PRF, Seguradora, Cliente..." class="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-slate-200 focus:border-blue-500 outline-none" />
            </div>
            <div>
              <label class="block text-xs font-bold text-slate-300 mb-1">Detalhes (Opcional)</label>
              <textarea id="comm-details" rows="2" placeholder="Ex: Ligar para informar tombamento..." class="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-slate-200 focus:border-blue-500 outline-none"></textarea>
            </div>
          </div>
          <div class="p-4 border-t border-slate-800 bg-slate-950/50 flex justify-end gap-3">
            <button type="button" onclick="App.closeNewCommunicationModal()" class="px-4 py-2 rounded-xl text-xs font-bold text-slate-300 hover:bg-slate-800 transition-all">Cancelar</button>
            <button type="button" onclick="App.saveNewCommunication()" class="bg-blue-600 hover:bg-blue-500 text-white px-5 py-2 rounded-xl text-xs font-bold shadow-md transition-all flex items-center gap-2">
              <i data-lucide="plus" class="w-4 h-4"></i> Adicionar
            </button>
          </div>
        </div>
      </div>

  <!-- MOCK GOOGLE LOGIN MODAL -->
  <div id="mock-google-login-modal" class="hidden fixed inset-0 z-[100] bg-black/80 backdrop-blur-sm items-center justify-center p-4 transition-opacity duration-300">
    <div class="bg-white p-8 rounded-3xl shadow-2xl max-w-sm w-full space-y-6 relative overflow-hidden">
      <div class="absolute -top-10 -right-10 w-32 h-32 bg-blue-500/10 rounded-full blur-2xl"></div>
      <div class="flex flex-col items-center justify-center text-center space-y-4 relative z-10">
        <svg class="w-10 h-10" viewBox="0 0 24 24">
          <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
          <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
          <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/>
          <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/>
        </svg>
        <div>
          <h3 class="text-xl font-medium text-slate-900">Fazer login</h3>
          <p class="text-sm text-slate-600 mt-1">Prosseguir para o GENERAL App</p>
        </div>
      </div>
      <div id="google-account-list" class="space-y-3 relative z-10">
        <button onclick="App.confirmMockGoogleLogin('Sua Conta Padrão', 'usuario@gmail.com')" class="w-full flex items-center gap-4 p-3 rounded-xl hover:bg-slate-50 transition-all border border-transparent hover:border-slate-200">
          <div class="w-10 h-10 rounded-full bg-blue-600 text-white font-bold flex items-center justify-center text-lg shadow-inner">U</div>
          <div class="text-left flex-1">
            <p class="text-sm font-bold text-slate-900">Sua Conta Padrão</p>
            <p class="text-xs text-slate-500">usuario@gmail.com</p>
          </div>
        </button>
        <button onclick="App.showMockGoogleOtherAccount()" class="w-full flex items-center gap-4 p-3 rounded-xl hover:bg-slate-50 transition-all border border-transparent hover:border-slate-200 group">
          <div class="w-10 h-10 rounded-full bg-slate-100 text-slate-600 flex items-center justify-center group-hover:bg-slate-200 transition-colors">
            <i data-lucide="user-plus" class="w-5 h-5"></i>
          </div>
          <div class="text-left">
            <p class="text-sm font-bold text-slate-900">Usar outra conta</p>
          </div>
        </button>
      </div>
      <div id="google-other-account-form" class="hidden flex-col gap-4 relative z-10">
        <div>
          <input type="email" id="mock-google-email" placeholder="E-mail ou telefone" class="w-full px-4 py-3 border border-slate-300 rounded-lg focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none text-sm text-slate-900 transition-all placeholder:text-slate-500" />
        </div>
        <div class="flex justify-end gap-3 mt-4">
          <button onclick="App.hideMockGoogleOtherAccount()" class="px-4 py-2 text-sm font-bold text-slate-600 hover:text-slate-900 hover:bg-slate-100 rounded-lg transition-all">Cancelar</button>
          <button onclick="App.confirmMockGoogleLoginCustom()" class="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white font-bold text-sm rounded-lg shadow-md transition-all">Avançar</button>
        </div>
      </div>
      <div id="google-verifying-spinner" class="hidden flex-col items-center justify-center py-6 relative z-10 space-y-4">
        <div class="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
        <p class="text-sm font-medium text-slate-600">Verificando informações...</p>
      </div>
      <button onclick="document.getElementById('mock-google-login-modal').classList.add('hidden'); document.getElementById('mock-google-login-modal').classList.remove('flex');" class="absolute top-4 right-4 text-slate-400 hover:text-slate-600 transition-colors z-20">
        <i data-lucide="x" class="w-5 h-5"></i>
      </button>
    </div>
  </div>

  <!-- Scripts Core -->
  <script src="js/state.js"></script>
  <script src="js/hazmat-db.js"></script>
  <script src="js/risk-engine.js"></script>
  
  <!-- IA e Planejamento -->
  <script src="js/ai-copilot.js"></script>
  <script src="js/ai-predictive.js"></script>
  <script src="js/logistics-planner.js"></script>
  
  <!-- Módulos Adicionais -->
  <script src="js/map.js"></script>
  <script src="js/notifications.js"></script>
  <script src="js/rca-investigation.js"></script>
  <script src="js/report-pdf.js"></script>
  <script src="js/transshipment.js"></script>
  
  <!-- Controlador Principal -->
  <script src="js/app.js"></script>
  <script src="js/pwa.js"></script>
</body>
</html>
"""

with open('index.html', 'w', encoding='utf-8') as f:
    f.writelines(good_lines)
    f.write(rest_of_file)
