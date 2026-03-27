#!/usr/bin/env python3
"""Inject Google Translate widget assets into all built HTML files."""

import glob
import os
import shutil

SCRIPTS_DIR = os.path.dirname(__file__)
BUILD_DIR = os.path.join(os.path.dirname(SCRIPTS_DIR), "_build", "html")
BASE_URL = os.environ.get("BASE_URL", "").rstrip("/")


def inject():
    # Copy widget assets into the build directory
    for asset in ("gtranslate-widget.js", "gtranslate-widget.css"):
        src = os.path.join(SCRIPTS_DIR, asset)
        dst = os.path.join(BUILD_DIR, asset)
        shutil.copy2(src, dst)
        print(f"Copied {asset} to {BUILD_DIR}")

    # Inject <link> and <script> tags into <head> of each HTML file
    css_tag = f'<link rel="stylesheet" href="{BASE_URL}/gtranslate-widget.css"/>'
    js_tag = f'<script src="{BASE_URL}/gtranslate-widget.js" defer></script>'
    inject_snippet = f"\n{css_tag}\n{js_tag}\n"

    html_files = glob.glob(os.path.join(BUILD_DIR, "**", "*.html"), recursive=True)
    count = 0
    for path in html_files:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        if "gtranslate-widget" in content:
            continue
        if "</head>" in content:
            content = content.replace("</head>", inject_snippet + "</head>")
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            count += 1

    print(f"Injected Google Translate widget into {count} HTML file(s)")


if __name__ == "__main__":
    inject()
