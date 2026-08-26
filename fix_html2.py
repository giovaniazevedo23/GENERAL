import os

with open('index.html', 'r', encoding='utf-8') as f:
    current_html = f.read()

with open('www/index.html', 'r', encoding='utf-8') as f:
    www_html = f.read()

insert_idx = current_html.find('<!-- MOCK GOOGLE LOGIN MODAL -->')
if insert_idx == -1:
    print('Could not find insert index')
    exit(1)

top_part = current_html[:insert_idx]
bottom_part = current_html[insert_idx:]

hazmat_start_idx = www_html.find('<!-- ============================================== -->\n      <!-- VIEW: PRODUTOS PERIGOSOS (ONU / HAZMAT) -->')
if hazmat_start_idx == -1:
    print('Could not find hazmat start index')
    exit(1)

scripts_core_idx = www_html.find('<!-- Scripts Core -->')
if scripts_core_idx == -1:
    print('Could not find scripts core index')
    exit(1)

missing_views_and_modals = www_html[hazmat_start_idx:scripts_core_idx]

# Check if there are duplicate modals now:
# current_html already has new-communication-modal?
# Actually, www/index.html might have new-communication-modal too.
# Let's verify what missing_views_and_modals contains.
# It should contain everything from hazmat to the end.
# If current_html already contains new-communication-modal, we might have duplicates.

with open('index_fixed.html', 'w', encoding='utf-8') as out:
    out.write(top_part + missing_views_and_modals + bottom_part)
print(f'Merged successfully. Original size: {len(current_html)}. New size: {len(top_part) + len(missing_views_and_modals) + len(bottom_part)}')
