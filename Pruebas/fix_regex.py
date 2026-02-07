with open(r'c:\Proyectos\LdP\v1r12\Web_Launcher\trabajo-1-feb-2026.html', 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace('[00-ff]', r'[\u0300-\u036f]')
with open(r'c:\Proyectos\LdP\v1r12\Web_Launcher\trabajo-1-feb-2026.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Fixed!')
