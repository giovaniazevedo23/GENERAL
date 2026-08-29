import codecs

target_file = r'c:\Users\giova\.gemini\antigravity\scratch\general-app\js\app.js'

with codecs.open(target_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix in triggerPlanAnalysis (around line 1389)
old_code_1 = """          const routeData = await window.LocationService.calculateRoute(originCoords, destCoords);
          
          if (routeData) {"""

new_code_1 = """          let routeData = await window.LocationService.calculateRoute(originCoords, destCoords);
          if (Array.isArray(routeData) && routeData.length > 0) routeData = routeData[0];
          
          if (routeData) {"""

content = content.replace(old_code_1, new_code_1)

# Fix in runAWS_AIRouting (around line 1677)
old_code_2 = """        const routeData = await window.LocationService.calculateRoute(originCoords, destCoords);
        if (routeData) {"""

new_code_2 = """        let routeData = await window.LocationService.calculateRoute(originCoords, destCoords);
        if (Array.isArray(routeData) && routeData.length > 0) routeData = routeData[0];
        
        if (routeData) {"""

content = content.replace(old_code_2, new_code_2)

with codecs.open(r'c:\Users\giova\.gemini\antigravity\scratch\general-app\js\app.js', 'w', encoding='utf-8') as f:
    f.write(content)

with codecs.open(r'c:\Users\giova\.gemini\antigravity\scratch\general-app\www\js\app.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Array fix applied successfully.")
