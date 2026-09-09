import re
import os

def patch_app(filepath):
    if not os.path.exists(filepath):
        print(f"Not found: {filepath}")
        return
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find where styleEl.innerHTML = css; is called
    target = r"styleEl\.innerHTML\s*=\s*css;"
    
    overrides = """
    if (themeId !== 'default' && themeId !== '' && css !== '') {
      css += `
        /* Forcing Tailwind Overrides for Themes */
        .bg-slate-950 { background-color: var(--tw-slate-950) !important; }
        .bg-slate-900 { background-color: var(--tw-slate-900) !important; }
        .bg-slate-800 { background-color: var(--tw-slate-800) !important; }
        .bg-slate-700 { background-color: var(--tw-slate-700) !important; }
        .text-slate-100 { color: var(--tw-slate-100) !important; }
        .text-slate-200 { color: var(--tw-slate-200) !important; }
        .text-slate-300 { color: var(--tw-slate-300) !important; }
        .text-slate-400 { color: var(--tw-slate-400) !important; }
        .text-slate-500 { color: var(--tw-slate-500) !important; }
        .border-slate-800 { border-color: var(--tw-slate-800) !important; }
        .border-slate-700 { border-color: var(--tw-slate-700) !important; }
        
        .bg-blue-600 { background-color: var(--tw-blue-600) !important; }
        .hover\:bg-blue-500:hover { background-color: var(--tw-blue-500) !important; }
        .text-blue-500 { color: var(--tw-blue-500) !important; }
        .border-blue-500 { border-color: var(--tw-blue-500) !important; }
        .focus\:border-blue-500:focus { border-color: var(--tw-blue-500) !important; }
      `;
    }
    
    styleEl.innerHTML = css;
"""
    
    if re.search(target, content):
        if "Forcing Tailwind Overrides for Themes" not in content:
            content = re.sub(target, overrides, content)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Successfully patched {filepath}")
        else:
            print(f"Already patched {filepath}")
    else:
        print(f"Target not found in {filepath}")

patch_app('../gestor-app/js/app.js')
patch_app('../gestor-app/js/app_motorista.js')
