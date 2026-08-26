import os

with open('index.html', 'r', encoding='utf-8') as f:
    current_html = f.read()

with open('www/index.html', 'r', encoding='utf-8') as f:
    www_html = f.read()

insert_idx = current_html.find('<!-- MOCK GOOGLE LOGIN MODAL -->')

top_part = current_html[:insert_idx]
bottom_part = current_html[insert_idx:]

start_missing_idx = www_html.find('<!-- ============================================== -->\n      <!-- VIEW: PRODUTOS PERIGOSOS (ONU / HAZMAT) -->')

end_missing_idx = www_html.find('<!-- SCRIPTS DA APLICAÇÃO')

missing_content = www_html[start_missing_idx:end_missing_idx]

with open('index.html', 'w', encoding='utf-8') as out:
    out.write(top_part + missing_content + bottom_part)
print(f'Successfully restored missing HTML! Restored {len(missing_content)} characters.')
