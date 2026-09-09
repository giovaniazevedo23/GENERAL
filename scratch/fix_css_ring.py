import re

def fix_css_injection(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # The issue: the CSS override for the blue ring is INSIDE the if (themeId !== 'default') block!
    # I need to make sure the blue ring CSS is appended ALWAYS!
    
    # We will remove it from the "Forcing Tailwind Overrides" block
    content = content.replace("""        /* Forcing Tailwind Overrides for Themes */
        .theme-selected .theme-ring {
          box-shadow: 0 0 0 4px #0f172a, 0 0 0 6px #3b82f6 !important;
        }""", "        /* Forcing Tailwind Overrides for Themes */")
        
    # And we will append it right before styleEl.innerHTML = css;
    
    global_css = """
    // Always inject the ring selection CSS, regardless of theme
    css += `
      .theme-selected .theme-ring {
        box-shadow: 0 0 0 4px #0f172a, 0 0 0 6px #3b82f6 !important;
      }
    `;
    
    styleEl.innerHTML = css;"""
    
    if "// Always inject the ring selection CSS" not in content:
        content = content.replace("styleEl.innerHTML = css;", global_css)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed CSS injection in {filepath}")

fix_css_injection('../gestor-app/js/app.js')
fix_css_injection('../gestor-app/js/app_motorista.js')
