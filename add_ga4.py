# -*- coding: utf-8 -*-
"""Add Google Analytics 4 snippet to all public HTML files."""

import os
import glob

GA4_ID = "G-T1XF1Z8ML9"

GA4_SNIPPET = f"""  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', '{GA4_ID}');
  </script>
</head>"""

BASE = r"C:\Proyectos\launcher"

# Collect files: root *.html + tutorials/**/*.html + simulators/**/*.html
# Exclude Pruebas/, LdP_Datalogger help, and treinamento-em-turbinas-eolicas/
patterns = [
    os.path.join(BASE, "*.html"),
    os.path.join(BASE, "tutorials", "**", "*.html"),
    os.path.join(BASE, "simulators", "**", "*.html"),
]

EXCLUDE_DIRS = ["Pruebas", "LdP_Datalogger_Viewer_help", "treinamento-em-turbinas-eolicas", "tmpclaude"]

files = []
for pattern in patterns:
    for f in glob.glob(pattern, recursive=True):
        skip = False
        for ex in EXCLUDE_DIRS:
            if ex in f:
                skip = True
                break
        if not skip:
            files.append(f)

updated = 0
skipped = 0

for fpath in sorted(files):
    with open(fpath, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    if GA4_ID in content:
        skipped += 1
        continue

    if "</head>" not in content:
        skipped += 1
        continue

    new_content = content.replace("</head>", GA4_SNIPPET, 1)

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(new_content)

    rel = os.path.relpath(fpath, BASE)
    print(f"  Updated: {rel}")
    updated += 1

print(f"\nDone: {updated} files updated, {skipped} skipped (already had GA4 or no </head>).")
