with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()
    if 'view-hazmat' in text:
        print('Found view-hazmat')
    else:
        print('Not found')
