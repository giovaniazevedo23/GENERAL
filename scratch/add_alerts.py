import re

def add_alerts(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    new_setTheme = """  setTheme(themeId) {
    alert('SETTING THEME: ' + themeId);
    try { localStorage.setItem('app-theme', themeId); } catch(e) { console.warn('localStorage denied'); }
    let styleEl = document.getElementById('dynamic-theme');
    if (!styleEl) {
      styleEl = document.createElement('style');
      styleEl.id = 'dynamic-theme';
      document.head.appendChild(styleEl);
    }
    
    let css = '';
"""
    content = content.replace("  setTheme(themeId) {\n    try { localStorage.setItem('app-theme', themeId);", new_setTheme)

    new_saveProfile = """  saveProfile() {
    alert('SAVE PROFILE CLICKED!');
    if (!appState.currentUser) {
        alert('NO CURRENT USER');
        return;
    }
"""
    content = content.replace("  saveProfile() {\n    if (!appState.currentUser) return;", new_saveProfile)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Added alerts to {filepath}")

add_alerts('../gestor-app/js/app.js')
add_alerts('../gestor-app/js/app_motorista.js')
