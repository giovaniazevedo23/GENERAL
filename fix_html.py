import os

with open('index.html', 'r', encoding='utf-8') as f:
    current_html = f.read()

with open('www/index.html', 'r', encoding='utf-8') as f:
    www_html = f.read()

# We need to find the exact place where things were cut off.
# In current_html, we have:
# <!-- VIEW: GOLDEN HOUR (TRIAGEM) -->
# ...
# <!-- MODAL NOVA COMUNICAÇÃO -->
# ...
# <!-- MOCK GOOGLE LOGIN MODAL -->

# Let's extract the Golden hour and New Communication modal from current_html
# Actually, the view-wizard in www/index.html is intact. We can just take everything from www/index.html 
# starting from <!-- ============================================== -->\n      <!-- VIEW: PRODUTOS PERIGOSOS (ONU) -->
# up to the end of the file.

# Then we insert it into current_html right before <!-- MOCK GOOGLE LOGIN MODAL -->.

insert_idx = current_html.find('<!-- MOCK GOOGLE LOGIN MODAL -->')
top_part = current_html[:insert_idx]
bottom_part = current_html[insert_idx:]

hazmat_start_idx = www_html.find('<!-- ============================================== -->\n      <!-- VIEW: PRODUTOS PERIGOSOS (ONU) -->')
# We take everything from hazmat_start_idx to the end, EXCEPT the closing body/html and scripts,
# OR we can just take all the views and modals up to the Scripts Core.

scripts_core_idx = www_html.find('<!-- Scripts Core -->')
missing_views_and_modals = www_html[hazmat_start_idx:scripts_core_idx]

# Write out the combined HTML
with open('index_fixed.html', 'w', encoding='utf-8') as out:
    out.write(top_part + missing_views_and_modals + bottom_part)
print('Merged successfully')
