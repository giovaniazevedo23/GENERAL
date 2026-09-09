import shutil
import os

files_to_sync = [
    ('index.html', 'www/index.html'),
    ('motorista.html', 'www/motorista.html'),
    ('js/app.js', 'www/js/app.js'),
    ('js/app_motorista.js', 'www/js/app_motorista.js')
]

for src, dst in files_to_sync:
    if os.path.exists(src) and os.path.exists(os.path.dirname(dst)):
        try:
            shutil.copy2(src, dst)
            print(f"Synced {src} -> {dst}")
        except Exception as e:
            print(f"Error syncing {src}: {e}")
    else:
        print(f"Could not sync {src} (exists? {os.path.exists(src)}) to {dst} (dir exists? {os.path.exists(os.path.dirname(dst))})")
