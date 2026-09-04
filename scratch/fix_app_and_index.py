import re

def fix():
    # 1. Fix app.js
    with open('../js/app.js', 'r', encoding='utf-8', errors='ignore') as f:
        js = f.read()

    start_idx = js.find('renderInvestigationTab() {')
    # Find the next method (renderDossierTab) to know where renderInvestigationTab ends
    end_idx = js.find('renderDossierTab() {', start_idx)
    
    if start_idx != -1 and end_idx != -1:
        # We replace everything between start_idx and end_idx
        correct_render = """renderInvestigationTab() {
    const inc = appState.getCurrentIncident() || {};
    
    // Tratamento seguro para RCA
    const rca = inc.rca || { ishikawa: {}, fiveWhys: ["", "", "", "", ""] };
    
    const ishikawaContainer = document.getElementById('ishikawa-interactive-container');
    const whysContainer = document.getElementById('five-whys-interactive-container');
    
    if (ishikawaContainer && window.RCAInvestigationModule) ishikawaContainer.innerHTML = RCAInvestigationModule.renderIshikawaDiagram(rca.ishikawa);
    if (whysContainer && window.RCAInvestigationModule) whysContainer.innerHTML = RCAInvestigationModule.renderFiveWhys(rca.fiveWhys);
  },

  """
        js = js[:start_idx] + correct_render + js[end_idx:]
        
        with open('../js/app.js', 'w', encoding='utf-8') as f:
            f.write(js)
        print("Fixed app.js syntax error.")
    else:
        print("Could not find boundaries in app.js")

    # 2. Fix index.html
    with open('../index.html', 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()
        
    html = html.replace('Ê?RVORE DOS 5º PORQUÊÊS', 'ÁRVORE DOS 5 PORQUÊS')
    html = html.replace('Ê?rvore dos 5º Porquêês', 'Árvore dos 5 Porquês')
    html = html.replace('?rvore dos 5 Porquês', 'Árvore dos 5 Porquês')
    html = html.replace('Investigação de Acidente — Diagrama de Ishikawa (6M) & 5º Porquêês', 'Investigação de Acidente — Diagrama de Ishikawa (6M) & 5 Porquês')
    html = html.replace('Os 5º Porquêês', 'Os 5 Porquês')
    html = html.replace('5º Porquêês', '5 Porquês')
    html = html.replace('Ê?RVORE', 'ÁRVORE')
    html = html.replace('Ê?rvore', 'Árvore')
    
    with open('../index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Fixed index.html encoding.")

if __name__ == '__main__':
    fix()
