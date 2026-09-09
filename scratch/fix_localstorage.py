import re

def fix_localstorage(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # In setTheme
    content = content.replace("localStorage.setItem('app-theme', themeId);", "try { localStorage.setItem('app-theme', themeId); } catch(e) { console.warn('localStorage denied'); }")
    
    # In loadTheme
    old_load = """  loadTheme() {
    const saved = localStorage.getItem('app-theme') || 'default';
    this.setTheme(saved);
  },"""
    new_load = """  loadTheme() {
    let saved = 'default';
    try { saved = localStorage.getItem('app-theme') || 'default'; } catch(e) { console.warn('localStorage denied'); }
    this.setTheme(saved);
  },"""
    
    if old_load in content:
        content = content.replace(old_load, new_load)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed localStorage in {filepath}")

fix_localstorage('../gestor-app/js/app.js')
fix_localstorage('../gestor-app/js/app_motorista.js')
