import re

def patch_motorista():
    with open('../motorista.html', 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()

    # Remove the hamburger menu button
    # Locate <button onclick="App.toggleMobileDrawer()" class="lg:hidden...
    start_tag = '<button onclick="App.toggleMobileDrawer()"'
    end_tag = '</button>'
    
    idx = html.find(start_tag)
    if idx != -1:
        end_idx = html.find(end_tag, idx) + len(end_tag)
        html = html[:idx] + html[end_idx:]

    # Modify bottom nav to replace saved-plans with profile
    old_btn = """<button data-tab="saved-plans" onclick="App.switchTab('saved-plans')" class="nav-button mobile-nav-btn flex-1 flex flex-col items-center justify-center py-1 text-slate-400">
      <i data-lucide="saveAll" class="w-5 h-5 text-emerald-400"></i>
      <span class="text-[10px] font-medium">Salvos</span>
    </button>"""
    
    new_btn = """<button data-tab="profile" onclick="App.switchTab('profile')" class="nav-button mobile-nav-btn flex-1 flex flex-col items-center justify-center py-1 text-slate-400">
      <i data-lucide="award" class="w-5 h-5 text-amber-500"></i>
      <span class="text-[10px] font-medium">Perfil</span>
    </button>"""
    
    # Also fix lucide icon name (lucide saveAll doesn't exist, it's save or save-all, maybe that's why it was broken)
    html = html.replace(old_btn, new_btn)

    with open('../motorista.html', 'w', encoding='utf-8') as f:
        f.write(html)
        
    print("motorista.html hamburger removed and bottom nav profile added.")

if __name__ == '__main__':
    patch_motorista()
