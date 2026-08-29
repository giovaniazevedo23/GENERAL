const fs = require('fs');

let appJs = fs.readFileSync('js/app.js', 'utf8');

// Fix encodings
appJs = appJs.replace(/â€¢/g, '•').replace(/âš ï¸/g, '⚠️').replace(/ðŸ’¡/g, '💡');

// Replace AWSLocation with LocationService entirely
appJs = appJs.replace(/window\.AWSLocation/g, 'window.LocationService');
appJs = appJs.replace(/Erro AWS Location/g, 'Erro Google Location');
appJs = appJs.replace(/Previsão AWS/g, 'Previsão Google');
appJs = appJs.replace(/Módulo AWS Location/g, 'Módulo Google Location');

// 1. Add route rendering logic to the App object
const renderRoutesLogic = `
  renderRouteOptionsUI(routesList) {
    let container = document.getElementById('route-options-container');
    if (!container) {
      const mapContainer = document.getElementById('planner-map-container');
      if (mapContainer) {
        container = document.createElement('div');
        container.id = 'route-options-container';
        container.className = 'w-full mt-3 flex flex-col gap-2';
        mapContainer.parentNode.insertBefore(container, mapContainer.nextSibling);
      }
    }
    
    if (container) {
      container.innerHTML = '<h3 class="text-slate-300 font-bold text-sm">Opções de Rota:</h3>';
      routesList.forEach(route => {
        const totalHours = route.durationSeconds / 3600;
        const formattedTime = \`\${Math.floor(totalHours)}h \${Math.round((totalHours % 1) * 60)}m\`;
        
        const btn = document.createElement('button');
        btn.className = \`text-left p-3 rounded-lg border transition-all \${route.isMain ? 'bg-blue-600 border-blue-500 text-white' : 'bg-slate-800 border-slate-700 text-slate-300 hover:bg-slate-700'}\`;
        btn.innerHTML = \`
          <div class="flex justify-between items-center">
            <div class="font-bold">\${route.name}</div>
            <div class="\${route.isMain ? 'text-blue-200' : 'text-emerald-400'} font-mono text-xs">\${formattedTime}</div>
          </div>
          <div class="text-xs mt-1 \${route.isMain ? 'text-blue-100' : 'text-slate-400'}">\${route.distanceKm.toFixed(1)} km</div>
        \`;
        
        btn.onclick = (e) => {
          e.preventDefault();
          window.dispatchEvent(new CustomEvent('routeSelected', { detail: { routeId: route.id } }));
        };
        container.appendChild(btn);
      });
    }
  },

  applySelectedRouteToForm(route) {
    document.getElementById('plan-dist').value = Math.round(route.distanceKm);
    
    const totalHours = route.durationSeconds / 3600;
    const predictedDays = Math.ceil(totalHours / 8);
    const formattedTime = \`\${Math.floor(totalHours)}h \${Math.round((totalHours % 1) * 60)}m\`;
    
    const durationInput = document.getElementById('plan-duration');
    if (durationInput) {
      durationInput.value = \`\${formattedTime} (\${predictedDays} dia\${predictedDays > 1 ? 's' : ''} de viagem estimad\${predictedDays > 1 ? 'os' : 'o'})\`;
    }
    this.simulateFuelCost();
  },
`;

