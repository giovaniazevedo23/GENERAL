import sys
import re

file_path = "index.html"

try:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
except UnicodeDecodeError:
    with open(file_path, "r", encoding="latin-1") as f:
        content = f.read()

# 1. Update eventType Select
old_select = '''<select name="eventType" class="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-xs text-white">
              <option value="Tombamento">Tombamento</option>
              <option value="Colisão Traseira">Colisão Traseira</option>
              <option value="Avaria Térmica / Carga">Avaria Térmica / Carga</option>
              <option value="Vazamento Químico">Vazamento Químico</option>
              <option value="Saída de Pista">Saída de Pista</option>
                <option value="Outros">Outros</option>
            </select>'''

# fallback search in case of slight changes
select_pattern = re.compile(r'<select name="eventType" class="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-xs text-white">.*?</select>', re.DOTALL)

new_select = '''<select id="eventTypeSelect" name="eventType" class="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-xs text-white" onchange="if(typeof App !== 'undefined' && App.handleEventTypeChange) App.handleEventTypeChange(this)">
              <option value="Avaria">Avaria</option>
              <option value="Roubo">Roubo</option>
              <option value="Incêndio">Incêndio</option>
              <option value="Perda Total">Perda Total</option>
              <option value="Colisões">Colisões</option>
              <option value="Outros">Outros...</option>
            </select>
            <input type="text" id="customEventType" placeholder="Especifique o tipo de evento (Pressione Enter para usar)" class="hidden mt-2 w-full bg-slate-900 border border-blue-500 rounded-lg p-2 text-xs text-white focus:outline-none" />'''

content = select_pattern.sub(new_select, content, 1)

