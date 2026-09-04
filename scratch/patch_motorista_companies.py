import re

def patch_html():
    with open('../motorista.html', 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()
    
    # Add onblur to CNPJ input
    if 'onblur="App.fetchCompanyByCnpj(this.value)"' not in html:
        html = html.replace('id="motorista-cnpj"', 'id="motorista-cnpj" onblur="if(window.App) App.fetchCompanyByCnpj(this.value)"')

    with open('../motorista.html', 'w', encoding='utf-8') as f:
        f.write(html)

def patch_js():
    with open('../js/app_motorista.js', 'r', encoding='utf-8', errors='ignore') as f:
        js = f.read()

    fetch_logic = """
  fetchCompanyByCnpj(cnpj) {
    if (!cnpj || cnpj.length < 18) return;
    if (!window.db) return;
    
    // Mostra feedback de carregamento
    const companyInput = document.getElementById('motorista-company');
    if (companyInput) {
        companyInput.value = 'Buscando empresa...';
        companyInput.disabled = true;
    }
    
    window.db.collection('companies').where('cnpj', '==', cnpj).get()
      .then(snapshot => {
          if (!snapshot.empty) {
              const data = snapshot.docs[0].data();
              if (companyInput && data.name) {
                  companyInput.value = data.name;
                  this.showToast('Empresa encontrada e preenchida automaticamente.');
              }
          } else {
              if (companyInput) {
                  companyInput.value = '';
                  companyInput.disabled = false;
                  this.showToast('Empresa no encontrada. Preencha manualmente.');
              }
          }
      })
      .catch(err => {
          console.error("Erro ao buscar empresa:", err);
          if (companyInput) {
              companyInput.value = '';
              companyInput.disabled = false;
          }
      });
  },
"""
    if 'fetchCompanyByCnpj' not in js:
        # Insert it before login()
        js = js.replace('login() {', fetch_logic + 'login() {')

    with open('../js/app_motorista.js', 'w', encoding='utf-8') as f:
        f.write(js)

if __name__ == '__main__':
    patch_html()
    patch_js()
    print("CNPJ fetch logic patched.")