appJs = appJs.replace(/calculateDeadline\(\) \{/, renderRoutesLogic + '\n  calculateDeadline() {');

// 2. Replace routing logic safely (without deleting the closing brace or the Gemini logic)
const calcPrevisionOld = `const routeData = await window.LocationService.calculateRoute(originCoords, destCoords);
          
          if (routeData) {
            document.getElementById('plan-dist').value = Math.round(routeData.distanceKm);
            
            // Regra de Negócio (Previsão de Dias)
            const totalHours = routeData.durationSeconds / 3600;
            const predictedDays = Math.ceil(totalHours / 8);
            const formattedTime = \`\${Math.floor(totalHours)}h \${Math.round((totalHours % 1) * 60)}m\`;
            
            const durationInput = document.getElementById('plan-duration');
            if (durationInput) {
              durationInput.value = \`\${formattedTime} (\${predictedDays} dia\${predictedDays > 1 ? 's' : ''} de viagem estimad\${predictedDays > 1 ? 'os' : 'o'})\`;
            }`;

const calcPrevisionNew = `const routesList = await window.LocationService.calculateRoute(originCoords, destCoords);
          
          if (routesList && routesList.length > 0) {
            window.currentRoutesList = routesList;
            const routeData = routesList.find(r => r.isMain) || routesList[0];
            this.applySelectedRouteToForm(routeData);
            this.renderRouteOptionsUI(routesList);
            
            // Regra de Negócio (Previsão de Dias) mantida para o Gemini abaixo`;

appJs = appJs.replace(calcPrevisionOld, calcPrevisionNew);

const mapRenderOld1 = `if (routeData.geometry && routeData.geometry.length > 0) {
              window.plannerMapController.drawRoute(routeData.geometry);
            } else {
              window.plannerMapController.updateMapLocation(originCoords[0], originCoords[1]);
            }`;
const mapRenderNew1 = `window.plannerMapController.drawRoutes(routesList);`;
appJs = appJs.replace(mapRenderOld1, mapRenderNew1);


// 3. Replace runGoogle_AIRouting logic (now runAWS_AIRouting probably)
const runOld = `const routeData = await window.LocationService.calculateRoute(originCoords, destCoords);
        if (routeData) {
          document.getElementById('plan-dist').value = Math.round(routeData.distanceKm);
          
          const totalHours = routeData.durationSeconds / 3600;
          const predictedDays = Math.floor(totalHours / 8); // Assuming 8 hours of driving per day
          const remainingHours = Math.round(totalHours % 8);
          
          const durationInput = document.getElementById('plan-duration');
          if (durationInput) {
            let durText = '';
            if (predictedDays > 0) durText += \`\${predictedDays} dias \`;
            if (remainingHours > 0 || predictedDays === 0) durText += \`\${remainingHours} horas\`;
            durationInput.value = durText.trim();
          }

          // Atualizar Custo de Combustível
          this.simulateFuelCost();`;

const runNew = `const routesList = await window.LocationService.calculateRoute(originCoords, destCoords);
        if (routesList && routesList.length > 0) {
          window.currentRoutesList = routesList;
          const routeData = routesList.find(r => r.isMain) || routesList[0];
          this.applySelectedRouteToForm(routeData);
          this.renderRouteOptionsUI(routesList);`;

appJs = appJs.replace(runOld, runNew);

const mapRenderOld2 = `if (routeData.geometry && routeData.geometry.length > 0) {
              window.plannerMapController.drawRoute(routeData.geometry);
            } else {
              window.plannerMapController.updateMapLocation(originCoords[0], originCoords[1]);
            }`;
const mapRenderNew2 = `window.plannerMapController.drawRoutes(routesList);`;
appJs = appJs.replace(mapRenderOld2, mapRenderNew2);


// Add event listener for routeSelected in bindEvents
const eventListener = `
    window.addEventListener('routeSelected', (e) => {
      const routeId = e.detail.routeId;
      if (window.currentRoutesList) {
        window.currentRoutesList.forEach(r => r.isMain = (r.id === routeId));
        this.renderRouteOptionsUI(window.currentRoutesList);
        if (window.plannerMapController) window.plannerMapController.drawRoutes(window.currentRoutesList);
        const activeRoute = window.currentRoutesList.find(r => r.isMain);
        if(activeRoute) this.applySelectedRouteToForm(activeRoute);
      }
    });
`;
appJs = appJs.replace(/bindEvents\(\) \{/, 'bindEvents() {' + eventListener);

fs.writeFileSync('js/app.js', appJs);
console.log("app.js patched safely.");
