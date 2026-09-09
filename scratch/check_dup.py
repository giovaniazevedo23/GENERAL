with open('../gestor-app/index.html', 'r', encoding='utf-8') as f:
    content = f.read()
print('Number of superhero buttons:', content.count('data-theme="superhero"'))
