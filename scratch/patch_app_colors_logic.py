import re

def patch_app(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    superhero_css = """
          --tw-slate-950: #0a3314;
          --tw-slate-900: #0f4a1f;
          --tw-slate-800: #146329;
          --tw-slate-700: #1a7a34;
          --tw-slate-600: #229c43;
          --tw-slate-500: #2cbd52;
          --tw-slate-400: #4ade6e;
          --tw-slate-300: #86f09f;
          --tw-slate-200: #bbf7cb;
          
          --tw-blue-600: #9cb85c;
          --tw-blue-500: #D6CE15;
          --tw-blue-400: #e8e34f;
          --tw-blue-900: #082910;
          
          --tw-rose-950: #38110b;
          --tw-rose-900: #541d14;
        }"""
        
    nurture_css = """
          --tw-slate-950: #0a3133;
          --tw-slate-900: #0e4a4d;
          --tw-slate-800: #136366;
          --tw-slate-700: #1a7a7e;
          --tw-slate-600: #249ea3;
          --tw-slate-500: #2dc4ca;
          --tw-slate-400: #5ce1e6;
          --tw-slate-300: #93f1f5;
          --tw-slate-200: #c9fafc;
          
          --tw-blue-600: #57BA98;
          --tw-blue-500: #65CCB8;
          --tw-blue-400: #8ae3d1;
          --tw-blue-900: #082829;
        }"""
        
    fivehundred_css = """
          --tw-slate-950: #1c0d2e;
          --tw-slate-900: #2c144a;
          --tw-slate-800: #3e1d66;
          --tw-slate-700: #4f2680;
          --tw-slate-600: #6b35ad;
          --tw-slate-500: #8843d9;
          --tw-slate-400: #aa71eb;
          --tw-slate-300: #ccabf5;
          --tw-slate-200: #ebd6ff;
          
          --tw-blue-600: #9b46e8;
          --tw-blue-500: #17E9E0;
          --tw-blue-400: #FFB48F;
          --tw-blue-900: #150924;
          
          --tw-emerald-400: #FCCD04;
          --tw-emerald-500: #e3b700;
        }"""
        
    umwelt_css = """
          --tw-slate-950: #092a33;
          --tw-slate-900: #0d404d;
          --tw-slate-800: #125666;
          --tw-slate-700: #176e82;
          --tw-slate-600: #2190aa;
          --tw-slate-500: #2bb4d4;
          --tw-slate-400: #5eddfc;
          --tw-slate-300: #9eeafd;
          --tw-slate-200: #cff4fe;
          
          --tw-blue-600: #3AAFA9;
          --tw-blue-500: #5dcbc5;
          --tw-blue-400: #8fe1dd;
          --tw-blue-900: #072026;
        }"""

    # Replace colors
    pattern = r"(if\s*\(themeId\s*===\s*'superhero'\)\s*\{\s*css\s*=\s*`\s*:root\s*\{)[\s\S]*?(      `;)"
    match = re.search(pattern, content)
    if match: content = content[:match.start()] + match.group(1) + superhero_css + match.group(2) + content[match.end():]

    pattern = r"(if\s*\(themeId\s*===\s*'nurture'\)\s*\{\s*css\s*=\s*`\s*:root\s*\{)[\s\S]*?(      `;)"
    match = re.search(pattern, content)
    if match: content = content[:match.start()] + match.group(1) + nurture_css + match.group(2) + content[match.end():]

    pattern = r"(if\s*\(themeId\s*===\s*'fivehundred'\)\s*\{\s*css\s*=\s*`\s*:root\s*\{)[\s\S]*?(      `;)"
    match = re.search(pattern, content)
    if match: content = content[:match.start()] + match.group(1) + fivehundred_css + match.group(2) + content[match.end():]

    pattern = r"(if\s*\(themeId\s*===\s*'umwelt'\)\s*\{\s*css\s*=\s*`\s*:root\s*\{)[\s\S]*?(      `;)"
    match = re.search(pattern, content)
    if match: content = content[:match.start()] + match.group(1) + umwelt_css + match.group(2) + content[match.end():]

    # Add selection logic
    selection_logic = """
    // Update visual selection
    document.querySelectorAll('.theme-btn').forEach(btn => {
      let ringDiv = btn.querySelector('.theme-ring');
      if (ringDiv) {
        if (btn.dataset.theme === themeId || (themeId === 'default' && btn.dataset.theme === 'default')) {
          ringDiv.classList.add('ring-4', 'ring-blue-500', 'ring-offset-2', 'ring-offset-slate-900');
        } else {
          ringDiv.classList.remove('ring-4', 'ring-blue-500', 'ring-offset-2', 'ring-offset-slate-900');
        }
      }
    });
    
    styleEl.innerHTML = css;
"""
    
    if "Update visual selection" not in content:
        content = content.replace("styleEl.innerHTML = css;", selection_logic)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Patched app in {filepath}")

patch_app('../gestor-app/js/app.js')
patch_app('../gestor-app/js/app_motorista.js')
