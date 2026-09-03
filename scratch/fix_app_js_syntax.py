import sys
import re

def fix():
    file_path = r"c:\Users\giova\.gemini\antigravity\scratch\general-app\js\app.js"
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Find the wrongly inserted block:
    wrong_block = """
  submitGoogleExtraInfo() {
    const company = document.getElementById('google-extra-company')?.value.trim();
    const cnpj = document.getElementById('google-extra-cnpj')?.value.trim();
    const role = document.getElementById('google-extra-role')?.value.trim();
    
    if (!company || !cnpj || !role) {
      this.showToast('Por favor, preencha todos os campos da empresa.');
      return;
    }
    
    if (window.tempGoogleUser) {
       window.tempGoogleUser.company = company;
       window.tempGoogleUser.companyCnpj = cnpj;
       window.tempGoogleUser.role = role;
       
       appState.currentUser = window.tempGoogleUser;
       localStorage.setItem('general_user', JSON.stringify(window.tempGoogleUser));
       
       document.getElementById('google-extra-modal').classList.add('hidden');
       this.checkAuth();
       this.showToast(`ðŸ”‘ Bem-vindo(a) via Google, ${window.tempGoogleUser.name}!`);
    }
  },
"""

    if wrong_block in content:
        # Remove it from the end of the file
        content = content.replace(wrong_block, "")
        
        # Insert it before the end of the App object.
        # Let's search for "};\n\nwindow.addEventListener('DOMContentLoaded'"
        
        target = "};\n\nwindow.addEventListener('DOMContentLoaded'"
        if target in content:
            replacement = "," + wrong_block + target
            content = content.replace(target, replacement)
        else:
            print("Target not found. End of App object may look different.")
            
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("Syntax fixed.")
    else:
        print("Wrong block not found.")

if __name__ == "__main__":
    fix()
