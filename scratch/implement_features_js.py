import sys
import re

file_path = "js/app.js"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add new methods to App object. We will just insert them right after `init() { ... },`
init_re = re.compile(r'(init\(\) \{.*?\n  \},)', re.DOTALL)
match_init = init_re.search(content)

new_methods = '''

  handleEventTypeChange(selectElement) {
    const customInput = document.getElementById('customEventType');
    if (customInput) {
      if (selectElement.value === 'Outros') {
        customInput.classList.remove('hidden');
        customInput.required = true;
      } else {
        customInput.classList.add('hidden');
        customInput.required = false;
        customInput.value = '';
      }
    }
  },

  loadCustomEventTypes() {
    try {
      const customEvents = JSON.parse(localStorage.getItem('GENERAL_CUSTOM_EVENTS') || '[]');
      const selectElement = document.getElementById('eventTypeSelect');
      if (selectElement && customEvents.length > 0) {
        const options = Array.from(selectElement.options);
        const outrosIndex = options.findIndex(opt => opt.value === 'Outros');
        if (outrosIndex > -1) {
          customEvents.forEach(evt => {
            if (!Array.from(selectElement.options).find(o => o.value === evt)) {
               const newOption = new Option(evt, evt);
               selectElement.insertBefore(newOption, selectElement.options[outrosIndex]);
            }
          });
        }
      }
    } catch(e) {
      console.error(e);
    }
  },

  renderIndicatorsTab() {
    if (!window.appState) return;
    const incidents = appState.incidents || [];
    const totalIncidents = incidents.length;
    
    let totalPlans = 0;
    try {
      const savedPlans = JSON.parse(localStorage.getItem('general_saved_plans') || '[]');
      totalPlans = savedPlans.length;
    } catch(e) {}

    const freq = totalPlans > 0 ? ((totalIncidents / totalPlans) * 100).toFixed(1) : (totalIncidents * 10).toFixed(1);
    
    let totalCost = 0;
    let criticalCount = 0;
    let highCount = 0;
    let medCount = 0;

    let dmgTotal = 0;
    let dmgPartial = 0;
    let dmgNone = 0;

    let totalDowntimeHours = 0;
    let affectedDeliveries = 0;

    incidents.forEach(inc => {
      totalCost += Number(inc.cargoValue) || 0;

      if (inc.severity === 'CRITICO' || inc.severity === 'FATALIDADE' || inc.driverStatus === 'FATALIDADE') {
        criticalCount++;
      } else if (inc.severity === 'ALTO' || inc.driverStatus === 'FERIDO_GRAVE') {
        highCount++;
      } else {
        medCount++;
      }

      if (inc.damageCondition === 'TOTAL' || inc.damageCondition === 'PERDA_TOTAL') {
        dmgTotal++;
      } else if (inc.damageCondition === 'PARCIAL' || inc.damageCondition === 'PERDA_PARCIAL_VAZAMENTO') {
        dmgPartial++;
      } else {
        dmgNone++;
      }

      if (inc.status === 'EM_ATENDIMENTO' || inc.status === 'PENDENTE') {
         totalDowntimeHours += 4.5;
      } else if (inc.status === 'FINALIZADO') {
         totalDowntimeHours += 1.5;
      } else {
         totalDowntimeHours += 2;
      }

      affectedDeliveries++; 
    });

    const elTotal = document.getElementById('kpi-total-incidents');
    if(elTotal) elTotal.textContent = totalIncidents;
    
    const elFreq = document.getElementById('kpi-freq-incidents');
    if(elFreq) elFreq.textContent = freq + '%';
    
    const elCost = document.getElementById('kpi-total-cost');
    if(elCost) elCost.textContent = totalCost.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    
    const affectedPercent = totalPlans > 0 ? ((affectedDeliveries / totalPlans) * 100).toFixed(1) : (affectedDeliveries > 0 ? 100 : 0);
    const elAff = document.getElementById('kpi-affected-deliveries');
    if(elAff) elAff.textContent = affectedPercent + '%';

    const elDown = document.getElementById('kpi-downtime');
    if(elDown) elDown.textContent = Math.floor(totalDowntimeHours) + 'h';

    const updateBar = (id, count, total) => {
      const pct = total > 0 ? Math.round((count / total) * 100) : 0;
      const valEl = document.getElementById(`val-${id}`);
      const barEl = document.getElementById(`bar-${id}`);
      if (valEl) valEl.textContent = pct + '%';
      if (barEl) barEl.style.width = pct + '%';
    };

    updateBar('grav-critical', criticalCount, totalIncidents);
    updateBar('grav-high', highCount, totalIncidents);
    updateBar('grav-medium', medCount, totalIncidents);

    updateBar('dmg-total', dmgTotal, totalIncidents);
    updateBar('dmg-partial', dmgPartial, totalIncidents);
    updateBar('dmg-none', dmgNone, totalIncidents);
  },
'''

if match_init:
    content = content[:match_init.end()] + new_methods + content[match_init.end():]

# 2. Call loadCustomEventTypes() inside init()
init_body_re = re.compile(r'(init\(\) \{.*?)(this\.checkAuth\(\);)', re.DOTALL)
match_init_body = init_body_re.search(content)
if match_init_body:
    content = content[:match_init_body.start(2)] + "this.loadCustomEventTypes();\n    " + content[match_init_body.start(2):]

# 3. Handle switchTab('indicators')
switchTab_re = re.compile(r'(switchTab\(tabId\) \{.*?)(if \(tabId === \'monitoring\'\))', re.DOTALL)
match_switch = switchTab_re.search(content)
if match_switch:
    content = content[:match_switch.start(2)] + "if (tabId === 'indicators') { this.renderIndicatorsTab(); }\n    " + content[match_switch.start(2):]
else:
    # fallback
    switchTab_re2 = re.compile(r'(switchTab\(tabId\) \{.*?this\.currentTab = tabId;)', re.DOTALL)
    match_switch2 = switchTab_re2.search(content)
    if match_switch2:
        content = content[:match_switch2.end()] + "\n    if (tabId === 'indicators') { this.renderIndicatorsTab(); }" + content[match_switch2.end():]

# 4. Handle custom event type inside submitNewIncident
submit_re = re.compile(r'const newInc = appState\.createIncident\(\{\s+title: formData\.get\(\'title\'\),\s+eventType: formData\.get\(\'eventType\'\),', re.DOTALL)

new_submit_logic = '''
    let finalEventType = formData.get('eventType');
    if (finalEventType === 'Outros') {
      const customInput = document.getElementById('customEventType');
      if (customInput && customInput.value.trim()) {
        finalEventType = customInput.value.trim();
        try {
           const customEvents = JSON.parse(localStorage.getItem('GENERAL_CUSTOM_EVENTS') || '[]');
           if (!customEvents.includes(finalEventType)) {
               customEvents.push(finalEventType);
               localStorage.setItem('GENERAL_CUSTOM_EVENTS', JSON.stringify(customEvents));
               
               // Inject into select right now
               const selectElement = document.getElementById('eventTypeSelect');
               if (selectElement) {
                   const options = Array.from(selectElement.options);
                   const outrosIndex = options.findIndex(opt => opt.value === 'Outros');
                   if (outrosIndex > -1) {
                       const newOption = new Option(finalEventType, finalEventType);
                       selectElement.insertBefore(newOption, selectElement.options[outrosIndex]);
                   }
               }
           }
        } catch(e) {}
      }
    }

    const newInc = appState.createIncident({
      title: formData.get('title'),
      eventType: finalEventType,
'''
content = submit_re.sub(new_submit_logic, content, 1)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("js/app.js successfully patched.")
