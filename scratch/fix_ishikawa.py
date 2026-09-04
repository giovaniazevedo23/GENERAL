import re

def fix_ishikawa():
    # 1. Fix app.js renderInvestigationTab
    with open('../js/app.js', 'r', encoding='utf-8', errors='ignore') as f:
        js = f.read()
    
    # We must replace renderInvestigationTab() so that it renders even if !inc
    start_idx = js.find('renderInvestigationTab() {')
    end_idx = js.find('},', start_idx)
    
    new_render = """renderInvestigationTab() {
    const inc = appState.getCurrentIncident() || {};
    
    // Tratamento seguro para RCA
    const rca = inc.rca || { ishikawa: {}, fiveWhys: ["", "", "", "", ""] };
    
    const ishikawaContainer = document.getElementById('ishikawa-interactive-container');
    const whysContainer = document.getElementById('five-whys-interactive-container');
    
    if (ishikawaContainer && window.RCAInvestigationModule) ishikawaContainer.innerHTML = RCAInvestigationModule.renderIshikawaDiagram(rca.ishikawa);
    if (whysContainer && window.RCAInvestigationModule) whysContainer.innerHTML = RCAInvestigationModule.renderFiveWhys(rca.fiveWhys);
  """
    
    if start_idx != -1:
        js = js[:start_idx] + new_render + js[end_idx:]
        
    with open('../js/app.js', 'w', encoding='utf-8') as f:
        f.write(js)
    
    # 2. Fix index.html encoding for Ishikawa and 5 Porquês
    with open('../index.html', 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()
    
    # Precise replacements:
    html = html.replace('?rvore dos 5 Porqu\ufffds', 'Árvore dos 5 Porquês')
    html = html.replace('?rvore dos 5 Porqus', 'Árvore dos 5 Porquês')
    html = html.replace('\ufffd\ufffd?rvore', 'Árvore')
    html = html.replace('\ufffd?rvore', 'Árvore')
    html = html.replace('Ê?RVORE', 'ÁRVORE')
    html = html.replace('Ê?rvore', 'Árvore')
    
    html = html.replace('Investigao de Acidente', 'Investigação de Acidente')
    html = html.replace('Diagrama de Ishikawa (6M) & 5 Porqus', 'Diagrama de Ishikawa (6M) & 5 Porquês')
    html = html.replace('Investigao da Causa', 'Investigação da Causa')
    html = html.replace('Ocorrncia', 'Ocorrência')
    html = html.replace('Seleo', 'Seleção')
    html = html.replace('avaliao', 'avaliação')
    html = html.replace('Tcnicos', 'Técnicos')
    html = html.replace('Condio', 'Condição')
    html = html.replace('Segurana', 'Segurança')
    html = html.replace('Aplicvel', 'Aplicável')
    html = html.replace('escoriaes', 'escoriações')
    html = html.replace('Veculo', 'Veículo')
    html = html.replace('1 Porqu', '1º Porquê')
    html = html.replace('2 Porqu', '2º Porquê')
    html = html.replace('3 Porqu', '3º Porquê')
    html = html.replace('4 Porqu', '4º Porquê')
    html = html.replace('5 Porqu', '5º Porquê')
    
    with open('../index.html', 'w', encoding='utf-8') as f:
        f.write(html)
        
    print("Fixed Ishikawa rendering and encoding.")

if __name__ == '__main__':
    fix_ishikawa()
