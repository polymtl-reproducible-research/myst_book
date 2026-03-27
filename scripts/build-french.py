#!/usr/bin/env python3
"""Build the French version of the MyST book.

1. Translates source files using translate-sources.py
2. Runs myst build --html in the translated directory
3. Copies the French build output into _build/html/fr/
"""

import os
import shutil
import subprocess
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRANSLATED_DIR = os.path.join(ROOT_DIR, "_translated", "fr")
ENGLISH_BUILD = os.path.join(ROOT_DIR, "_build", "html")
FRENCH_BUILD_SRC = os.path.join(TRANSLATED_DIR, "_build", "html")
FRENCH_BUILD_DST = os.path.join(ENGLISH_BUILD, "fr")
BASE_URL = os.environ.get("BASE_URL", "").rstrip("/")


def run(cmd, cwd=None):
    print(f"  Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.returncode != 0:
        print(f"  ERROR: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    return result


def main():
    # Step 1: Translate sources
    print("=== Step 1: Translating source files ===")
    run([sys.executable, os.path.join(ROOT_DIR, "scripts", "translate-sources.py")])

    # Step 2: Build French site with myst
    print("\n=== Step 2: Building French HTML ===")
    # Set BASE_URL for the French sub-site
    env = os.environ.copy()
    env["BASE_URL"] = f"{BASE_URL}/fr"
    result = subprocess.run(
        ["myst", "build", "--html"],
        cwd=TRANSLATED_DIR,
        env=env,
        capture_output=True,
        text=True,
    )
    if result.stdout:
        print(result.stdout)
    if result.returncode != 0:
        print(f"  ERROR building French site: {result.stderr}", file=sys.stderr)
        sys.exit(1)

    # Step 3: Copy French build into English build's /fr/ directory
    print("\n=== Step 3: Merging French build into main site ===")
    if not os.path.exists(FRENCH_BUILD_SRC):
        print(f"  ERROR: French build output not found at {FRENCH_BUILD_SRC}", file=sys.stderr)
        sys.exit(1)

    if os.path.exists(FRENCH_BUILD_DST):
        shutil.rmtree(FRENCH_BUILD_DST)

    shutil.copytree(FRENCH_BUILD_SRC, FRENCH_BUILD_DST)
    print(f"  Copied French build to {os.path.relpath(FRENCH_BUILD_DST, ROOT_DIR)}")

    # Step 4: Clean up translated source directory (optional, saves space)
    # shutil.rmtree(TRANSLATED_DIR)

    print("\n=== French build complete ===")
    # Count pages
    html_count = sum(
        1 for f in os.listdir(FRENCH_BUILD_DST) if f.endswith(".html")
    )
    print(f"  {html_count} French HTML pages in {os.path.relpath(FRENCH_BUILD_DST, ROOT_DIR)}")


if __name__ == "__main__":
    main()
