import sys
import re

file_path = "index.html"

try:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
except UnicodeDecodeError:
    with open(file_path, "r", encoding="latin-1") as f:
        content = f.read()

# 1. Remove Copilot button from sidebar
sidebar_btn_re = re.compile(r'<button data-tab="copilot"[^>]+>.*?Copilot Tático 24h\s*</button>', re.DOTALL)
content = sidebar_btn_re.sub('', content)

# 2. Replace Manual de Uso in Central de Ajuda
manual_de_uso_re = re.compile(r'<a href="#" onclick="App\.showToast\(\'Em breve:[^\n]+>.*?<i data-lucide="book-open".*?<span class="text-xs font-bold text-blue-300">Manual de Uso</span>.*?</a>', re.DOTALL)

copilot_card = '''
          <a href="#" onclick="App.switchTab('copilot'); document.getElementById('help-modal').classList.add('hidden');" class="bg-blue-600 border border-blue-500 rounded-xl p-4 flex flex-col items-center justify-center gap-2 hover:bg-blue-500 transition-colors relative">
            <span class="absolute -top-2 -right-2 flex h-4 w-4">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-white opacity-75"></span>
              <span class="relative inline-flex rounded-full h-4 w-4 bg-blue-100"></span>
            </span>
            <i data-lucide="bot" class="w-6 h-6 text-white"></i>
            <span class="text-xs font-bold text-white">Copilot Tático 24h</span>
            <span class="text-[9px] text-blue-200 text-center">IA Assistente</span>
          </a>
'''
content = manual_de_uso_re.sub(copilot_card, content)

try:
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
except Exception:
    with open(file_path, "w", encoding="latin-1") as f:
        f.write(content)

print("index.html patched again.")
