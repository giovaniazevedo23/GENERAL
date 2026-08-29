import codecs

target_file = r'c:\Users\giova\.gemini\antigravity\scratch\general-app\original_app.js'

with codecs.open(target_file, 'r', encoding='utf-16le') as f:
    content = f.read()

# Fix 1
orig_fix1 = """        // Geocodificação Origem
        const originRef = document.getElementById('plan-origin-ref').value;
        const originQuery = originRef ? `${originRef}, ${plan.origin}` : plan.origin;
        const originCoords = await window.LocationService.geocode(originQuery);
        
        // Geocodificação Destino
        const destRef = document.getElementById('plan-dest-ref').value;
        const destQuery = destRef ? `${destRef}, ${plan.destination}` : plan.destination;
        const destCoords = await window.LocationService.geocode(destQuery);"""

new_fix1 = """        // Geocodificação Origem
        const originQuery = plan.origin.replace(' - ', ', ');
        const originCoords = await window.LocationService.geocode(originQuery);
        
        // Geocodificação Destino
        const destQuery = plan.destination.replace(' - ', ', ');
        const destCoords = await window.LocationService.geocode(destQuery);"""

content = content.replace(orig_fix1, new_fix1)

# Fix 2
orig_fix2 = """        // Query formatação: CEP, Cidade, Estado, Brasil
        const originQuery = originRef ? `${originRef}, ${originCity}, ${originState}, Brazil` : `${originCity}, ${originState}, Brazil`;
        const originCoords = await window.LocationService.geocode(originQuery);
        
        const destQuery = destRef ? `${destRef}, ${destCity}, ${destState}, Brazil` : `${destCity}, ${destState}, Brazil`;
        const destCoords = await window.LocationService.geocode(destQuery);"""

new_fix2 = """        // Query formatação: CEP, Cidade, Estado, Brasil
        const originQuery = originRef ? `${originRef}, ${originCity}, ${originState}, Brazil` : `${originCity}, ${originState}, Brazil`;
        let originCoords = await window.LocationService.geocode(originQuery);
        if (!originCoords && originRef) {
          originCoords = await window.LocationService.geocode(`${originCity}, ${originState}, Brazil`);
        }
        
        const destQuery = destRef ? `${destRef}, ${destCity}, ${destState}, Brazil` : `${destCity}, ${destState}, Brazil`;
        let destCoords = await window.LocationService.geocode(destQuery);
        if (!destCoords && destRef) {
          destCoords = await window.LocationService.geocode(`${destCity}, ${destState}, Brazil`);
        }"""

content = content.replace(orig_fix2, new_fix2)

with codecs.open(r'c:\Users\giova\.gemini\antigravity\scratch\general-app\js\app.js', 'w', encoding='utf-8') as f:
    f.write(content)

with codecs.open(r'c:\Users\giova\.gemini\antigravity\scratch\general-app\www\js\app.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("App.js patched successfully.")
