#!/usr/bin/env python3
"""Inject language switcher into all built HTML files (English + French).

Injects:
  - A <style> block with the widget CSS (body::after pseudo-element with flag SVGs)
  - A <script> tag for click handling and auto-redirect
  - A <meta> tag with the base URL

The CSS is embedded directly as static HTML in <head>. React/Remix cannot remove
<style> tags from <head> during SPA navigation — they persist across route changes.
"""

import base64
import glob
import os
import shutil

SCRIPTS_DIR = os.path.dirname(__file__)
BUILD_DIR = os.path.join(os.path.dirname(SCRIPTS_DIR), "_build", "html")
BASE_URL = os.environ.get("BASE_URL", "").rstrip("/")

# Flag SVGs as base64 data URIs
UK_SVG = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="16" viewBox="0 0 60 40"><rect width="60" height="40" fill="#012169"/><path d="M0,0 L60,40 M60,0 L0,40" stroke="#fff" stroke-width="8"/><path d="M0,0 L60,40" stroke="#C8102E" stroke-width="4" clip-path="polygon(0 0,30 20,60 0,60 40,30 20,0 40)"/><path d="M60,0 L0,40" stroke="#C8102E" stroke-width="4" clip-path="polygon(0 0,30 20,0 40,60 40,30 20,60 0)"/><path d="M30,0 V40 M0,20 H60" stroke="#fff" stroke-width="12"/><path d="M30,0 V40 M0,20 H60" stroke="#C8102E" stroke-width="6"/></svg>'

QC_SVG = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="16" viewBox="0 0 24 16"><rect width="24" height="16" fill="#003DA5"/><rect x="10" y="0" width="4" height="16" fill="#fff"/><rect x="0" y="6" width="24" height="4" fill="#fff"/><text x="5" y="5.5" font-size="5" fill="#fff" font-family="serif">\u269C</text><text x="15" y="5.5" font-size="5" fill="#fff" font-family="serif">\u269C</text><text x="5" y="13.5" font-size="5" fill="#fff" font-family="serif">\u269C</text><text x="15" y="13.5" font-size="5" fill="#fff" font-family="serif">\u269C</text></svg>'

UK_B64 = base64.b64encode(UK_SVG.encode("utf-8")).decode("ascii")
QC_B64 = base64.b64encode(QC_SVG.encode("utf-8")).decode("ascii")

WIDGET_CSS = f"""<style id="lang-switcher-css">
body::after {{
  content: "";
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 2147483647;
  display: block;
  width: 80px;
  height: 32px;
  background-color: rgba(255, 255, 255, 0.95);
  background-image: url("data:image/svg+xml;base64,{UK_B64}"), url("data:image/svg+xml;base64,{QC_B64}");
  background-repeat: no-repeat, no-repeat;
  background-position: 8px center, 48px center;
  background-size: 24px 16px, 24px 16px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.15);
  cursor: pointer;
  pointer-events: auto;
}}
.dark body::after, html.dark body::after {{
  background-color: rgba(30, 30, 30, 0.95);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.4);
}}
@media (max-width: 640px) {{
  body::after {{
    bottom: 10px;
    right: 10px;
  }}
}}
</style>"""


def inject():
    # Copy JS file into the build directory
    src = os.path.join(SCRIPTS_DIR, "language-switcher.js")
    dst = os.path.join(BUILD_DIR, "language-switcher.js")
    shutil.copy2(src, dst)
    print(f"Copied language-switcher.js to {BUILD_DIR}")

    # Also copy to fr/ subdirectory if it exists
    fr_dir = os.path.join(BUILD_DIR, "fr")
    if os.path.isdir(fr_dir):
        shutil.copy2(src, os.path.join(fr_dir, "language-switcher.js"))
        print(f"Copied language-switcher.js to {fr_dir}")

    # Inject <style> + <meta> + <script> into <head> of each HTML file
    meta_tag = f'<meta name="base-url" content="{BASE_URL}"/>'
    js_tag_en = f'<script src="{BASE_URL}/language-switcher.js" defer></script>'

    html_files = glob.glob(os.path.join(BUILD_DIR, "**", "*.html"), recursive=True)
    count = 0
    for path in html_files:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        if "lang-switcher-css" in content:
            continue
        if "</head>" not in content:
            continue

        rel = os.path.relpath(path, BUILD_DIR)
        is_french = rel.startswith("fr" + os.sep) or rel.startswith("fr/")

        if is_french:
            js_tag = f'<script src="{BASE_URL}/fr/language-switcher.js" defer></script>'
        else:
            js_tag = js_tag_en

        inject_snippet = f"\n{WIDGET_CSS}\n{meta_tag}\n{js_tag}\n"
        content = content.replace("</head>", inject_snippet + "</head>")

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        count += 1

    print(f"Injected language switcher into {count} HTML file(s)")


if __name__ == "__main__":
    inject()
