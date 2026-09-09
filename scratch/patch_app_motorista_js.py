import re

with open('js/app_motorista.js', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

new_methods = """
  // --- NOVO LOGIN CPF / AUTÔNOMO ---
  setLoginType(type) {
    this.loginType = type;
    const btnVinc = document.getElementById('btn-login-vinculado');
    const btnAuto = document.getElementById('btn-login-autonomo');
    const fieldName = document.getElementById('field-driver-name');
    const fieldCnpj = document.getElementById('field-driver-cnpj');
    
    if(type === 'vinculado') {
        btnVinc.className = 'bg-blue-600 text-white text-sm font-bold py-2 rounded-lg border border-blue-500 transition-all';
        btnAuto.className = 'bg-slate-800 text-slate-400 text-sm font-bold py-2 rounded-lg border border-slate-700 transition-all hover:bg-slate-700 hover:text-slate-300';
        fieldName.classList.add('hidden');
        fieldCnpj.classList.add('hidden');
    } else {
        btnAuto.className = 'bg-blue-600 text-white text-sm font-bold py-2 rounded-lg border border-blue-500 transition-all';
        btnVinc.className = 'bg-slate-800 text-slate-400 text-sm font-bold py-2 rounded-lg border border-slate-700 transition-all hover:bg-slate-700 hover:text-slate-300';
        fieldName.classList.remove('hidden');
        fieldCnpj.classList.remove('hidden');
    }
  },
  
  loginDriver() {
    const type = this.loginType || 'vinculado';
    const cpf = document.getElementById('login-cpf').value.trim();
    
    if(!cpf) {
        this.showToast('Por favor, digite seu CPF.', 'error');
        return;
    }
    
    // Check if we are simulating database via localStorage
    const drivers = JSON.parse(localStorage.getItem('GENERAL_DRIVERS') || '[]');
    let driverData = null;
    
    if(type === 'vinculado') {
        driverData = drivers.find(d => d.cpf === cpf && d.type === 'vinculado');
        if(!driverData) {
            // For demo purposes, we will allow login anyway if not strict, but let's be strict
            // If empty, auto-register as mock
            driverData = { id: Date.now(), name: 'Motorista Mock', cpf, cnpj: '00.000.000/0001-00', type: 'vinculado' };
            this.showToast('CPF não encontrado, mas login liberado para demonstração.', 'warning');
        }
    } else {
        const name = document.getElementById('login-name').value.trim();
        const cnpj = document.getElementById('login-cnpj').value.trim();
        if(!name || !cnpj) {
            this.showToast('Preencha Nome e CNPJ.', 'error');
            return;
        }
        driverData = { id: Date.now(), name, cpf, cnpj, type: 'autonomo' };
        
        // Auto register in Gestor Panel
        drivers.push(driverData);
        localStorage.setItem('GENERAL_DRIVERS', JSON.stringify(drivers));
    }
    
    appState.currentUser = driverData;
    localStorage.setItem('general_user', JSON.stringify(driverData));
    
    document.getElementById('login-overlay').classList.add('hidden');
    this.showToast(`Bem-vindo, ${driverData.name}!`);
    this.checkAuth(); // Updates UI
  },

  // --- CÂMERA E SINAIS VITAIS ---
  startDriverCamera() {
    if(this.cameraActive) {
        this.stopDriverCamera();
        return;
    }
    
    const container = document.getElementById('driver-camera-container');
    const video = document.getElementById('driver-selfie-video');
    const btnFloat = document.getElementById('btn-start-camera-float');
    
    if(btnFloat) btnFloat.innerHTML = '<i data-lucide="video-off" class="w-5 h-5"></i> Parar Gravação';
    
    navigator.mediaDevices.getUserMedia({ video: { facingMode: 'user' }, audio: false })
    .then(stream => {
        this.cameraActive = true;
        this.videoStream = stream;
        video.srcObject = stream;
        container.classList.remove('hidden');
        container.classList.add('flex');
        
        this.showToast('Câmera ativada. Transmissão iniciada.');
        this.startTelemetryBroadcast(video);
    })
    .catch(err => {
        console.error('Erro na câmera:', err);
        this.showToast('Erro ao acessar câmera.', 'error');
    });
  },
  
  stopDriverCamera() {
    this.cameraActive = false;
    const container = document.getElementById('driver-camera-container');
    const btnFloat = document.getElementById('btn-start-camera-float');
    
    if(this.videoStream) {
        this.videoStream.getTracks().forEach(track => track.stop());
    }
    
    if(this.telemetryInterval) {
        clearInterval(this.telemetryInterval);
    }
    
    container.classList.remove('flex');
    container.classList.add('hidden');
    if(btnFloat) btnFloat.innerHTML = '<i data-lucide="camera" class="w-5 h-5"></i> Iniciar Gravação da Rota';
    
    // Notify Gestor
    if(this.monitoringChannel) {
        this.monitoringChannel.postMessage({ type: 'route_ended' });
    }
  },
  
  startTelemetryBroadcast(videoElement) {
    if(!this.monitoringChannel) {
        this.monitoringChannel = new BroadcastChannel('general_monitoring_channel');
    }
    
    const driverName = appState.currentUser ? appState.currentUser.name : 'Desconhecido';
    
    // Send Start Signal
    this.monitoringChannel.postMessage({ 
        type: 'route_started', 
        driverName, 
        routeCode: 'GNR-' + Math.floor(Math.random() * 90000 + 10000)
    });
    
    // Create a hidden canvas to grab frames
    const canvas = document.createElement('canvas');
    canvas.width = 320;
    canvas.height = 240;
    const ctx = canvas.getContext('2d');
    
    let baseBpm = 75;
    
    this.telemetryInterval = setInterval(() => {
        // Frame
        let frameData = null;
        if (videoElement.readyState === videoElement.HAVE_ENOUGH_DATA) {
            ctx.drawImage(videoElement, 0, 0, canvas.width, canvas.height);
            frameData = canvas.toDataURL('image/jpeg', 0.5); // lower quality for speed
        }
        
        // Mock HR
        // Fluctuates slightly, but if user reported an incident, drop it
        if(appState && appState.isEmergency) {
            baseBpm = Math.max(40, baseBpm - 5); // drops dangerously
        } else {
            baseBpm = 70 + Math.floor(Math.random() * 15);
        }
        
        document.getElementById('driver-local-bpm').innerText = baseBpm + ' bpm';
        if(baseBpm < 50) document.getElementById('driver-local-bpm').classList.replace('text-white', 'text-rose-500');
        
        // GPS (Mock using geolocation if available, else static)
        let loc = { lat: -23.5505 + (Math.random()*0.01), lng: -46.6333 + (Math.random()*0.01) };
        if(appState.currentLocation) {
            loc = appState.currentLocation;
        }
        
        this.monitoringChannel.postMessage({
            type: 'telemetry',
            heartRate: baseBpm,
            location: loc,
            videoFrame: frameData
        });
        
    }, 1000); // Send 1 frame/sec for demo purposes to avoid crashing localStorage/channel
  }
"""

if "startDriverCamera" not in content:
    # Insert before the last `};`
    last_brace_idx = content.rfind('};')
    
    new_content = content[:last_brace_idx] + ",\n" + new_methods + "\n" + content[last_brace_idx:]
    
    # Initialize loginType to vinculado
    if 'init() {' in new_content:
        new_content = new_content.replace('init() {', "init() {\n    this.setLoginType('vinculado');\n", 1)

    with open('js/app_motorista.js', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Patched js/app_motorista.js successfully")
else:
    print("Methods already exist in js/app_motorista.js")

