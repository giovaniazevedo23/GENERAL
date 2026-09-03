import sys
import re
import os

def patch_index_html():
    file_path = r"c:\Users\giova\.gemini\antigravity\scratch\general-app\index.html"
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    if "firebase-auth-compat" not in content:
        content = content.replace(
            '<script src="https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore-compat.js"></script>',
            '<script src="https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore-compat.js"></script>\n  <script src="https://www.gstatic.com/firebasejs/10.12.2/firebase-auth-compat.js"></script>'
        )
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("Patched index.html")
    else:
        print("index.html already patched")

def patch_motorista_html():
    file_path = r"c:\Users\giova\.gemini\antigravity\scratch\general-app\motorista.html"
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    firebase_scripts = """
  <script src="https://www.gstatic.com/firebasejs/10.12.2/firebase-app-compat.js"></script>
  <script src="https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore-compat.js"></script>
  <script src="https://www.gstatic.com/firebasejs/10.12.2/firebase-auth-compat.js"></script>
  <script>
    const firebaseConfig = {
      apiKey: "AIzaSyDxUS2P-vjhEiYsb8rhYOaTxNOZohaEVo4",
      authDomain: "general-f311a.firebaseapp.com",
      projectId: "general-f311a",
      storageBucket: "general-f311a.firebasestorage.app",
      messagingSenderId: "689040676417",
      appId: "1:689040676417:web:cd237169036e4bcbeed8c0",
      measurementId: "G-T3008FMGZS"
    };
    if (!firebase.apps.length) {
       firebase.initializeApp(firebaseConfig);
    }
    window.db = firebase.firestore();
  </script>
"""

    if "firebase-app-compat" not in content:
        content = content.replace(
            '<script src="js/lucide.min.js"></script>',
            firebase_scripts + '  <script src="js/lucide.min.js"></script>'
        )
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("Patched motorista.html")
    else:
        print("motorista.html already patched")

def patch_app_js():
    file_path = r"c:\Users\giova\.gemini\antigravity\scratch\general-app\js\app.js"
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 1. Patch loginWithGoogle
    # We will replace the entire try block of loginWithGoogle
    login_with_google_regex = r"async loginWithGoogle\(\)\s*\{\s*try\s*\{.*?catch\s*\([^)]*\)\s*\{.*?\}\s*\},"
    
    new_login_with_google = """async loginWithGoogle() {
    try {
      this.showToast('Abrindo contas do Google...');
      const provider = new firebase.auth.GoogleAuthProvider();
      const result = await firebase.auth().signInWithPopup(provider);
      const user = result.user;
      
      const googleUser = {
        id: 'GOOG-' + (user.uid),
        name: user.displayName || user.email.split('@')[0],
        email: user.email,
        provider: 'google',
        photo: user.photoURL || null
      };

      // Check if user exists in Firestore
      const docSnap = await window.db.collection('users').doc(user.email).get();
      if (docSnap.exists) {
          const data = docSnap.data();
          if (data.companyCnpj) {
              googleUser.company = data.company;
              googleUser.companyCnpj = data.companyCnpj;
              googleUser.role = data.role;
              
              appState.currentUser = googleUser;
              localStorage.setItem('general_user', JSON.stringify(googleUser));
              this.checkAuth();
              this.showToast(`🔑 Bem-vindo(a) de volta, ${googleUser.name}!`);
              return;
          }
      }

      // If not, ask for extra info
      window.tempGoogleUser = googleUser;
      const modal = document.getElementById('google-extra-modal');
      if (modal) {
         modal.classList.remove('hidden');
         if(window.lucide) window.lucide.createIcons();
      } else {
         appState.currentUser = googleUser;
         localStorage.setItem('general_user', JSON.stringify(googleUser));
         this.checkAuth();
      }
    } catch (e) {
      console.error(e);
      this.showToast('Erro ao logar com Google.');
    }
  },"""
    
    content = re.sub(login_with_google_regex, new_login_with_google, content, flags=re.DOTALL)
    
    # 2. Patch submitGoogleExtraInfo
    submit_extra_regex = r"submitGoogleExtraInfo\(\)\s*\{.*?(?=appState\.currentUser = window\.tempGoogleUser;)"
    
    # Actually it's easier to just do a string replace for the submit logic
    old_submit_save = """       appState.currentUser = window.tempGoogleUser;
       localStorage.setItem('general_user', JSON.stringify(window.tempGoogleUser));"""
       
    new_submit_save = """       appState.currentUser = window.tempGoogleUser;
       localStorage.setItem('general_user', JSON.stringify(window.tempGoogleUser));
       
       // Save to Firestore so Motorista APK can see it
       if (window.db) {
           window.db.collection('users').doc(window.tempGoogleUser.email).set(window.tempGoogleUser)
             .catch(e => console.error('Erro ao salvar no Firestore:', e));
       }"""
    
    content = content.replace(old_submit_save, new_submit_save)
    
    # 3. Patch login (manual login) to also sync to Firestore
    # We find where usersDb[userId] = newUser is set
    old_manual_save = """        usersDb[userId] = newUser;
        localStorage.setItem('general_users_db', JSON.stringify(usersDb));"""
        
    new_manual_save = """        usersDb[userId] = newUser;
        localStorage.setItem('general_users_db', JSON.stringify(usersDb));
        
        // Sync new manual registration to Firestore
        if (window.db) {
            window.db.collection('users').doc(userId).set(newUser)
              .catch(e => console.error('Erro sync Firestore:', e));
        }"""
        
    content = content.replace(old_manual_save, new_manual_save)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Patched app.js")


