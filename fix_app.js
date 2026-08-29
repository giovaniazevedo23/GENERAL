const fs = require('fs');

let code = fs.readFileSync('js/app.js', 'utf8');

// The replacement for calculatePrevisionGoogle block
const regex1 = /if \(routeData\) \{\s*document.getElementById\('plan-dist'\).value = Math.round\(routeData.distanceKm\);[\s\S]*?const durationInput = document.getElementById\('plan-duration'\);[\s\S]*?if \(durationInput\) \{\s*durationInput.value = [^\}]+;\s*\}/;

const repl1 = `if (routesList && routesList.length > 0) {
            window.currentRoutesList = routesList;
            const routeData = routesList.find(r => r.isMain) || routesList[0];
            this.applySelectedRouteToForm(routeData);
            this.renderRouteOptionsUI(routesList);
            const predictedDays = Math.ceil((routeData.durationSeconds / 3600) / 8);`;

code = code.replace(regex1, repl1);

// The replacement for runGoogle_AIRouting block
const regex2 = /if \(routeData\) \{\s*document.getElementById\('plan-dist'\).value = Math.round\(routeData.distanceKm\);[\s\S]*?const durationInput = document.getElementById\('plan-duration'\);[\s\S]*?if \(durationInput\) \{\s*let durText = '';[\s\S]*?durationInput.value = durText.trim\(\);\s*\}[\s\S]*?\/\/ Atualizar Custo de Combustível\s*this.simulateFuelCost\(\);/;

const repl2 = `if (routesList && routesList.length > 0) {
          window.currentRoutesList = routesList;
          const routeData = routesList.find(r => r.isMain) || routesList[0];
          this.applySelectedRouteToForm(routeData);
          this.renderRouteOptionsUI(routesList);`;

code = code.replace(regex2, repl2);

fs.writeFileSync('js/app.js', code);
console.log('Fixed app.js successfully!');
