import re

with open('index.html', 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")
for i, line in enumerate(lines):
    if 'switchTab' in line or 'sidebar' in line.lower() or 'nav' in line.lower():
        print(f"Line {i+1}: {line.strip()[:150]}")
