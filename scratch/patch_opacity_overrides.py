import re

def patch_app(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    new_overrides = """
        .bg-slate-900\\\\/40 { background-color: color-mix(in srgb, var(--tw-slate-900) 40%, transparent) !important; }
        .bg-slate-900\\\\/50 { background-color: color-mix(in srgb, var(--tw-slate-900) 50%, transparent) !important; }
        .bg-slate-900\\\\/60 { background-color: color-mix(in srgb, var(--tw-slate-900) 60%, transparent) !important; }
        .bg-slate-900\\\\/80 { background-color: color-mix(in srgb, var(--tw-slate-900) 80%, transparent) !important; }
        .bg-slate-900\\\\/90 { background-color: color-mix(in srgb, var(--tw-slate-900) 90%, transparent) !important; }
        .bg-slate-900\\\\/95 { background-color: color-mix(in srgb, var(--tw-slate-900) 95%, transparent) !important; }
        .bg-slate-800\\\\/80 { background-color: color-mix(in srgb, var(--tw-slate-800) 80%, transparent) !important; }
        .border-slate-800\\\\/80 { border-color: color-mix(in srgb, var(--tw-slate-800) 80%, transparent) !important; }
    """
    
    # We will insert this right after .bg-slate-900 { background-color: var(--tw-slate-900) !important; }
    target = r"\.bg-slate-900 \{ background-color: var\(--tw-slate-900\) !important; \}"
    replacement = r".bg-slate-900 { background-color: var(--tw-slate-900) !important; }" + new_overrides
    
    if "color-mix" not in content:
        content = re.sub(target, replacement, content)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Patched {filepath}")
    else:
        print(f"Already patched {filepath}")

patch_app('../gestor-app/js/app.js')
patch_app('../gestor-app/js/app_motorista.js')