# 2. Add Indicators View
indicators_view = '''
      <!-- VIEW: INDICADORES E KPIS -->
      <div id="view-indicators" class="tab-view hidden space-y-6">
        
        <div class="flex items-center justify-between mb-4">
          <div>
            <h2 class="text-xl font-black text-white flex items-center gap-2">
              <i data-lucide="bar-chart-2" class="w-6 h-6 text-indigo-400"></i>
              Indicadores & Desempenho (KPIs)
            </h2>
            <p class="text-xs text-slate-400 mt-1">Estatísticas globais normalizadas de planos logísticos e ocorrências.</p>
          </div>
          <button onclick="if(window.App) App.renderIndicatorsTab()" class="bg-slate-800 hover:bg-slate-700 text-slate-300 px-3 py-2 rounded-xl text-xs font-bold transition-all flex items-center gap-2 border border-slate-700">
            <i data-lucide="refresh-cw" class="w-4 h-4"></i> Atualizar Dados
          </button>
        </div>

        <!-- KPI Grid -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <!-- Total Ocorrências -->
          <div class="bg-slate-900 border border-slate-800 p-5 rounded-2xl flex flex-col justify-between">
            <div class="flex items-center gap-2 mb-2">
              <div class="w-8 h-8 rounded-full bg-blue-500/10 flex items-center justify-center">
                <i data-lucide="alert-triangle" class="w-4 h-4 text-blue-400"></i>
              </div>
              <span class="text-xs font-bold text-slate-400 uppercase tracking-wide">Ocorrências</span>
            </div>
            <div class="flex items-end gap-2">
              <span id="kpi-total-incidents" class="text-3xl font-black text-white">0</span>
              <span class="text-[10px] text-slate-500 mb-1">Registradas</span>
            </div>
          </div>

          <!-- Frequência (Incidentes / Planos) -->
          <div class="bg-slate-900 border border-slate-800 p-5 rounded-2xl flex flex-col justify-between">
            <div class="flex items-center gap-2 mb-2">
              <div class="w-8 h-8 rounded-full bg-purple-500/10 flex items-center justify-center">
                <i data-lucide="activity" class="w-4 h-4 text-purple-400"></i>
              </div>
              <span class="text-xs font-bold text-slate-400 uppercase tracking-wide">Frequência</span>
            </div>
            <div class="flex items-end gap-2">
              <span id="kpi-freq-incidents" class="text-3xl font-black text-white">0%</span>
              <span class="text-[10px] text-slate-500 mb-1">Taxa de Acidente</span>
            </div>
          </div>

          <!-- Custo Total Estimado -->
          <div class="bg-slate-900 border border-slate-800 p-5 rounded-2xl flex flex-col justify-between">
            <div class="flex items-center gap-2 mb-2">
              <div class="w-8 h-8 rounded-full bg-rose-500/10 flex items-center justify-center">
                <i data-lucide="dollar-sign" class="w-4 h-4 text-rose-400"></i>
              </div>
              <span class="text-xs font-bold text-slate-400 uppercase tracking-wide">Custo Est.</span>
            </div>
            <div class="flex items-end gap-1">
              <span class="text-lg font-bold text-slate-500 mb-1">R$</span>
              <span id="kpi-total-cost" class="text-2xl font-black text-rose-400">0</span>
            </div>
          </div>

          <!-- Entregas Afetadas -->
          <div class="bg-slate-900 border border-slate-800 p-5 rounded-2xl flex flex-col justify-between">
            <div class="flex items-center gap-2 mb-2">
              <div class="w-8 h-8 rounded-full bg-amber-500/10 flex items-center justify-center">
                <i data-lucide="truck" class="w-4 h-4 text-amber-400"></i>
              </div>
              <span class="text-xs font-bold text-slate-400 uppercase tracking-wide">Afetadas</span>
            </div>
            <div class="flex items-end gap-2">
              <span id="kpi-affected-deliveries" class="text-3xl font-black text-amber-400">0%</span>
              <span class="text-[10px] text-slate-500 mb-1">Cargas</span>
            </div>
          </div>
        </div>

        <!-- Gráficos de Barra Customizados (CSS) -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          
          <!-- Gravidade dos Acidentes -->
          <div class="bg-slate-900/50 border border-slate-800 p-6 rounded-2xl">
            <h3 class="text-sm font-bold text-white mb-4 flex items-center gap-2">
              <i data-lucide="pie-chart" class="w-4 h-4 text-slate-400"></i> Nível de Gravidade
            </h3>
            <div class="space-y-4">
              
              <div>
                <div class="flex justify-between text-xs mb-1">
                  <span class="font-semibold text-slate-300">Crítico / Fatalidade</span>
                  <span id="val-grav-critical" class="text-slate-400 font-bold">0%</span>
                </div>
                <div class="w-full bg-slate-950 rounded-full h-2">
                  <div id="bar-grav-critical" class="bg-rose-500 h-2 rounded-full transition-all duration-1000" style="width: 0%"></div>
                </div>
              </div>

              <div>
                <div class="flex justify-between text-xs mb-1">
                  <span class="font-semibold text-slate-300">Alto Risco</span>
                  <span id="val-grav-high" class="text-slate-400 font-bold">0%</span>
                </div>
                <div class="w-full bg-slate-950 rounded-full h-2">
                  <div id="bar-grav-high" class="bg-amber-500 h-2 rounded-full transition-all duration-1000" style="width: 0%"></div>
                </div>
              </div>

              <div>
                <div class="flex justify-between text-xs mb-1">
                  <span class="font-semibold text-slate-300">Médio / Leve</span>
                  <span id="val-grav-medium" class="text-slate-400 font-bold">0%</span>
                </div>
                <div class="w-full bg-slate-950 rounded-full h-2">
                  <div id="bar-grav-medium" class="bg-blue-400 h-2 rounded-full transition-all duration-1000" style="width: 0%"></div>
                </div>
              </div>

            </div>
          </div>

          <!-- Danos à Mercadoria -->
          <div class="bg-slate-900/50 border border-slate-800 p-6 rounded-2xl">
            <h3 class="text-sm font-bold text-white mb-4 flex items-center gap-2">
              <i data-lucide="package-minus" class="w-4 h-4 text-slate-400"></i> Danos à Mercadoria
            </h3>
            <div class="space-y-4">
              
              <div>
                <div class="flex justify-between text-xs mb-1">
                  <span class="font-semibold text-slate-300">Perda Total</span>
                  <span id="val-dmg-total" class="text-slate-400 font-bold">0%</span>
                </div>
                <div class="w-full bg-slate-950 rounded-full h-2">
                  <div id="bar-dmg-total" class="bg-red-500 h-2 rounded-full transition-all duration-1000" style="width: 0%"></div>
                </div>
              </div>

              <div>
                <div class="flex justify-between text-xs mb-1">
                  <span class="font-semibold text-slate-300">Avaria Parcial</span>
                  <span id="val-dmg-partial" class="text-slate-400 font-bold">0%</span>
                </div>
                <div class="w-full bg-slate-950 rounded-full h-2">
                  <div id="bar-dmg-partial" class="bg-orange-400 h-2 rounded-full transition-all duration-1000" style="width: 0%"></div>
                </div>
              </div>

              <div>
                <div class="flex justify-between text-xs mb-1">
                  <span class="font-semibold text-slate-300">Sem Danos</span>
                  <span id="val-dmg-none" class="text-slate-400 font-bold">0%</span>
                </div>
                <div class="w-full bg-slate-950 rounded-full h-2">
                  <div id="bar-dmg-none" class="bg-emerald-400 h-2 rounded-full transition-all duration-1000" style="width: 0%"></div>
                </div>
              </div>

            </div>
          </div>

        </div>

        <!-- Log Temporal -->
        <div class="bg-slate-900 border border-slate-800 p-6 rounded-2xl">
           <h3 class="text-sm font-bold text-white mb-4 flex items-center gap-2">
             <i data-lucide="clock" class="w-4 h-4 text-slate-400"></i> Tempo de Paralisação (Horas Paradas)
           </h3>
           <div class="flex items-center gap-6">
             <div class="flex-1">
               <p class="text-xs text-slate-400 mb-2">Acúmulo de horas de inatividade decorrente das ocorrências não resolvidas.</p>
               <div class="h-4 w-full bg-slate-950 rounded-full overflow-hidden">
                 <div class="h-full bg-gradient-to-r from-blue-600 to-cyan-400 w-1/3 progress-stripes"></div>
               </div>
             </div>
             <div class="text-right shrink-0">
               <span id="kpi-downtime" class="text-2xl font-black text-cyan-400">0h</span>
             </div>
           </div>
        </div>

      </div>
'''

