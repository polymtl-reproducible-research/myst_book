#!/usr/bin/env python3
"""Inject language switcher assets into all built HTML files (English + French)."""

import glob
import os
import shutil

SCRIPTS_DIR = os.path.dirname(__file__)
BUILD_DIR = os.path.join(os.path.dirname(SCRIPTS_DIR), "_build", "html")
BASE_URL = os.environ.get("BASE_URL", "").rstrip("/")


def inject():
    # Copy widget assets into the build directory
    for asset in ("language-switcher.js", "language-switcher.css"):
        src = os.path.join(SCRIPTS_DIR, asset)
        dst = os.path.join(BUILD_DIR, asset)
        shutil.copy2(src, dst)
        print(f"Copied {asset} to {BUILD_DIR}")

    # Also copy to fr/ subdirectory if it exists
    fr_dir = os.path.join(BUILD_DIR, "fr")
    if os.path.isdir(fr_dir):
        for asset in ("language-switcher.js", "language-switcher.css"):
            src = os.path.join(SCRIPTS_DIR, asset)
            dst = os.path.join(fr_dir, asset)
            shutil.copy2(src, dst)
        print(f"Copied assets to {fr_dir}")

    # Inject tags into <head> of each HTML file (both English and French)
    # Also inject a <meta> tag with the base URL so the JS can detect it
    meta_tag = f'<meta name="base-url" content="{BASE_URL}"/>'
    css_tag_en = f'<link rel="stylesheet" href="{BASE_URL}/language-switcher.css"/>'
    js_tag_en = f'<script src="{BASE_URL}/language-switcher.js" defer></script>'

    html_files = glob.glob(os.path.join(BUILD_DIR, "**", "*.html"), recursive=True)
    count = 0
    for path in html_files:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        if "lang-switcher-widget" in content:
            continue
        if "</head>" not in content:
            continue

        # Determine if this is a French page
        rel = os.path.relpath(path, BUILD_DIR)
        is_french = rel.startswith("fr" + os.sep) or rel.startswith("fr/")

        if is_french:
            css_tag = f'<link rel="stylesheet" href="{BASE_URL}/fr/language-switcher.css"/>'
            js_tag = f'<script src="{BASE_URL}/fr/language-switcher.js" defer></script>'
        else:
            css_tag = css_tag_en
            js_tag = js_tag_en

        inject_snippet = f"\n{meta_tag}\n{css_tag}\n{js_tag}\n"
        content = content.replace("</head>", inject_snippet + "</head>")

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        count += 1

    print(f"Injected language switcher into {count} HTML file(s)")


if __name__ == "__main__":
    inject()
