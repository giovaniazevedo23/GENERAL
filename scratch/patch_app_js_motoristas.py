import re

with open('js/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

new_methods = """
  // --- GESTÃO DE MOTORISTAS ---
  showDriverModal() {
    const modal = document.getElementById('driver-modal');
    if(modal) {
        modal.classList.remove('opacity-0', 'pointer-events-none');
        document.getElementById('driver-modal-content').classList.remove('scale-95');
        this.setDriverType('vinculado'); // default
    }
  },
  hideDriverModal() {
    const modal = document.getElementById('driver-modal');
    if(modal) {
        modal.classList.add('opacity-0', 'pointer-events-none');
        document.getElementById('driver-modal-content').classList.add('scale-95');
        // Clear inputs
        document.getElementById('driver-name').value = '';
        document.getElementById('driver-cpf').value = '';
        document.getElementById('driver-cnpj').value = '';
    }
  },
  setDriverType(type) {
    this.driverType = type;
    const btnVinc = document.getElementById('btn-driver-type-vinculado');
    const btnAuto = document.getElementById('btn-driver-type-autonomo');
    const labelCnpj = document.getElementById('label-driver-cnpj');
    
    if(type === 'vinculado') {
        btnVinc.className = 'bg-blue-600 text-white text-sm font-bold py-2 rounded-lg border border-blue-500 transition-all';
        btnAuto.className = 'bg-slate-800 text-slate-400 text-sm font-bold py-2 rounded-lg border border-slate-700 transition-all hover:bg-slate-700 hover:text-slate-300';
        labelCnpj.innerText = 'CNPJ da sua Empresa';
    } else {
        btnAuto.className = 'bg-blue-600 text-white text-sm font-bold py-2 rounded-lg border border-blue-500 transition-all';
        btnVinc.className = 'bg-slate-800 text-slate-400 text-sm font-bold py-2 rounded-lg border border-slate-700 transition-all hover:bg-slate-700 hover:text-slate-300';
        labelCnpj.innerText = 'CNPJ do Contratante';
    }
  },
  saveDriver() {
    const name = document.getElementById('driver-name').value.trim();
    const cpf = document.getElementById('driver-cpf').value.trim();
    const cnpj = document.getElementById('driver-cnpj').value.trim();
    
    if(!name || !cpf || !cnpj) {
        this.showToast('Preencha todos os campos do motorista.', 'error');
        return;
    }
    
    let drivers = JSON.parse(localStorage.getItem('GENERAL_DRIVERS') || '[]');
    drivers.push({
        id: Date.now(),
        type: this.driverType,
        name,
        cpf,
        cnpj,
        status: 'Ativo'
    });
    localStorage.setItem('GENERAL_DRIVERS', JSON.stringify(drivers));
    
    this.hideDriverModal();
    this.showToast('Motorista cadastrado com sucesso!');
    this.renderDriversList();
  },
  renderDriversList() {
    const list = document.getElementById('drivers-list');
    if(!list) return;
    
    const drivers = JSON.parse(localStorage.getItem('GENERAL_DRIVERS') || '[]');
    if(drivers.length === 0) {
        list.innerHTML = '<div class="col-span-2 p-4 border border-slate-800 border-dashed rounded-xl text-center text-slate-500 text-sm">Nenhum motorista cadastrado ainda.</div>';
        return;
    }
    
    list.innerHTML = drivers.map(d => `
        <div class="bg-slate-900 border border-slate-800 p-3 rounded-xl flex flex-col justify-between hover:border-slate-700 transition-colors">
            <div>
                <div class="flex items-center justify-between mb-2">
                    <span class="text-xs font-bold text-white">${d.name}</span>
                    <span class="text-[9px] font-bold px-1.5 py-0.5 rounded uppercase ${d.type === 'vinculado' ? 'bg-blue-900/30 text-blue-400 border border-blue-800' : 'bg-amber-900/30 text-amber-400 border border-amber-800'}">${d.type}</span>
                </div>
                <div class="text-[10px] text-slate-400 space-y-0.5 font-mono">
                    <p>CPF: ${d.cpf}</p>
                    <p>CNPJ: ${d.cnpj}</p>
                </div>
            </div>
            <div class="mt-3 pt-3 border-t border-slate-800 flex items-center justify-between">
                <span class="text-[10px] text-emerald-400 flex items-center gap-1"><i data-lucide="check-circle" class="w-3 h-3"></i> ${d.status}</span>
                <button onclick="App.showToast('Função de edição em breve.')" class="text-slate-500 hover:text-blue-400"><i data-lucide="edit" class="w-3 h-3"></i></button>
            </div>
        </div>
    `).join('');
    
    if(window.lucide && window.lucide.createIcons) window.lucide.createIcons();
  },
  
  // --- MONITORAMENTO AO VIVO ---
  initLiveMonitoring() {
    if(!this.monitoringChannel) {
        this.monitoringChannel = new BroadcastChannel('general_monitoring_channel');
        this.monitoringChannel.onmessage = (event) => {
            this.handleLiveMonitoringData(event.data);
        };
    }
  },
  handleLiveMonitoringData(data) {
    const idleContainer = document.getElementById('idle-monitoring-container');
    const liveContainer = document.getElementById('live-monitoring-container');
    const noSignal = document.getElementById('no-signal-overlay');
    const alertCritical = document.getElementById('live-vital-alert');
    const videoElem = document.getElementById('manager-live-video');
    
    if(!liveContainer) return;
    
    if(data.type === 'route_started') {
        idleContainer.classList.add('hidden');
        liveContainer.classList.remove('hidden');
        document.getElementById('live-driver-name').innerText = data.driverName || 'Motorista Desconhecido';
        document.getElementById('live-route-code').innerText = data.routeCode || 'Rota ' + Math.floor(Math.random()*1000);
    }
    else if(data.type === 'route_ended') {
        idleContainer.classList.remove('hidden');
        liveContainer.classList.add('hidden');
        videoElem.srcObject = null;
    }
    else if(data.type === 'telemetry') {
        // GPS
        if(data.location) {
            document.getElementById('live-location').innerText = `Lat: ${data.location.lat.toFixed(4)} Lng: ${data.location.lng.toFixed(4)}`;
        }
        
        // Batimentos
        if(data.heartRate) {
            const hrElem = document.getElementById('live-heart-rate');
            hrElem.innerHTML = `${data.heartRate} <span class="text-[10px] font-normal text-slate-500">BPM</span>`;
            
            if(data.heartRate < 50 || data.heartRate > 120) {
                hrElem.classList.replace('text-white', 'text-rose-500');
                alertCritical.classList.remove('hidden');
            } else {
                hrElem.classList.replace('text-rose-500', 'text-white');
                alertCritical.classList.add('hidden');
            }
        }
        
        // Video Stream
        // For a local demo, we pass the frame as dataURL or rely on WebRTC. 
        // BroadcastChannel passing dataURL frames at low FPS is good enough for a demo.
        if(data.videoFrame) {
            noSignal.classList.add('hidden');
            // Instead of srcObject, we can use a canvas or update poster
            // To make it easy, we'll set it as a background image of the video parent, or just an img tag.
            // Let's replace the video element with an image if it's not already.
            let imgElem = document.getElementById('manager-live-img');
            if(!imgElem) {
                videoElem.style.display = 'none';
                imgElem = document.createElement('img');
                imgElem.id = 'manager-live-img';
                imgElem.className = 'w-full h-full object-cover';
                videoElem.parentElement.appendChild(imgElem);
            }
            imgElem.src = data.videoFrame;
        }
    }
  }
"""

if "renderDriversList" not in content:
    # Insert before the last `};`
    last_brace_idx = content.rfind('};')
    
    new_content = content[:last_brace_idx] + ",\n" + new_methods + "\n" + content[last_brace_idx:]
    
    # Also hook initLiveMonitoring and renderDriversList into init() or switchTab
    # We can just put them in App.init()
    if 'App.init();' in new_content:
        # Actually it's better to hook it inside init()
        init_hook = "    this.renderDriversList();\n    this.initLiveMonitoring();\n"
        new_content = new_content.replace('init() {', 'init() {\n' + init_hook, 1)

    with open('js/app.js', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Patched js/app.js successfully")
else:
    print("Methods already exist in js/app.js")

