import chardet

with open('www/index.html', 'rb') as f:
    raw_data = f.read(10000)
    print(chardet.detect(raw_data))
