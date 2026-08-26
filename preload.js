const { contextBridge, ipcRenderer } = require('electron');

// Expor ponte segura de APIs Nativas do SO para o aplicativo frontend
contextBridge.exposeInMainWorld('electronAPI', {
  isNativeApp: true,
  getAppVersion: () => ipcRenderer.invoke('get-app-version'),
  showAlertDialog: (msg) => ipcRenderer.invoke('show-alert-dialog', msg)
});

console.log('⚡ GENERAL Preload Nativo ativado com sucesso.');
