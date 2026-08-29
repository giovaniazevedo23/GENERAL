import sys
import re

file_path = "index.html"

try:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
except UnicodeDecodeError:
    with open(file_path, "r", encoding="latin-1") as f:
        content = f.read()

desktop_monitoring_btn = '''
          <button data-tab="monitoring" onclick="App.switchTab('monitoring')" class="nav-button w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-bold text-slate-400 hover:bg-slate-800 hover:text-slate-200 transition-all">
            <i data-lucide="activity" class="w-4 h-4 text-emerald-400"></i>
            Monitoramento Tático
          </button>'''

drawer_monitoring_btn = '''
              <button data-tab="monitoring" onclick="App.switchTab('monitoring'); App.toggleMobileDrawer();" class="nav-button w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-bold text-slate-400 hover:bg-slate-800 transition-all">
                <i data-lucide="activity" class="w-4 h-4 text-emerald-400"></i>
                Monitoramento Tático
              </button>'''

# 1. Desktop sidebar: find the 'planner' button and append after its closing </button>
pattern_desktop = re.compile(r'(<button data-tab="planner" onclick="App.switchTab\(\'planner\'\)" class="nav-button w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-bold text-slate-400 hover:bg-slate-800 hover:text-slate-200 transition-all">.*?</button>)', re.DOTALL)
match_desktop = pattern_desktop.search(content)

if match_desktop:
    content = content[:match_desktop.end()] + desktop_monitoring_btn + content[match_desktop.end():]
else:
    print("Desktop button not found!")

# 2. Drawer menu: find the 'planner' button (with toggleMobileDrawer) and append after its closing </button>
pattern_drawer = re.compile(r'(<button data-tab="planner" onclick="App.switchTab\(\'planner\'\); App.toggleMobileDrawer\(\);" class="nav-button w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-bold text-slate-400 hover:bg-slate-800 transition-all">.*?</button>)', re.DOTALL)
match_drawer = pattern_drawer.search(content)

if match_drawer:
    content = content[:match_drawer.end()] + drawer_monitoring_btn + content[match_drawer.end():]
else:
    print("Drawer button not found!")

try:
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
except Exception:
    with open(file_path, "w", encoding="latin-1") as f:
        f.write(content)

print("Fixed sidebars!")
