const { app, BrowserWindow, Menu, ipcMain, shell, dialog } = require('electron');
const path = require('path');

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1366,
    height: 868,
    minWidth: 375,
    minHeight: 600,
    title: "GENERAL — Gestão Logística & IA Preditiva",
    icon: path.join(__dirname, 'icons', 'icon-512.png'),
    backgroundColor: '#080c14',
    show: false,
    autoHideMenuBar: true,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: false,
      contextIsolation: true,
      webSecurity: true,
      devTools: true
    }
  });

  // Remove menu bar padrão do sistema para visual 100% nativo
  Menu.setApplicationMenu(null);

  // Carrega o arquivo html nativo da aplicação
  mainWindow.loadFile(path.join(__dirname, 'index.html'));

  // Exibe a janela assim que estiver pronta para evitar flicker
  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
    mainWindow.focus();
  });

  // Garante que links externos (WhatsApp, etc) abram no navegador do SO
  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    if (url.startsWith('http:') || url.startsWith('https:') || url.startsWith('mailto:') || url.startsWith('https://wa.me/')) {
      shell.openExternal(url);
      return { action: 'deny' };
    }
    return { action: 'allow' };
  });

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

// Inicialização do aplicativo nativo
app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

// IPC Communication Handlers
ipcMain.handle('get-app-version', () => app.getVersion());

ipcMain.handle('show-alert-dialog', async (event, message) => {
  if (!mainWindow) return;
  return await dialog.showMessageBox(mainWindow, {
    type: 'info',
    title: 'GENERAL',
    message: message,
    buttons: ['OK']
  });
});
