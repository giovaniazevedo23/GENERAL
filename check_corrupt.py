with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

weird = []
lines = text.split('\n')
for i, line in enumerate(lines):
    # Search for specific broken characters that might have bypassed ftfy
    if 'Ã' in line or 'â' in line or '¢' in line or '¼' in line:
        weird.append((i+1, line.strip()))

for i, w in weird[:20]:
    print(f"{i}: {w}")
