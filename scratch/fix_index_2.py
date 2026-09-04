def fix_encoding_2():
    with open('../index.html', 'rb') as f:
        content = f.read()

    text = content.decode('utf-8', errors='replace')
    
    text = text.replace('\ufffd\ufffd', 'Á')
    text = text.replace('\ufffd', 'ê')
    text = text.replace('HISTêRICO GERAL (CONCLU??DAS)', 'HISTÓRICO GERAL (CONCLUÍDAS)')
    text = text.replace('CRONê??METRO', 'CRONÔMETRO')
    text = text.replace('??rvore dos 5 Porquês', 'Árvore dos 5 Porquês')
    
    with open('../index.html', 'w', encoding='utf-8') as f:
        f.write(text)
    
    print("Fixed remaining encoding in index.html")

if __name__ == '__main__':
    fix_encoding_2()
