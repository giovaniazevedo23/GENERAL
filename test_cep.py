import urllib.request
import json

def get_cep(cep):
    url = f"https://brasilapi.com.br/api/cep/v2/{cep}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        return str(e)

print("Origem CEP:", get_cep("64027638"))
print("Destino CEP:", get_cep("62300000"))
