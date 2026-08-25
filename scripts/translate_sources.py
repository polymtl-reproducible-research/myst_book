#!/usr/bin/env python3
"""Translate MyST book source files (Markdown + Notebooks) to French.

Reads myst.yml to discover source files, translates prose while preserving
code blocks, math, directives, cross-references, and frontmatter.
Writes translated files to _translated/fr/.

Strings resolve through overrides, then the cache, then the translator. Any
string that cannot be resolved fails the build rather than silently shipping
English.
"""

import argparse
import json
import os
import shutil
import sys
import yaml

from md_segmenter import translate_body
from resolver import Resolver, load_json, save_json
from translator_backend import make_google_translator

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRANSLATED_DIR = os.path.join(ROOT_DIR, "_translated", "fr")
DEFAULT_CACHE = os.path.join(ROOT_DIR, ".tcache", "fr.cache.json")
OVERRIDES_PATH = os.path.join(ROOT_DIR, "translations", "fr.overrides.json")


def split_frontmatter(content):
    """Split YAML frontmatter from body. Returns (frontmatter_str, body)."""
    if content.startswith("---\n"):
        end = content.find("\n---\n", 4)
        if end != -1:
            fm = content[: end + 5]  # includes closing ---\n
            body = content[end + 5 :]
            return fm, body
    return "", content


def translate_md_file(src_path, dst_path, resolve):
    """Translate a single markdown file."""
    print("  Translating " + os.path.relpath(src_path, ROOT_DIR))
    with open(src_path, "r", encoding="utf-8") as handle:
        content = handle.read()

    frontmatter, body = split_frontmatter(content)
    if frontmatter:
        frontmatter = _translate_frontmatter(frontmatter, resolve, ("title", "description"))

    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    with open(dst_path, "w", encoding="utf-8") as handle:
        handle.write(frontmatter + translate_body(body, resolve))


def _translate_frontmatter(frontmatter, resolve, fields):
    try:
        data = yaml.safe_load(frontmatter.strip("- \n"))
        for field in fields:
            if isinstance(data.get(field), str):
                data[field] = resolve(data[field])
        return "---\n" + yaml.dump(data, allow_unicode=True, default_flow_style=False) + "---\n"
    except Exception:
        return frontmatter   # keep original on parse error


def translate_notebook(src_path, dst_path, resolve):
    """Translate markdown cells in a Jupyter notebook."""
    print("  Translating " + os.path.relpath(src_path, ROOT_DIR))
    with open(src_path, "r", encoding="utf-8") as handle:
        notebook = json.load(handle)

    for cell in notebook.get("cells", []):
        if cell["cell_type"] != "markdown":
            continue
        frontmatter, body = split_frontmatter("".join(cell["source"]))
        if frontmatter:
            frontmatter = _translate_frontmatter(frontmatter, resolve, ("title",))
        translated = frontmatter + translate_body(body, resolve)
        cell["source"] = [line + "\n" for line in translated.split("\n")]
        if cell["source"]:
            cell["source"][-1] = cell["source"][-1].rstrip("\n")

    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    with open(dst_path, "w", encoding="utf-8") as handle:
        json.dump(notebook, handle, ensure_ascii=False, indent=1)


def collect_source_files(myst_config):
    """Extract source file paths from myst.yml TOC."""
    files = []
    project = myst_config.get("project", {})
    toc = project.get("toc", [])

    def walk_toc(items):
        for item in items:
            if "file" in item:
                files.append(item["file"])
            if "children" in item:
                walk_toc(item["children"])

    walk_toc(toc)
    return files


