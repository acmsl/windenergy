path = r'c:\Proyectos\LdP\v1r12\Web_Launcher\trabajo-1-feb-2026.html'
with open(path, 'r', encoding='utf-8') as f:
    s = f.read()
old_sig = 'function normalizeText(s){'
idx = s.find(old_sig)
if idx == -1:
    print('normalizeText not found')
else:
    # find end of function: look for pattern '\n      }' after idx
    end_idx = s.find('\n      }', idx)
    if end_idx == -1:
        print('end of function not found')
    else:
        end_idx += len('\n      }')
        new_func = 'function normalizeText(s){\n        return (s || "").toLowerCase().normalize("NFD").replace(/[\\u0300-\\u036f]/g, "");\n      }'
        new_s = s[:idx] + new_func + s[end_idx:]
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_s)
        print('Replaced normalizeText')
