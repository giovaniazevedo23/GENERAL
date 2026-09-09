import re

def patch_motorista_html(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add face-api.js script tag if not present
    face_api_script = '<script defer src="https://cdn.jsdelivr.net/npm/face-api.js@0.22.2/dist/face-api.min.js"></script>'
    driver_monitor_script = '<script src="js/driver-monitor.js"></script>'
    
    if face_api_script not in content:
        # Add after other scripts at the bottom
        content = content.replace('<script src="js/app_motorista.js?v=6.0.0"></script>', f'{face_api_script}\n  {driver_monitor_script}\n  <script src="js/app_motorista.js?v=7.0.0"></script>')
        content = content.replace('<script src="js/app_motorista.js?v=7.0.0"></script>', f'{face_api_script}\n  {driver_monitor_script}\n  <script src="js/app_motorista.js?v=7.0.0"></script>')
    
    # 2. Add the monitoring overlay
    overlay_html = """
  <!-- Driver Monitoring Overlay -->
  <div id="driver-monitoring-overlay" class="hidden fixed inset-0 z-50 bg-slate-950/95 backdrop-blur-md flex flex-col items-center justify-center p-4">
    <div class="absolute top-6 left-6 flex items-center gap-3">
      <div class="w-12 h-12 rounded-xl bg-slate-900 border border-slate-700 flex items-center justify-center shadow-lg">
        <i data-lucide="shield-check" class="w-6 h-6 text-emerald-500" id="monitor-shield-icon"></i>
      </div>
      <div>
        <h2 class="text-white font-black text-lg">Segurança Ativa</h2>
        <p id="monitor-status-text" class="text-emerald-400 text-xs font-bold uppercase tracking-widest">Rosto Detectado</p>
      </div>
    </div>
    
    <div class="absolute top-6 right-6">
      <div class="bg-slate-900 border border-slate-800 px-4 py-2 rounded-xl shadow-lg flex items-center gap-3">
        <i data-lucide="heart-pulse" class="w-5 h-5 text-rose-500 animate-pulse" id="bpm-icon"></i>
        <div class="flex flex-col">
          <span class="text-slate-400 text-[10px] uppercase font-bold tracking-wider">BPM Simulado</span>
          <span id="bpm-value" class="text-white font-black text-xl leading-none">--</span>
        </div>
      </div>
    </div>

    <!-- Camera Container -->
    <div class="relative w-full max-w-sm aspect-[3/4] bg-black rounded-3xl overflow-hidden border-4 border-slate-800 shadow-2xl mt-12">
      <video id="monitor-video" autoplay muted playsinline class="absolute inset-0 w-full h-full object-cover"></video>
      <canvas id="monitor-canvas" class="absolute inset-0 w-full h-full pointer-events-none"></canvas>
      
      <!-- Warning Overlay (Hidden by default) -->
      <div id="monitor-warning" class="hidden absolute inset-0 bg-rose-600/90 flex flex-col items-center justify-center z-10">
        <i data-lucide="alert-triangle" class="w-16 h-16 text-white mb-4 animate-bounce"></i>
        <h3 class="text-white font-black text-2xl uppercase text-center px-4">Atenção!</h3>
        <p class="text-white/90 text-sm font-bold text-center mt-2 px-6">Rosto não detectado.<br>Por favor, olhe para a câmera.</p>
      </div>
    </div>

    <!-- Controls -->
    <div class="absolute bottom-10 w-full px-6 max-w-sm flex flex-col gap-3">
      <button onclick="if(window.DriverMonitor) DriverMonitor.stop()" class="w-full bg-slate-800 hover:bg-slate-700 text-white font-bold py-4 rounded-2xl border border-slate-700 transition-all flex items-center justify-center gap-2 shadow-lg">
        <i data-lucide="pause-circle" class="w-5 h-5"></i>
        Pausar Monitoramento
      </button>
    </div>
  </div>
  """
    if 'driver-monitoring-overlay' not in content:
        # Insert right before the body closes or before bottom navigation
        content = content.replace('</body>', overlay_html + '\n</body>')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Patched {filepath}")

patch_motorista_html('../gestor-app/motorista.html')
