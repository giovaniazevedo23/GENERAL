import re

def patch_motorista_html():
    with open('motorista.html', 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()

    # 1. Replace feedback-route input with a select
    old_input = '<input type="text" id="feedback-route" placeholder="Ex: BR-116, SP-280..." class="w-full bg-slate-950 border border-slate-800 rounded-lg p-3 text-sm text-white" />'
    new_select = '<select id="feedback-route" class="w-full bg-slate-950 border border-slate-800 rounded-lg p-3 text-sm text-white"><option value="">Carregando planos...</option></select>'
    
    if old_input in html:
        html = html.replace(old_input, new_select)
        
    with open('motorista.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("motorista.html feedback-route patched.")

def patch_app_motorista_js():
    with open('js/app_motorista.js', 'r', encoding='utf-8', errors='ignore') as f:
        js = f.read()

    # 2. Add populateFeedbackRoutes method
    populate_logic = """
  populateFeedbackRoutes() {
      const select = document.getElementById('feedback-route');
      if (!select) return;
      if (!window.db) {
          select.innerHTML = '<option value="">Banco offline (digite manualmente)</option>';
          select.outerHTML = '<input type="text" id="feedback-route" placeholder="Digite a rota manualmente" class="w-full bg-slate-950 border border-slate-800 rounded-lg p-3 text-sm text-white" />';
          return;
      }
      
      select.innerHTML = '<option value="">Carregando rotas...</option>';
      window.db.collection('saved_plans').orderBy('createdAt', 'desc').limit(20).get().then(snapshot => {
          if (snapshot.empty) {
              select.innerHTML = '<option value="">Nenhuma rota encontrada.</option>';
              return;
          }
          let html = '<option value="">Selecione um Plano salvo...</option>';
          snapshot.forEach(doc => {
              const data = doc.data();
              const routeName = `${data.origin || 'Origem'} \u2192 ${data.destination || 'Destino'} (${data.company || 'Geral'})`;
              html += `<option value="${doc.id}">${routeName}</option>`;
          });
          select.innerHTML = html;
      }).catch(err => {
          console.error("Erro carregando rotas para avaliacao", err);
          select.innerHTML = '<option value="">Erro ao carregar. Digite a rota.</option>';
      });
  },
"""

    if 'populateFeedbackRoutes()' not in js:
        js = js.replace('login() {', populate_logic + '\nlogin() {')

    # 3. Call populateFeedbackRoutes on switchTab('feedback')
    # Let's find switchTab logic
    # In app_motorista.js, it's switchTab(tabId)
    switch_tab_hook = """
      if (tabId === 'feedback') {
          if (this.populateFeedbackRoutes) this.populateFeedbackRoutes();
      }
"""
    if 'this.populateFeedbackRoutes()' not in js:
        # inject it inside switchTab
        idx = js.find('switchTab(tabId) {')
        if idx != -1:
            idx = js.find('{', idx) + 1
            js = js[:idx] + switch_tab_hook + js[idx:]

    with open('js/app_motorista.js', 'w', encoding='utf-8') as f:
        f.write(js)
    
    print("app_motorista.js populateFeedbackRoutes patched.")

if __name__ == '__main__':
    patch_motorista_html()
    patch_app_motorista_js()
