import os

replacements = {
    'Ãª': 'ê',
    'Ã¡': 'á',
    'Ã§': 'ç',
    'Ã£': 'ã',
    'Ã³': 'ó',
    'Ã­': 'í',
    'Ã©': 'é',
    'Ãº': 'ú',
    'Ã¢': 'â',
    'Ãµ': 'õ',
    'Ã': 'í', # Catch some edge cases if needed, but risky. Let's stick to the double chars
    'Abertura de Nova OcorrÃªncia': 'Abertura de Nova Ocorrência',
    'TÃ­tulo': 'Título',
    'LocalizaÃ§Ã£o': 'Localização',
    'ReferÃªncia': 'Referência',
    'VeÃ­culo': 'Veículo',
    'VÃ­tima': 'Vítima',
    'CaminhÃ£o': 'Caminhão',
    'RodoviÃ¡rio': 'Rodoviário',
    'CÃ³digo': 'Código',
    'aplicÃ¡vel': 'aplicável',
    'DescriÃ§Ã£o': 'Descrição',
    'OcorrÃªncia': 'Ocorrência',
    'OcorrÃªncias': 'Ocorrências',
    'OpÃ§Ãµes': 'Opções',
    'NÃ£o': 'Não',
    'aviÃ£o': 'avião',
    'AÃ©reo': 'Aéreo',
    'MarÃ­timo': 'Marítimo',
    'FerroviÃ¡rio': 'Ferroviário',
    'PrÃ©-Laudo': 'Pré-Laudo',
    'TrÃ¢nsito': 'Trânsito',
    'ConcluÃ­da': 'Concluída',
    'ConcluÃ­das': 'Concluídas',
    'GeolocalizaÃ§Ã£o': 'Geolocalização',
    'AÃ§Ã£o': 'Ação',
    'AÃ§Ãµes': 'Ações',
    'InformaÃ§Ãµes': 'Informações',
    'InvestigaÃ§Ã£o': 'Investigação',
    'PrevenÃ§Ã£o': 'Prevenção',
    'ReincidÃªncia': 'Reincidência',
    'TÃ©cnica': 'Técnica',
    'TÃ©cnico': 'Técnico',
    'CondiÃ§Ã£o': 'Condição',
    'SeguranÃ§a': 'Segurança',
    'AnÃ¡lise': 'Análise',
    'CÃ¢mera': 'Câmera',
    'MÃ©todo': 'Método',
    'MÃ¡quina': 'Máquina',
    'CorreÃ§Ã£o': 'Correção',
    'OrtogrÃ¡fica': 'Ortográfica'
}

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

for k, v in replacements.items():
    html = html.replace(k, v)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Encoding fixed in index.html')
