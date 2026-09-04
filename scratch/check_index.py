html = open('../index.html', 'rb').read().decode('utf-8', errors='replace')
lines = html.split('\n')
for i, line in enumerate(lines):
    if '\ufffd' in line:
        print(f"{i}: {line.replace('\ufffd', '?').strip()}")
