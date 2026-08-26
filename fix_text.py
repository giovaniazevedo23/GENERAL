import os

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace IA Preditiva (Previsão)
html = html.replace('IA Preditiva (Previsão)', 'IA Preditiva')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Replaced IA Preditiva in index.html')
