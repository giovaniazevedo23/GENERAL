# -*- coding: utf-8 -*-
html_path = r'C:\Users\giova\.gemini\antigravity\scratch\gestor-app\index.html'

with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

view_html = '''
    <!-- VIEW: CADASTRO DE MOTORISTAS VINCULADOS -->
    <div id="view-driver-registration" class="view hidden space-y-6">
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
            <input type="text" id="reg-driver-cpf" required oninput="let v = this.value.replace(/\\D/g, ''); v = v.replace(/(\\d{3})(\\d)/, '.'); v = v.replace(/(\\d{3})(\\d)/, '.'); v = v.replace(/(\\d{3})(\\d{1,2})$/, '-'); this.value = v;" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2 text-white outline-none focus:border-blue-500 font-mono" placeholder="000.000.000-00" />
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

if 'id="view-driver-registration"' not in html_content:
    if 'id="view-planner"' in html_content:
        html_content = html_content.replace('<div id="view-planner"', view_html + '\n    <div id="view-planner"')
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print("Injected view successfully.")
    else:
        print("view-planner not found!")
else:
    print("view-driver-registration already exists.")
