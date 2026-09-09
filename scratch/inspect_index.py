import chardet

with open('index.html', 'rb') as f:
    raw = f.read(100000)

result = chardet.detect(raw)
print(f"Detected encoding: {result}")

with open('index.html', 'rb') as f:
    raw = f.read()

enc = result['encoding'] if result['encoding'] else 'utf-8'

try:
    content = raw.decode(enc)
    print(f"File length: {len(content)} characters")
    
    import re
    nav_items = re.findall(r'<button[^>]*onclick="App\.switchTab\([^>]*>', content)
    print("Found tabs:")
    for item in set(nav_items):
        print(item[:100] + "...")
        
except Exception as e:
    print(f"Error decoding: {e}")
