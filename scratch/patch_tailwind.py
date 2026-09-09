import re
import sys
import os

def fix_tailwind(filepath):
    if not os.path.exists(filepath):
        print(f"File {filepath} not found")
        return
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # The regex matches the brand object exactly as it is in the HTML
    pattern = re.compile(r"brand:\s*\{\s*50:\s*'#eff6ff',\s*500:\s*'#3b82f6',\s*600:\s*'#2563eb',\s*700:\s*'#1d4ed8',\s*900:\s*'#1e3a8a',\s*950:\s*'#0f172a'\s*\}", re.MULTILINE)
    
    new_colors = """brand: { 50: '#eff6ff', 500: '#3b82f6', 600: '#2563eb', 700: '#1d4ed8', 900: '#1e3a8a', 950: '#0f172a' },
            slate: {
              50: 'var(--tw-slate-50, #f8fafc)',
              100: 'var(--tw-slate-100, #f1f5f9)',
              200: 'var(--tw-slate-200, #e2e8f0)',
              300: 'var(--tw-slate-300, #cbd5e1)',
              400: 'var(--tw-slate-400, #94a3b8)',
              500: 'var(--tw-slate-500, #64748b)',
              600: 'var(--tw-slate-600, #475569)',
              700: 'var(--tw-slate-700, #334155)',
              800: 'var(--tw-slate-800, #1e293b)',
              900: 'var(--tw-slate-900, #0f172a)',
              950: 'var(--tw-slate-950, #020617)'
            },
            blue: {
              50: 'var(--tw-blue-50, #eff6ff)',
              100: 'var(--tw-blue-100, #dbeafe)',
              200: 'var(--tw-blue-200, #bfdbfe)',
              300: 'var(--tw-blue-300, #93c5fd)',
              400: 'var(--tw-blue-400, #60a5fa)',
              500: 'var(--tw-blue-500, #3b82f6)',
              600: 'var(--tw-blue-600, #2563eb)',
              700: 'var(--tw-blue-700, #1d4ed8)',
              800: 'var(--tw-blue-800, #1e40af)',
              900: 'var(--tw-blue-900, #1e3a8a)',
              950: 'var(--tw-blue-950, #172554)'
            },
            rose: {
              300: 'var(--tw-rose-300, #fda4af)',
              400: 'var(--tw-rose-400, #fb7185)',
              500: 'var(--tw-rose-500, #f43f5e)',
              600: 'var(--tw-rose-600, #e11d48)',
              900: 'var(--tw-rose-900, #881337)',
              950: 'var(--tw-rose-950, #4c0519)'
            },
            emerald: {
              400: 'var(--tw-emerald-400, #34d399)',
              500: 'var(--tw-emerald-500, #10b981)',
              600: 'var(--tw-emerald-600, #059669)',
              900: 'var(--tw-emerald-900, #064e3b)',
              950: 'var(--tw-emerald-950, #022c22)'
            },
            amber: {
              400: 'var(--tw-amber-400, #fbbf24)',
              500: 'var(--tw-amber-500, #f59e0b)',
              900: 'var(--tw-amber-900, #78350f)'
            }"""

    if pattern.search(content):
        content = pattern.sub(new_colors, content)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Patched tailwind.config in {filepath}")
    else:
        print(f"Could not find brand block in {filepath}")

fix_tailwind('../gestor-app/index.html')
fix_tailwind('../gestor-app/motorista.html')
