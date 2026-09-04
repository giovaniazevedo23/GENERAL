import re

def patch_app_motorista_js():
    with open('../js/app_motorista.js', 'r', encoding='utf-8', errors='ignore') as f:
        js = f.read()

    # Block incident creation if shift is over 12 hours
    if 'if (this.checkShiftLimit && this.checkShiftLimit()) return;' not in js:
        js = js.replace('openNewIncidentModal() {', "openNewIncidentModal() {\n      if (this.checkShiftLimit && this.checkShiftLimit()) return;\n")

    # Block dispatch if shift is over 12 hours
    if 'openDispatchModal' in js and 'if (this.checkShiftLimit && this.checkShiftLimit()) return;' not in js.split('openDispatchModal')[1][:200]:
        js = js.replace('openDispatchModal() {', "openDispatchModal() {\n      if (this.checkShiftLimit && this.checkShiftLimit()) return;\n")

    with open('../js/app_motorista.js', 'w', encoding='utf-8') as f:
        f.write(js)
    
    print("app_motorista.js shift validation added.")

if __name__ == '__main__':
    patch_app_motorista_js()
