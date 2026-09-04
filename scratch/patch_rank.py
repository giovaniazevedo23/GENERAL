import re

def patch_index_html():
    with open('../index.html', 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()

    widget_html = """
      <!-- GESTÃO RÁPIDA DE MOTORISTAS -->
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg relative overflow-hidden mt-6">
        <div class="absolute top-0 right-0 w-32 h-32 bg-indigo-500/5 rounded-bl-full pointer-events-none"></div>
        <div class="flex items-center justify-between mb-6">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-xl bg-indigo-500/10 flex items-center justify-center border border-indigo-500/20">
              <i data-lucide="users" class="w-5 h-5 text-indigo-500"></i>
            </div>
            <div>
              <h3 class="text-sm font-black text-white uppercase tracking-wider">Tropa em Campo</h3>
              <p class="text-xs text-slate-400">Patentes e envio de recompensas</p>
            </div>
          </div>
        </div>
        
        <div class="space-y-3" id="driver-rank-container">
          <!-- Mockup para visualização rápida (em prod, carregar do DB) -->
          <div class="flex items-center justify-between p-3 bg-slate-800/50 rounded-xl border border-slate-700/50">
            <div class="flex items-center gap-3">
              <div class="w-8 h-8 rounded-full bg-slate-950 border border-amber-500 flex items-center justify-center">
                <i data-lucide="shield" class="w-4 h-4 text-amber-500"></i>
              </div>
              <div>
                <p class="text-xs font-bold text-white">Carlos Almeida (Transportes S.A.)</p>
                <p class="text-[10px] text-amber-400 font-bold uppercase tracking-widest">Elite</p>
              </div>
            </div>
            <button onclick="if(window.App) App.showToast('Recompensa de +50 XP enviada com sucesso!')" class="bg-indigo-600 hover:bg-indigo-500 text-white p-2 rounded-xl transition-all" title="Enviar Recompensa XP">
              <i data-lucide="gift" class="w-4 h-4"></i>
            </button>
          </div>
          
          <div class="flex items-center justify-between p-3 bg-slate-800/50 rounded-xl border border-slate-700/50">
            <div class="flex items-center gap-3">
              <div class="w-8 h-8 rounded-full bg-slate-950 border border-slate-500 flex items-center justify-center">
                <i data-lucide="shield" class="w-4 h-4 text-slate-400"></i>
              </div>
              <div>
                <p class="text-xs font-bold text-white">José Ferreira (Logística BR)</p>
                <p class="text-[10px] text-slate-400 font-bold uppercase tracking-widest">Veterano</p>
              </div>
            </div>
            <button onclick="if(window.App) App.showToast('Recompensa de +50 XP enviada com sucesso!')" class="bg-indigo-600 hover:bg-indigo-500 text-white p-2 rounded-xl transition-all" title="Enviar Recompensa XP">
              <i data-lucide="gift" class="w-4 h-4"></i>
            </button>
          </div>
        </div>
      </div>
    """
    
    if 'GESTÃO RÁPIDA DE MOTORISTAS' not in html:
        # Insert after TROPA DE ELITE WIDGET or before <!-- KPI Grid -->
        idx = html.find('<!-- KPI Grid -->')
        if idx != -1:
            html = html[:idx] + widget_html + '\n\n' + html[idx:]
            
    with open('../index.html', 'w', encoding='utf-8') as f:
        f.write(html)
        
    print("Rank widget added to index.html")

if __name__ == '__main__':
    patch_index_html()
