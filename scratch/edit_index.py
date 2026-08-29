import sys
import re

file_path = "index.html"

try:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
except UnicodeDecodeError:
    with open(file_path, "r", encoding="latin-1") as f:
        content = f.read()

# 1. Extract the Monitoramento block
start_marker = "<!-- Monitoramento T" # to avoid encoding issue in 'Tático'
end_marker = "<!-- Layout 2 Colunas: Formulário do Plano vs. Parecer da IA -->"

# Find the block
idx_start = content.find(start_marker)
idx_end = content.find(end_marker)

if idx_start == -1 or idx_end == -1:
    print("Could not find the Monitoramento block")
    sys.exit(1)

monitoramento_block = content[idx_start:idx_end].strip()

# Remove it from view-planner
content = content[:idx_start] + "\n        " + content[idx_end:]

# Wrap it in view-monitoring
monitoring_view = f'''
      <!-- VIEW: MONITORAMENTO -->
      <div id="view-monitoring" class="tab-view hidden space-y-6">
        {monitoramento_block}
      </div>
'''

# Insert it before view-planner
view_planner_marker = '<div id="view-planner" class="tab-view hidden space-y-6">'
idx_planner = content.find(view_planner_marker)
if idx_planner == -1:
    print("Could not find view-planner")
    sys.exit(1)

content = content[:idx_planner] + monitoring_view + content[idx_planner:]

# 3. Add to desktop sidebar
desktop_planner_btn = '''<button data-tab="planner" onclick="App.switchTab('planner')" class="nav-button w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-bold text-slate-400 hover:bg-slate-800 hover:text-slate-200 transition-all">
            <i data-lucide="file-check-2" class="w-4 h-4"></i> Plano de Ação (IA)
          </button>'''

desktop_monitoring_btn = '''
          <button data-tab="monitoring" onclick="App.switchTab('monitoring')" class="nav-button w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-bold text-slate-400 hover:bg-slate-800 hover:text-slate-200 transition-all">
            <i data-lucide="activity" class="w-4 h-4"></i> Monitoramento
          </button>'''

content = content.replace(desktop_planner_btn, desktop_planner_btn + desktop_monitoring_btn)

# 4. Add to mobile bottom nav
mobile_nav_btn = '''<button data-tab="hazmat" onclick="App.switchTab('hazmat')" class="nav-button mobile-nav-btn flex-1 flex flex-col items-center justify-center py-1 text-slate-400">
      <i data-lucide="flame" class="w-5 h-5 text-rose-400"></i>
      <span class="text-[10px] font-medium">ONU</span>
    </button>'''

mobile_monitoring_btn = '''
    <button data-tab="monitoring" onclick="App.switchTab('monitoring')" class="nav-button mobile-nav-btn flex-1 flex flex-col items-center justify-center py-1 text-slate-400">
      <i data-lucide="activity" class="w-5 h-5 text-emerald-400"></i>
      <span class="text-[10px] font-medium">Monitorar</span>
    </button>'''

content = content.replace(mobile_nav_btn, mobile_nav_btn + mobile_monitoring_btn)

# 5. Add to mobile drawer
drawer_planner_btn = '''<button data-tab="planner" onclick="App.switchTab('planner'); App.toggleMobileDrawer();" class="nav-button w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-bold text-slate-400 hover:bg-slate-800 transition-all">
                <i data-lucide="file-check-2" class="w-4 h-4"></i> Plano de Ação (IA)
              </button>'''

drawer_monitoring_btn = '''
              <button data-tab="monitoring" onclick="App.switchTab('monitoring'); App.toggleMobileDrawer();" class="nav-button w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-bold text-slate-400 hover:bg-slate-800 transition-all">
                <i data-lucide="activity" class="w-4 h-4"></i> Monitoramento
              </button>'''

content = content.replace(drawer_planner_btn, drawer_planner_btn + drawer_monitoring_btn)


try:
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
except Exception as e:
    with open(file_path, "w", encoding="latin-1") as f:
        f.write(content)

print("Done editing index.html")