def patch_app_motorista_js():
    file_path = r"c:\Users\giova\.gemini\antigravity\scratch\general-app\js\app_motorista.js"
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Find the login listener for motorista
    old_listener = """    if (btnLoginMot) {
      btnLoginMot.addEventListener('click', () => {
        const nome = document.getElementById('mot-nome')?.value.trim();
        const emp = document.getElementById('mot-empresa')?.value.trim();
        const cnpj = document.getElementById('mot-cnpj')?.value.trim();
        const cargo = document.getElementById('mot-cargo')?.value.trim();

        if(!nome || !emp || !cnpj || !cargo) {
          this.showToast('Preencha todos os campos!');
          return;
        }

        const newUser = { id: 'MOT-'+Math.floor(Math.random()*900000+100000), name: nome, company: emp, companyCnpj: cnpj, role: cargo, provider: 'motorista' };
        appState.currentUser = newUser;
        localStorage.setItem('general_user', JSON.stringify(newUser));
        
        // Force sync cargo catalog for this cnpj
        this.renderCargoCatalog();
        
        this.checkAuth();
        this.showToast(`Bem-vindo, ${nome}!`);
      });
    }"""
    
    new_listener = """    if (btnLoginMot) {
      btnLoginMot.addEventListener('click', async () => {
        const nome = document.getElementById('mot-nome')?.value.trim();
        const emp = document.getElementById('mot-empresa')?.value.trim();
        const cnpj = document.getElementById('mot-cnpj')?.value.trim();
        const cargo = document.getElementById('mot-cargo')?.value.trim();

        if(!nome || !emp || !cnpj || !cargo) {
          this.showToast('Preencha todos os campos!');
          return;
        }
        
        this.showToast('Verificando CNPJ na nuvem...');
        
        // VALIDATE WITH FIRESTORE
        try {
            if (!window.db) {
                this.showToast('Erro: Conexão com banco de dados não estabelecida.', 'error');
                return;
            }
            
            const snapshot = await window.db.collection('users').where('companyCnpj', '==', cnpj).get();
            if (snapshot.empty) {
                this.showToast('CNPJ não cadastrado. Peça para o Gestor criar uma conta na Web primeiro.', 'error');
                return;
            }
            
            // Validado com sucesso!
            const newUser = { id: 'MOT-'+Math.floor(Math.random()*900000+100000), name: nome, company: emp, companyCnpj: cnpj, role: cargo, provider: 'motorista' };
            appState.currentUser = newUser;
            localStorage.setItem('general_user', JSON.stringify(newUser));
            
            this.renderCargoCatalog();
            this.checkAuth();
            this.showToast(`Acesso Liberado! Bem-vindo, ${nome}!`);
        } catch (error) {
            console.error(error);
            this.showToast('Erro de conexão ao verificar CNPJ. Tente novamente.', 'error');
        }
      });
    }"""
    
    content = content.replace(old_listener, new_listener)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Patched app_motorista.js")


if __name__ == "__main__":
    patch_index_html()
    patch_motorista_html()
    patch_app_js()
    patch_app_motorista_js()
