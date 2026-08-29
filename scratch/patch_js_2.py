import sys
import re

file_path = "js/app.js"
try:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
except UnicodeDecodeError:
    with open(file_path, "r", encoding="latin-1") as f:
        content = f.read()

# 1. Add methods
init_re = re.compile(r'(init\(\) \{.*?\n  \},)', re.DOTALL)
match_init = init_re.search(content)

new_methods = '''

  populateIncidentSelectors() {
    const incidents = (window.appState && appState.incidents) ? appState.incidents.filter(i => i.status !== 'CONCLUIDA') : [];
    const createOptions = (selectId) => {
      const sel = document.getElementById(selectId);
      if (!sel) return;
      sel.innerHTML = '<option value="">Selecione uma ocorrência ativa...</option>';
      incidents.forEach(inc => {
        sel.innerHTML += `<option value="${inc.id}">${inc.id} - ${inc.title}</option>`;
      });
      if (appState && appState.currentIncidentId) {
        sel.value = appState.currentIncidentId;
      }
    };
    createOptions('ishikawa-incident-select');
    createOptions('dossier-incident-select');
    createOptions('reverse-incident-select');
  },

  handleIshikawaIncidentSelect() {
    const val = document.getElementById('ishikawa-incident-select').value;
    if (val && window.appState) {
      appState.setCurrentIncident(val);
      // view is updated via subscribe
    }
  },
  
  handleDossierIncidentSelect() {
    const val = document.getElementById('dossier-incident-select').value;
    if (val && window.appState) {
      appState.setCurrentIncident(val);
    }
  },

  handleReverseIncidentSelect() {
    const val = document.getElementById('reverse-incident-select').value;
    const form = document.getElementById('reverse-logistics-form');
    if (val && window.appState) {
      appState.setCurrentIncident(val);
      if (form) form.classList.remove('hidden');
    } else {
      if (form) form.classList.add('hidden');
    }
  },

  submitReverseLogistics() {
    if (!window.appState) return;
    const currentInc = appState.getCurrentIncident();
    if (!currentInc) return;
    
    const statusEl = document.getElementById('reverse-status');
    const companyEl = document.getElementById('reverse-company');
    
    if (!statusEl || !companyEl) return;
    
    const reverseData = { 
        status: statusEl.value, 
        company: companyEl.value, 
        processedAt: new Date().toISOString() 
    };
    appState.updateCurrentIncident({ reverseLogistics: reverseData });
    
    this.showToast('Logística reversa processada com sucesso! Histórico atualizado.', 'success');
  },

'''

if match_init:
    content = content[:match_init.end()] + new_methods + content[match_init.end():]

# 2. Call populateIncidentSelectors in switchTab
switchTab_re = re.compile(r'(switchTab\(tabId\) \{.*?)(if \(tabId === \'monitoring\'\))', re.DOTALL)
match_switch = switchTab_re.search(content)
if match_switch:
    content = content[:match_switch.start(2)] + "if (['investigation', 'dossier', 'reverse-logistics'].includes(tabId)) { this.populateIncidentSelectors(); }\n    " + content[match_switch.start(2):]
else:
    # Fallback
    st_re2 = re.compile(r'(switchTab\(tabId\) \{.*?this\.currentTab = tabId;)', re.DOTALL)
    m_st2 = st_re2.search(content)
    if m_st2:
        content = content[:m_st2.end()] + "\n    if (['investigation', 'dossier', 'reverse-logistics'].includes(tabId)) { this.populateIncidentSelectors(); }" + content[m_st2.end():]

# 3. Patch copilot send
copilot_re = re.compile(r'const answer = await AICopilotEngine\.askCopilot\(text, inc\);', re.DOTALL)
fake_copilot = "const answer = `Olá, sou o General. Estou indisponível no momento por falta de inteligência artificial.<br><br>Por favor, entre em contato com a central de ajuda:<br>- E-mail: suporte@general.com<br>- Tel: (11) 99999-9999`;"
content = copilot_re.sub(fake_copilot, content)

# 4. Patch renderHistoryTab
history_re = re.compile(r'(<h3 class="font-bold text-white text-base leading-snug mb-2">\$\{inc\.title\}</h3>)', re.DOTALL)

badge_html = r'''${inc.reverseLogistics ? `
          <div class="mb-3 bg-emerald-950/40 border border-emerald-500/50 rounded-lg p-2.5 flex items-start gap-2 shadow-inner">
            <i data-lucide="recycle" class="w-4 h-4 text-emerald-400 mt-0.5"></i>
            <div>
              <span class="text-xs font-bold text-emerald-300 block">Cliente desistiu, produtos reaproveitados</span>
              <span class="text-[10px] text-emerald-500">Parceiro de reciclagem/recondicionamento: <b>${inc.reverseLogistics.company}</b></span>
            </div>
          </div>
          ` : ''}
          \1'''
content = history_re.sub(badge_html, content)

try:
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
except Exception:
    with open(file_path, "w", encoding="latin-1") as f:
        f.write(content)

print("js/app.js successfully patched.")
