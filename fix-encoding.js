const fs = require('fs');
let data = fs.readFileSync('js/app.js', 'utf8');
data = data.replace(/<h2 class="font-bold text-rose-900 uppercase text-xs mb-1">.* Perigos/g, '<h2 class="font-bold text-rose-900 uppercase text-xs mb-1">&#9888;&#65039; Perigos');
fs.writeFileSync('js/app.js', data);

let wwwData = fs.readFileSync('www/js/app.js', 'utf8');
wwwData = wwwData.replace(/<h1 class="text-lg font-black tracking-wider text-blue-900 uppercase">GENERAL .* Folha/g, '<h1 class="text-lg font-black tracking-wider text-blue-900 uppercase">GENERAL &bull; Folha');
wwwData = wwwData.replace(/<h2 class="font-bold text-rose-900 uppercase text-xs mb-1">.* Perigos/g, '<h2 class="font-bold text-rose-900 uppercase text-xs mb-1">&#9888;&#65039; Perigos');
wwwData = wwwData.replace(/<h2 class="font-bold text-blue-900 uppercase text-xs mb-1">.* Recomendações/g, '<h2 class="font-bold text-blue-900 uppercase text-xs mb-1">&#128161; Recomendações');
fs.writeFileSync('www/js/app.js', wwwData);

console.log("Done replacing.");
