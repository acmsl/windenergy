import os
import re
from pathlib import Path

FILE_MAP = {}
langs_order = ["en", "es", "fr", "it", "de", "pt"]

# Industrial turbines - all 6 langs
for lang, fname in [("en", "industrial-wind-turbines.html"), ("es", "aerogeneradores-industriales.html"),
                      ("fr", "eoliennes-industrielles.html"), ("it", "turbine-eoliche-industriali.html"),
                      ("de", "industrielle-windturbinen.html"), ("pt", "turbinas-eolicas-industriais.html")]:
    FILE_MAP[fname] = (lang, {"en":"industrial-wind-turbines.html", "es":"aerogeneradores-industriales.html",
                               "fr":"eoliennes-industrielles.html", "it":"turbine-eoliche-industriali.html",
                               "de":"industrielle-windturbinen.html", "pt":"turbinas-eolicas-industriais.html"})

# Families - all 6 langs
for lang, fname in [("en", "wind-turbine-families.html"), ("es", "familias-aerogeneradores.html"),
                      ("fr", "familles-eoliennes.html"), ("it", "famiglie-turbine-eoliche.html"),
                      ("de", "windturbinen-familien.html"), ("pt", "familias-turbinas-eolicas.html")]:
    FILE_MAP[fname] = (lang, {"en":"wind-turbine-families.html", "es":"familias-aerogeneradores.html",
                               "fr":"familles-eoliennes.html", "it":"famiglie-turbine-eoliche.html",
                               "de":"windturbinen-familien.html", "pt":"familias-turbinas-eolicas.html"})

# Operational ranges - all 6 langs
for lang, fname in [("en", "operational-wind-ranges.html"), ("es", "rangos-operacionales.html"),
                      ("fr", "plages-operationnelles.html"), ("it", "intervalli-operativi-vento.html"),
                      ("de", "betriebliche-windgeschwindigkeiten.html"), ("pt", "faixas-operacionais-vento.html")]:
    FILE_MAP[fname] = (lang, {"en":"operational-wind-ranges.html", "es":"rangos-operacionales.html",
                               "fr":"plages-operationnelles.html", "it":"intervalli-operativi-vento.html",
                               "de":"betriebliche-windgeschwindigkeiten.html", "pt":"faixas-operacionais-vento.html"})

# Mindmap - all 6 langs
for lang, fname in [("en", "wind-energy-mindmap.html"), ("es", "mapa-mental.html"),
                      ("fr", "carte-mentale.html"), ("it", "mappa-conoscenza-eolica.html"),
                      ("de", "windenergie-wissenskarte.html"), ("pt", "mapa-conhecimento-eolico.html")]:
    FILE_MAP[fname] = (lang, {"en":"wind-energy-mindmap.html", "es":"mapa-mental.html",
                               "fr":"carte-mentale.html", "it":"mappa-conoscenza-eolica.html",
                               "de":"windenergie-wissenskarte.html", "pt":"mapa-conhecimento-eolico.html"})

# Introduction - 3 langs
for lang, fname in [("en", "introduction.html"), ("es", "introduccion.html"), ("fr", "introduction.html")]:
    FILE_MAP[fname] = (lang, {"en":"introduction.html", "es":"introduccion.html", "fr":"introduction.html"})

# Simulators - 3 langs
for lang, fname in [("en", "simulators-and-tutorials.html"), ("es", "simuladores-y-tutoriales.html"),
                      ("fr", "simulateurs-et-tutoriels.html")]:
    FILE_MAP[fname] = (lang, {"en":"simulators-and-tutorials.html", "es":"simuladores-y-tutoriales.html",
                               "fr":"simulateurs-et-tutoriels.html"})

base = Path("c:/Proyectos/launcher/tutorials")
count = 0

for lang_dir in ["en", "es", "fr", "it", "de", "pt"]:
    dir_path = base / lang_dir
    if not dir_path.exists():
        continue
    for fpath in dir_path.glob("*.html"):
        if fpath.name not in FILE_MAP:
            continue
        
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        
        if "tut-lang-selector" in content:
            continue
        
        current_lang, files_map = FILE_MAP[fpath.name]
        
        opts = []
        for lang in langs_order:
            if lang in files_map:
                sel = " selected" if lang == current_lang else ""
                opts.append(f"        <option value="../{lang}/{files_map[lang]}"{sel}>{lang.upper()}</option>")
        
        selector = "    <div class="tut-lang-selector">
"
        selector += "      <select onchange="window.location.href = this.value" aria-label="Language">
"
        selector += "
".join(opts) + "
"
        selector += "      </select>
"
        selector += "    </div>"
        
        new_content = re.sub(
            r"(    </div>\s*)(    </div>\s*</header>)",
            r"" + selector + "
",
            content,
            count=1
        )
        
        if new_content != content:
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(new_content)
            count += 1
            print(f"Added selector: {lang_dir}/{fpath.name}")

print(f"
Total files updated: {count}")
