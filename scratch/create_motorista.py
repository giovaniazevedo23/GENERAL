import os
import re

def create_motorista():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # We want to change the title
    content = content.replace('<title>GENERAL', '<title>Motorista - GENERAL')

    # Change the script source from app.js to app_motorista.js
    content = content.replace('<script src="js/app.js"></script>', '<script src="js/app_motorista.js"></script>')

    # In the login overlay, change the login fields
    # We will replace the entire login-form div content
    login_form_match = re.search(r'<div id="login-form".*?>(.*?)</div>\s*</div>\s*</div>\s*<!-- TOP HEADER', content, re.DOTALL)
    
    if login_form_match:
        login_form_html = """
        <div id="login-form-motorista" class="space-y-4 w-full">
          <div>
            <label class="block text-xs font-bold text-slate-300 mb-1">Seu Nome</label>
            <input type="text" id="motorista-name" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-slate-200 font-mono focus:border-blue-500 outline-none transition-all" placeholder="Digite seu nome" />
          </div>

          <div class="mt-4">
            <label class="block text-xs font-bold text-slate-300 mb-1">Empresa Logística</label>
            <!-- Será preenchido via Firebase dinamicamente -->
            <select id="motorista-company" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-slate-200 font-mono focus:border-blue-500 outline-none transition-all">
               <option value="">Carregando empresas...</option>
            </select>
          </div>
          
          <button type="button" id="btn-action-login-motorista" class="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-2.5 rounded-xl shadow-lg shadow-blue-500/30 transition-all flex items-center justify-center gap-2 mt-6">
            <span>Entrar</span>
            <i data-lucide="arrow-right" class="w-4 h-4"></i>
          </button>
        </div>
        """
        content = content[:login_form_match.start(1)] + login_form_html + content[login_form_match.end(1):]

    # Hide the tabs in the login overlay
    content = content.replace('<div id="login-tabs"', '<div id="login-tabs" class="hidden"')
    content = content.replace('<p class="text-xs text-slate-400 mt-1">Identifique-se para acessar o painel de crise e auditoria.</p>', '<p class="text-xs text-slate-400 mt-1">Acesso exclusivo para motoristas.</p>')

    # Hide the sidebar for driver
    content = content.replace('<aside class="no-print hidden lg:flex', '<aside class="no-print hidden') # completely hide sidebar

    # Hide all views EXCEPT view-monitoring by defaulting view-monitoring to active
    content = content.replace('<div id="view-dashboard" class="tab-view space-y-6">', '<div id="view-dashboard" class="tab-view hidden space-y-6">')
    content = content.replace('<div id="view-monitoring" class="tab-view hidden space-y-6">', '<div id="view-monitoring" class="tab-view space-y-6">')
    
    # Write to motorista.html
    with open('motorista.html', 'w', encoding='utf-8') as f:
        f.write(content)

    print("motorista.html created successfully.")

if __name__ == '__main__':
    create_motorista()
