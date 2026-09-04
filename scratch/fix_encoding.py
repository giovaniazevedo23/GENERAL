import re

def fix_encoding():
    with open('../index.html', 'rb') as f:
        content = f.read()

    # The file is probably UTF-8 but some chars got mangled. Let's just decode ignoring errors and find the pattern.
    text = content.decode('utf-8', errors='replace')
    
    # Fix RVORE
    text = text.replace('\ufffdRVORE', 'ÁRVORE')
    # Also fix anything else like Avaliao
    text = text.replace('Avalia\ufffdo', 'Avaliação')
    text = text.replace('avalia\ufffdo', 'avaliação')
    text = text.replace('Ocorr\ufffdncia', 'Ocorrência')
    text = text.replace('Condi\ufffdo', 'Condição')
    text = text.replace('Clim\ufffdtica', 'Climática')
    text = text.replace('P\ufffdnico', 'Pânico')
    
    with open('../index.html', 'w', encoding='utf-8') as f:
        f.write(text)
    
    print("Encoding fixed in index.html")

    # Let's do the same for motorista.html
    with open('../motorista.html', 'rb') as f:
        content2 = f.read()
    
    text2 = content2.decode('utf-8', errors='replace')
    text2 = text2.replace('\ufffdRVORE', 'ÁRVORE')
    text2 = text2.replace('Avalia\ufffdo', 'Avaliação')
    text2 = text2.replace('Ocorr\ufffdncia', 'Ocorrência')
    text2 = text2.replace('Condi\ufffdo', 'Condição')
    text2 = text2.replace('Clim\ufffdtica', 'Climática')
    text2 = text2.replace('P\ufffdnico', 'Pânico')
    text2 = text2.replace('Log\ufffdstica', 'Logística')
    text2 = text2.replace('Emerg\ufffdncia', 'Emergência')
    text2 = text2.replace('R\ufffdpida', 'Rápida')
    text2 = text2.replace('avalia\ufffdo', 'avaliação')
    text2 = text2.replace('Ve\ufffdculo', 'Veículo')

    with open('../motorista.html', 'w', encoding='utf-8') as f:
        f.write(text2)
    print("Encoding fixed in motorista.html")

if __name__ == '__main__':
    fix_encoding()
