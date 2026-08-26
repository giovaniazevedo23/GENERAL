# 🛡️ GENERAL — Gestão e Resposta a Acidentes de Cargas (PAAC 360°)

**GENERAL** é um aplicativo de nível corporativo desenvolvido para o gerenciamento estratégico de sinistros rodoviários, resposta imediata (*Golden Hour*), controle de produtos perigosos (HazMat), dimensionamento de transbordo e emissão de dossiês periciais em PDF.

---

## 🌟 Principais Recursos

1. **Dashboard Operacional & Monitoramento em Tempo Real**
   - Mapa georreferenciado interativo (Leaflet) com círculo dinâmico de raio de isolamento.
   - Cálculo dinâmico do **Índice de Risco (0 a 100)** e sugestão da próxima ação prioritária.
   - Cronômetro de SLA de atendimento com alertas visuais e sonoros (Web Audio API).

2. **Wizard da Primeira Hora (*Golden Hour*)**
   - Triagem imediata de segurança humana, sinalização da pista a 200m e isolamento perimetral.
   - Acionamentos com 1 clique (SAMU 192, PRF 191, Bombeiros 193).

3. **Catálogo de Produtos Perigosos (ANTT / ABIQUIM / Nº ONU)**
   - Fichas completas com Número ONU, Número de Risco, Classe, EPIs obrigatórios e procedimentos de contenção e fogo.

4. **Central Multicanal de Disparos**
   - Mensagens formatadas instantâneas para **WhatsApp**, **E-mail oficial para Seguradora**, **Aviso ao Embarcador** e **Comunicação a Órgãos Ambientais (CETESB/IBAMA)**.

5. **Módulo de Transbordo & Salvamento**
   - Cálculo automático de veículos de apoio, bombas de transferência e checklist ambiental.

6. **Investigação de Causa Raiz (RCA)**
   - Diagrama interativo dos **6M de Ishikawa** (Método, Máquina, Mão de Obra, Material, Meio Ambiente, Medição) e técnica dos **5 Porquês**.

7. **Emissor de Dossiê Oficial em PDF**
   - Relatório técnico executivo completo pronto para impressão ou salvar em PDF para auditoria.

---

## 🤖 Projeto Nativo Android (Android Studio & Node.js)

O **GENERAL** possui um projeto nativo Android completo configurado via **Node.js** e **Capacitor**:

1. **Como abrir no Android Studio:**
   - Dê um duplo clique no script: `ABRIR_NO_ANDROID_STUDIO.bat`
   - Ou execute no terminal: `npm run android:open`
   - Ou abra o **Android Studio**, escolha **"Open an Existing Project"** e selecione a pasta: `C:\Users\giova\.gemini\antigravity\scratch\general-app\android`.

2. **Como gerar o arquivo APK nativo:**
   - Com o projeto aberto no Android Studio, vá ao menu superior:
     **Build > Build Bundle(s) / APK(s) > Build APK(s)**
   - O Android Studio gerará o arquivo **`app-debug.apk`** pronto para instalar diretamente em qualquer smartphone Android.

---

## 💻 Aplicativo Nativo Desktop (Windows Executável)

- Dê um duplo clique no atalho **`GENERAL`** na sua Área de Trabalho (`GENERAL.lnk`).
- Ou execute o arquivo `ABRIR_APP_GENERAL.bat`.
- O aplicativo iniciará em uma janela nativa do Windows (via Electron), sem navegador web.

---

## 📱 Instalação como Aplicativo Mobile (PWA)

O **GENERAL** também pode ser instalado como **Progressive Web App (PWA)** direto pelo navegador no Android/iOS:
- **Android:** Toque em "Instalar App" no topo da tela.
- **iPhone / iPad:** No Safari, toque em Compartilhar > "Adicionar à Tela de Início".