def create_french_myst_yml(config, resolve):
    """Write a myst.yml for the French build."""
    project = config.get("project", {})
    for field in ("title", "subtitle"):
        if isinstance(project.get(field), str):
            project[field] = resolve(project[field])

    options = config.get("site", {}).get("options", {}) or {}
    if isinstance(options.get("logo_text"), str):
        options["logo_text"] = resolve(options["logo_text"])

    if "abbreviations" in project and not project["abbreviations"]:
        del project["abbreviations"]

    for item in project.get("toc", []):
        if "title" in item:
            item["title"] = resolve(item["title"])

    if "exclude" in project:
        project["exclude"] = ["README.md", "LICENSE"]

    os.makedirs(TRANSLATED_DIR, exist_ok=True)
    destination = os.path.join(TRANSLATED_DIR, "myst.yml")
    with open(destination, "w", encoding="utf-8") as handle:
        yaml.dump(config, handle, allow_unicode=True, default_flow_style=False)
    print("  Created " + os.path.relpath(destination, ROOT_DIR))


def report_unresolved(unresolved):
    """Build the failure report printed before a non-zero exit."""
    lines = ["", "=== %d strings could not be translated ===" % len(unresolved)]
    for text in unresolved:
        excerpt = text if len(text) <= 70 else text[:67] + "..."
        lines.append("  " + excerpt)
    lines.append("")
    lines.append("Re-run the job, or pin a translation in translations/fr.overrides.json.")
    return "\n".join(lines)


def copy_site_option_assets(config):
    """Copy any file referenced as a relative path in site.options.

    Handles template-provided assets like favicon, logo, logo_dark, style.
    URLs and non-existent paths are skipped.
    """
    options = config.get("site", {}).get("options", {}) or {}
    for key, value in options.items():
        if not isinstance(value, str):
            continue
        rel = value[2:] if value.startswith("./") else value
        if rel.startswith(("http://", "https://", "/", "data:")):
            continue
        src = os.path.join(ROOT_DIR, rel)
        if not os.path.isfile(src):
            continue
        dst = os.path.join(TRANSLATED_DIR, rel)
        parent = os.path.dirname(dst)
        if parent:
            os.makedirs(parent, exist_ok=True)
        shutil.copy2(src, dst)
        print(f"  Copied {rel} (site.options.{key})")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Translate MyST sources to French.")
    parser.add_argument("--cache", default=DEFAULT_CACHE, help="path to the machine cache JSON")
    parser.add_argument("--attempts", type=int, default=8, help="translation attempts per string")
    args = parser.parse_args(argv)

    print("=== Translating MyST sources to French ===")

    if os.path.exists(TRANSLATED_DIR):
        shutil.rmtree(TRANSLATED_DIR)
    os.makedirs(TRANSLATED_DIR, exist_ok=True)

    with open(os.path.join(ROOT_DIR, "myst.yml"), "r", encoding="utf-8") as handle:
        config = yaml.safe_load(handle)

    resolver = Resolver(
        make_google_translator(attempts=args.attempts),
        cache=load_json(args.cache),
        overrides=load_json(OVERRIDES_PATH),
    )
    resolve = resolver.resolve

    source_files = collect_source_files(config)
    print("Found %d source files to translate" % len(source_files))

    for rel_path in source_files:
        src = os.path.join(ROOT_DIR, rel_path)
        dst = os.path.join(TRANSLATED_DIR, rel_path)
        if not os.path.exists(src):
            print("  Skipping %s (not found)" % rel_path)
            continue
        if rel_path.endswith(".ipynb"):
            translate_notebook(src, dst, resolve)
        elif rel_path.endswith(".md"):
            translate_md_file(src, dst, resolve)
        else:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)

    for name in ("images", "bibliography"):
        source = os.path.join(ROOT_DIR, name)
        if os.path.exists(source):
            shutil.copytree(source, os.path.join(TRANSLATED_DIR, name), dirs_exist_ok=True)
            print("  Copied %s/" % name)

    copy_site_option_assets(config)
    create_french_myst_yml(config, resolve)

    if resolver.added:
        save_json(args.cache, resolver.cache)
        print("  Cached %d new translations in %s" % (resolver.added, args.cache))

    if resolver.unresolved:
        print(report_unresolved(resolver.unresolved), file=sys.stderr)
        return 1

    print("=== Translation complete ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
