import os

def patch_app_js():
    js_file = 'js/app.js'
    if not os.path.exists(js_file):
        print("js/app.js not found!")
        return

    with open(js_file, 'r', encoding='utf-8') as f:
        content = f.read()

    sync_func_start = content.find('async syncFromFirebase() {')
    if sync_func_start == -1:
        print("Could not find syncFromFirebase in app.js")
        return

    if "collection('incidents')" in content[sync_func_start:sync_func_start+1000]:
        print("Incidents sync already exists.")
        return

    # Find the end of the window.db block to append our listener
    eval_listener_end = content.find('});', sync_func_start) + 3

    new_listener = """
          // Listen to panics (incidents)
          window.db.collection('incidents').where('type', '==', 'ALERTA_MOTORISTA').onSnapshot(snapshot => {
              let rapidReports = JSON.parse(localStorage.getItem('GENERAL_RAPID_REPORTS') || '[]');
              let changed = false;
              
              snapshot.docChanges().forEach(change => {
                  if (change.type === 'added') {
                      const data = change.doc.data();
                      
                      // Verifica se já não existe no rapidReports (baseado na data aproximada ou id)
                      const exists = rapidReports.find(r => r.id === data.id);
                      if (!exists) {
                          const report = {
                              id: data.id,
                              type: 'PÂNICO - ' + (data.driverName || 'Motorista'),
                              location: data.location || 'GPS Indisponível',
                              timestamp: data.date || new Date().toISOString()
                          };
                          rapidReports.push(report);
                          changed = true;
                          
                          App.showToast(`🚨 ALERTA PÂNICO: ${data.driverName} (GPS: ${data.location})`, 'error');
                      }
                  }
              });
              
              if (changed) {
                  localStorage.setItem('GENERAL_RAPID_REPORTS', JSON.stringify(rapidReports));
                  if (App.currentTab === 'dashboard') {
                      App.renderRiskDashboard();
                  }
              }
          });
"""
    # Insert it right after the first snapshot inside `if (window.db) {`
    if eval_listener_end != -1:
        content = content[:eval_listener_end] + "\n" + new_listener + content[eval_listener_end:]
        
        with open(js_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Patched app.js successfully!")

if __name__ == "__main__":
    patch_app_js()
