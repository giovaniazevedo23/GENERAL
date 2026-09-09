import re

def replace_theme(content, theme_id, new_css):
    # Regex to find the if (themeId === 'theme_id') { css = `...` }
    pattern = r"(if\s*\(themeId\s*===\s*'" + theme_id + r"'\)\s*\{\s*css\s*=\s*`\s*:root\s*\{)[\s\S]*?(      `;)"
    match = re.search(pattern, content)
    if match:
        replacement = match.group(1) + new_css + match.group(2)
        return content[:match.start()] + replacement + content[match.end():]
    return content

def patch_app(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    superhero_css = """
          --tw-slate-950: #041a04;
          --tw-slate-900: #082b08;
          --tw-slate-800: #0f400f;
          --tw-slate-700: #1a591a;
          --tw-slate-600: #2d822d;
          --tw-slate-500: #40a840;
          --tw-slate-400: #65c765;
          --tw-slate-300: #93de93;
          --tw-slate-200: #c2f0c2;
          
          --tw-blue-600: #7a9c33;
          --tw-blue-500: #D6CE15;
          --tw-blue-400: #e8e34f;
          --tw-blue-900: #1f3b0f;
          
          --tw-rose-950: #38110b;
          --tw-rose-900: #541d14;
        }"""
        
    nurture_css = """
          --tw-slate-950: #031c1d;
          --tw-slate-900: #052c2e;
          --tw-slate-800: #0b4548;
          --tw-slate-700: #156366;
          --tw-slate-600: #248a8e;
          --tw-slate-500: #35b0b5;
          --tw-slate-400: #5eced4;
          --tw-slate-300: #93e6eb;
          --tw-slate-200: #c9f5f7;
          
          --tw-blue-600: #3B945E;
          --tw-blue-500: #65CCB8;
          --tw-blue-400: #8ae3d1;
          --tw-blue-900: #0c3325;
        }"""
        
    fivehundred_css = """
          --tw-slate-950: #1c0630;
          --tw-slate-900: #2b0b4a;
          --tw-slate-800: #42136e;
          --tw-slate-700: #5c1e96;
          --tw-slate-600: #7e30c4;
          --tw-slate-500: #9b46e8;
          --tw-slate-400: #b97af5;
          --tw-slate-300: #d6aefc;
          --tw-slate-200: #efdbff;
          
          --tw-blue-600: #9b46e8;
          --tw-blue-500: #17E9E0;
          --tw-blue-400: #FFB48F;
          --tw-blue-900: #2a1140;
          
          --tw-emerald-400: #FCCD04;
          --tw-emerald-500: #e3b700;
        }"""
        
    umwelt_css = """
          --tw-slate-950: #061f26;
          --tw-slate-900: #0a2d36;
          --tw-slate-800: #124552;
          --tw-slate-700: #1c6173;
          --tw-slate-600: #2a8399;
          --tw-slate-500: #3ba3bd;
          --tw-slate-400: #60c5db;
          --tw-slate-300: #96e0f2;
          --tw-slate-200: #c9f2fc;
          
          --tw-blue-600: #2B7A78;
          --tw-blue-500: #3AAFA9;
          --tw-blue-400: #5dcbc5;
          --tw-blue-900: #0f3030;
        }"""

    content = replace_theme(content, 'superhero', superhero_css)
    content = replace_theme(content, 'nurture', nurture_css)
    content = replace_theme(content, 'fivehundred', fivehundred_css)
    content = replace_theme(content, 'umwelt', umwelt_css)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Patched colors in {filepath}")

patch_app('../gestor-app/js/app.js')
patch_app('../gestor-app/js/app_motorista.js')
