import urllib.request
import urllib.parse
import json

def geocode(query):
    url = f"https://nominatim.openstreetmap.org/search?format=json&q={urllib.parse.quote(query)}&limit=1"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            if data:
                return [float(data[0]['lat']), float(data[0]['lon'])]
    except Exception as e:
        print("Error:", e)
    return None

def route(origin, dest):
    url = f"https://router.project-osrm.org/route/v1/driving/{origin[1]},{origin[0]};{dest[1]},{dest[0]}?overview=full&geometries=geojson&steps=false"
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print("Route error:", e)
        return None

print("Geocoding Origin with CEP:")
orig = geocode("64034-827, Teresina, Piauí, Brazil")
print("Orig with CEP:", orig)
if not orig:
    print("Geocoding Origin without CEP:")
    orig = geocode("Teresina, Piauí, Brazil")
    print("Orig without CEP:", orig)

print("Geocoding Dest with CEP:")
dest = geocode("39790-97, Água Boa, Minas Gerais, Brazil")
print("Dest with CEP:", dest)
if not dest:
    print("Geocoding Dest without CEP:")
    dest = geocode("Água Boa, Minas Gerais, Brazil")
    print("Dest without CEP:", dest)

if orig and dest:
    print("Routing:")
    r = route(orig, dest)
    if r:
        print(r.get('code', r))
    else:
        print("Routing failed.")
