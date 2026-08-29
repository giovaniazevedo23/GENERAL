import urllib.request
import json

url = "https://router.project-osrm.org/route/v1/driving/-42.80194,-5.08917;-41.091504,-3.5667684?overview=full&geometries=geojson&steps=false"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        print("OSRM Success:", json.loads(response.read().decode())['code'])
except Exception as e:
    print("OSRM Error:", str(e))
