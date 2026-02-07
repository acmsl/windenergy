path = r'c:\Proyectos\LdP\v1r12\Web_Launcher\trabajo-1-feb-2026.html'
with open(path,'r',encoding='utf-8') as f:
    s=f.read()
pat='function normalizeText(s){'
idxs=[]
start=0
while True:
    i=s.find(pat,start)
    if i==-1: break
    idxs.append(i)
    start=i+1
print('found',len(idxs),'occurrences')
if len(idxs)>=2:
    first=idxs[0]
    second=idxs[1]
    new_func = pat + "\n        return (s || \"\").toLowerCase().normalize(\"NFD\").replace(/[\\u0300-\\u036f]/g, \"\");\n      }\n"
    new_s = s[:first] + new_func + s[second+len(pat):]
    with open(path,'w',encoding='utf-8') as f:
        f.write(new_s)
    print('replaced first occurrence')
else:
    print('not enough occurrences')
