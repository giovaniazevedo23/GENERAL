import re

def patch_app(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # We need to change the selection logic
    old_logic = """    // Update visual selection
    document.querySelectorAll('.theme-btn').forEach(btn => {
      let ringDiv = btn.querySelector('.theme-ring');
      if (ringDiv) {
        if (btn.dataset.theme === themeId || (themeId === 'default' && btn.dataset.theme === 'default')) {
          ringDiv.classList.add('ring-4', 'ring-blue-500', 'ring-offset-2', 'ring-offset-slate-900');
        } else {
          ringDiv.classList.remove('ring-4', 'ring-blue-500', 'ring-offset-2', 'ring-offset-slate-900');
        }
      }
    });"""

    new_logic = """    // Update visual selection
    document.querySelectorAll('.theme-btn').forEach(btn => {
      if (btn.dataset.theme === themeId || (themeId === 'default' && btn.dataset.theme === 'default')) {
        btn.classList.add('theme-selected');
      } else {
        btn.classList.remove('theme-selected');
      }
    });"""

    if old_logic in content:
        content = content.replace(old_logic, new_logic)
    
    # Add the CSS rule to EVERY theme (including default, superhero, etc)
    # We will just append it to the common overrides block
    css_override = """
        /* Forcing Tailwind Overrides for Themes */
        .theme-selected .theme-ring {
          box-shadow: 0 0 0 4px #0f172a, 0 0 0 6px #3b82f6 !important;
        }"""
        
    if ".theme-selected .theme-ring" not in content:
        content = content.replace("/* Forcing Tailwind Overrides for Themes */", css_override)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Patched logic in {filepath}")

patch_app('../gestor-app/js/app.js')
patch_app('../gestor-app/js/app_motorista.js')
