import os

with open('www/index.html', 'r', encoding='utf-8') as f:
    www_html = f.read()

# find where new-communication-modal ends
# It ends with:
#               <i data-lucide="plus" class="w-4 h-4"></i> Adicionar
#             </button>
#           </div>
#         </div>
#       </div>

idx = www_html.find('Adicionar\n            </button>\n          </div>\n        </div>\n      </div>')
if idx == -1:
    print('Not found')
else:
    # Print the next 1000 characters
    print(www_html[idx+90:idx+1090])
