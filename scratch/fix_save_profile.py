import re

def fix_save_profile(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    old_logic = "localStorage.setItem('general_user', JSON.stringify(appState.currentUser));"
    new_logic = "try { localStorage.setItem('general_user', JSON.stringify(appState.currentUser)); } catch(e) { console.warn('localStorage denied'); }"
    
    if old_logic in content:
        content = content.replace(old_logic, new_logic)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed saveProfile in {filepath}")

fix_save_profile('../gestor-app/js/app.js')
fix_save_profile('../gestor-app/js/app_motorista.js')