view_dashboard_marker = '<div id="view-dashboard"'
idx_dash = content.find(view_dashboard_marker)
if idx_dash != -1:
    content = content[:idx_dash] + indicators_view + "\n" + content[idx_dash:]


# 3. Sidebar Navigation for Indicators
desktop_dashboard_btn_re = re.compile(r'(<button data-tab="dashboard" onclick="App.switchTab\(\'dashboard\'\)" class="nav-button w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-bold transition-all bg-blue-600 text-white shadow-md">.*?</button>)', re.DOTALL)
desktop_indicators_btn = '''
          <button data-tab="indicators" onclick="App.switchTab('indicators')" class="nav-button w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-bold text-slate-400 hover:bg-slate-800 hover:text-slate-200 transition-all">
            <i data-lucide="bar-chart-2" class="w-4 h-4 text-indigo-400"></i>
            Indicadores e KPIs
          </button>'''

match_dt = desktop_dashboard_btn_re.search(content)
if match_dt:
    content = content[:match_dt.end()] + desktop_indicators_btn + content[match_dt.end():]


# 4. Mobile Bottom Nav for Indicators (we'll replace Monitoring Tático or just append)
mobile_dashboard_btn_re = re.compile(r'(<button data-tab="dashboard" onclick="App.switchTab\(\'dashboard\'\)" class="nav-button mobile-nav-btn flex-1 flex flex-col items-center justify-center py-1 text-slate-400">.*?</button>)', re.DOTALL)
mobile_indicators_btn = '''
    <button data-tab="indicators" onclick="App.switchTab('indicators')" class="nav-button mobile-nav-btn flex-1 flex flex-col items-center justify-center py-1 text-slate-400">
      <i data-lucide="bar-chart-2" class="w-5 h-5 text-indigo-400"></i>
      <span class="text-[10px] font-medium">KPIs</span>
    </button>'''

match_mb = mobile_dashboard_btn_re.search(content)
if match_mb:
    content = content[:match_mb.end()] + mobile_indicators_btn + content[match_mb.end():]

# 5. Mobile Drawer Menu
drawer_dashboard_btn_re = re.compile(r'(<button data-tab="dashboard" onclick="App.switchTab\(\'dashboard\'\); App.toggleMobileDrawer\(\);" class="nav-button w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-bold text-slate-400 hover:bg-slate-800 transition-all">.*?</button>)', re.DOTALL)
drawer_indicators_btn = '''
              <button data-tab="indicators" onclick="App.switchTab('indicators'); App.toggleMobileDrawer();" class="nav-button w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-bold text-slate-400 hover:bg-slate-800 transition-all">
                <i data-lucide="bar-chart-2" class="w-4 h-4 text-indigo-400"></i>
                Indicadores e KPIs
              </button>'''

match_dr = drawer_dashboard_btn_re.search(content)
if match_dr:
    content = content[:match_dr.end()] + drawer_indicators_btn + content[match_dr.end():]

try:
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
except Exception:
    with open(file_path, "w", encoding="latin-1") as f:
        f.write(content)

print("index.html successfully updated.")
