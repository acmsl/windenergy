import os
import re
from pathlib import Path

# Mapping of equivalent pages across languages
PAGE_MAPPING = {
    "introduction": {
        "en": "introduction.html",
        "es": "introduccion.html",
        "fr": "introduction.html",
        "it": None,
        "de": None,
        "pt": None,
    },
    "industrial-turbines": {
        "en": "industrial-wind-turbines.html",
        "es": "aerogeneradores-industriales.html",
        "fr": "eoliennes-industrielles.html",
        "it": "turbine-eoliche-industriali.html",
        "de": "industrielle-windturbinen.html",
        "pt": "turbinas-eolicas-industriais.html",
    },
    "families": {
        "en": "wind-turbine-families.html",
        "es": "familias-aerogeneradores.html",
        "fr": "familles-eoliennes.html",
        "it": "famiglie-turbine-eoliche.html",
        "de": "windturbinen-familien.html",
        "pt": "familias-turbinas-eolicas.html",
    },
    "operational-ranges": {
        "en": "operational-wind-ranges.html",
        "es": "rangos-operacionales.html",
        "fr": "plages-operationnelles.html",
        "it": "intervalli-operativi-vento.html",
        "de": "betriebliche-windgeschwindigkeiten.html",
        "pt": "faixas-operacionais-vento.html",
    },
    "simulators": {
        "en": "simulators-and-tutorials.html",
        "es": "simuladores-y-tutoriales.html",
        "fr": "simulateurs-et-tutoriels.html",
        "it": None,
        "de": None,
        "pt": None,
    },
    "mindmap": {
        "en": "wind-energy-mindmap.html",
        "es": "mapa-mental.html",
        "fr": "carte-mentale.html",
        "it": "mappa-conoscenza-eolica.html",
        "de": "windenergie-wissenskarte.html",
        "pt": "mapa-conhecimento-eolico.html",
    },
}

FILENAME_TO_CONCEPT = {}
for concept, langs in PAGE_MAPPING.items():
    for lang, filename in langs.items():
        if filename:
            FILENAME_TO_CONCEPT[filename] = (concept, lang)

SKIP_FILES = {
    "tutorials/en/introduction.html",
    "tutorials/en/industrial-wind-turbines.html",
}

def get_language_options(current_filename, current_lang):
    if current_filename not in FILENAME_TO_CONCEPT:
        print(f"Warning: {current_filename} not in mapping")
        return ""
    
    concept, _ = FILENAME_TO_CONCEPT[current_filename]
    options = []
    
    for lang in ["en", "es", "fr", "it", "de", "pt"]:
        filename = PAGE_MAPPING[concept].get(lang)
        if filename:
            selected = " selected" if lang == current_lang else ""
            option_value = f"../{lang}/{filename}"
            lang_upper = lang.upper()
            options.append(f'        <option value="{option_value}"{selected}>{lang_upper}</option>')
    
    return "
".join(options)

def extract_nav_links(content):
    nav_match = re.search(r'<nav>(.*?)</nav>', content, re.DOTALL)
    if nav_match:
        return nav_match.group(1).strip()
    return ""

def create_new_header(lang_code, nav_links, language_options):
    header = f'<header class="tut-header">
'
    header += f'  <div class="tut-header-row">
'
    header += f'    <div class="tut-header-left">
'
    header += f'      <img src="../../img/ACM_LOGO.png" alt="ACMSL" class="logo">
'
    header += f'      <a href="https://www.acm-sl.com" class="brand">ACMSL</a>
'
    header += f'    </div>
'
    header += f'    <nav>
'
    header += f'{nav_links}
'
    header += f'    </nav>
'
    header += f'  </div>
'
    header += f'  <div class="tut-header-toolbar">
'
    header += f'    <div class="tut-toolbar-actions">
'
    header += f'      <a href="../../index.html?lang={lang_code}">&#127968; Home</a>
'
    header += f'      <a href="https://www.acm-sl.com" target="_blank" rel="noopener">&#127760; acm-sl.com</a>
'
    header += f'    </div>
'
    header += f'    <div class="tut-lang-selector">
'
    header += f'      <select onchange="window.location.href = this.value" aria-label="Language">
'
    header += f'{language_options}
'
    header += f'      </select>
'
    header += f'    </div>
'
    header += f'  </div>
'
    header += f'</header>'
    return header

def update_header(filepath):
    rel_path = filepath.replace('\\', '/').replace('c:/Proyectos/launcher/', '')
    
    if rel_path in SKIP_FILES:
        print(f"✓ Skipping {rel_path} (already updated)")
        return None
    
    parts = filepath.replace('\\', '/').split('/')
    lang_code = parts[-2]
    filename = parts[-1]
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    backup_path = filepath + '.backup'
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    nav_links = extract_nav_links(content)
    if not nav_links:
        print(f"✗ Could not extract nav links from {rel_path}")
        return False
    
    language_options = get_language_options(filename, lang_code)
    if not language_options:
        print(f"✗ Could not generate language options for {rel_path}")
        return False
    
    new_header = create_new_header(lang_code, nav_links, language_options)
    
    content = re.sub(
        r'<div class="tut-toolbar">.*?</div>\s*(?=<header)',
        '',
        content,
        flags=re.DOTALL
    )
    
    new_content = re.sub(
        r'<header class="tut-header">.*?</header>',
        new_header,
        content,
        flags=re.DOTALL,
        count=1
    )
    
    if new_content == content:
        print(f"⚠ No changes made to {rel_path}")
        return False
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✓ Updated {rel_path}")
    return True

base_path = Path('c:/Proyectos/launcher/tutorials')

html_files = []
for lang in ['en', 'es', 'fr', 'it', 'de', 'pt']:
    lang_dir = base_path / lang
    if lang_dir.exists():
        html_files.extend(lang_dir.glob('*.html'))

print(f"Found {len(html_files)} HTML files to process
")

success_count = 0
skip_count = 0
fail_count = 0

for filepath in sorted(html_files):
    result = update_header(str(filepath))
    if result is True:
        success_count += 1
    elif result is None:
        skip_count += 1
    else:
        fail_count += 1

print(f"
{'='*60}")
print(f"Summary:")
print(f"  Updated: {success_count}")
print(f"  Skipped: {skip_count}")
print(f"  Failed: {fail_count}")
print(f"{'='*60}")
print(f"
Backup files created with .backup extension")
