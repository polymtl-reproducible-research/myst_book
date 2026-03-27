#!/usr/bin/env python3
"""Inject language switcher script into all built HTML files (English + French).

Only injects a <script> tag — all CSS lives inside the JS via adoptedStyleSheets,
so no <link> tag is needed and React/Remix cannot remove the styles.
"""

import glob
import os
import shutil

SCRIPTS_DIR = os.path.dirname(__file__)
BUILD_DIR = os.path.join(os.path.dirname(SCRIPTS_DIR), "_build", "html")
BASE_URL = os.environ.get("BASE_URL", "").rstrip("/")


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

    # Inject <meta> + <script> into <head> of each HTML file
    meta_tag = f'<meta name="base-url" content="{BASE_URL}"/>'
    js_tag_en = f'<script src="{BASE_URL}/language-switcher.js" defer></script>'

    html_files = glob.glob(os.path.join(BUILD_DIR, "**", "*.html"), recursive=True)
    count = 0
    for path in html_files:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        if "language-switcher" in content:
            continue
        if "</head>" not in content:
            continue

        # Determine if this is a French page
        rel = os.path.relpath(path, BUILD_DIR)
        is_french = rel.startswith("fr" + os.sep) or rel.startswith("fr/")

        if is_french:
            js_tag = f'<script src="{BASE_URL}/fr/language-switcher.js" defer></script>'
        else:
            js_tag = js_tag_en

        inject_snippet = f"\n{meta_tag}\n{js_tag}\n"
        content = content.replace("</head>", inject_snippet + "</head>")

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        count += 1

    print(f"Injected language switcher into {count} HTML file(s)")


if __name__ == "__main__":
    inject()
