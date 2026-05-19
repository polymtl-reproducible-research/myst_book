#!/usr/bin/env python3
"""Translate MyST book source files (Markdown + Notebooks) to French.

Reads myst.yml to discover source files, translates prose while preserving
code blocks, math, directives, cross-references, and frontmatter.
Writes translated files to _translated/fr/.
"""

import json
import os
import re
import shutil
import time
import yaml

from deep_translator import GoogleTranslator

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRANSLATED_DIR = os.path.join(ROOT_DIR, "_translated", "fr")
TRANSLATOR = GoogleTranslator(source="en", target="fr")

# Max chars per translation call (Google Translate limit is ~5000)
CHUNK_SIZE = 4500


def translate_text(text):
    """Translate a string from English to French, handling chunking."""
    text = text.strip()
    if not text:
        return text
    # Skip if text is just whitespace, numbers, or punctuation
    if not re.search(r"[a-zA-Z]{2,}", text):
        return text
    try:
        if len(text) <= CHUNK_SIZE:
            result = TRANSLATOR.translate(text)
            time.sleep(0.3)  # rate-limit
            return result
        # Split into paragraphs for chunking
        paragraphs = text.split("\n\n")
        translated = []
        chunk = ""
        for para in paragraphs:
            if len(chunk) + len(para) + 2 > CHUNK_SIZE:
                if chunk:
                    translated.append(TRANSLATOR.translate(chunk.strip()))
                    time.sleep(0.3)
                chunk = para
            else:
                chunk = chunk + "\n\n" + para if chunk else para
        if chunk:
            translated.append(TRANSLATOR.translate(chunk.strip()))
            time.sleep(0.3)
        return "\n\n".join(translated)
    except Exception as e:
        print(f"  Warning: translation failed ({e}), keeping original")
        return text


def split_frontmatter(content):
    """Split YAML frontmatter from body. Returns (frontmatter_str, body)."""
    if content.startswith("---\n"):
        end = content.find("\n---\n", 4)
        if end != -1:
            fm = content[: end + 5]  # includes closing ---\n
            body = content[end + 5 :]
            return fm, body
    return "", content


def translate_markdown_body(body):
    """Translate markdown body, preserving code blocks, math, directives, etc."""
    lines = body.split("\n")
    output = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # --- Fenced code blocks (``` or ~~~) ---
        fence_match = re.match(r"^(`{3,}|~{3,})", line)
        if fence_match:
            fence_char = fence_match.group(1)[0]
            fence_len = len(fence_match.group(1))
            output.append(line)
            i += 1
            # Consume until closing fence
            while i < len(lines):
                if re.match(
                    r"^" + re.escape(fence_char) + r"{" + str(fence_len) + r",}\s*$",
                    lines[i],
                ):
                    output.append(lines[i])
                    i += 1
                    break
                output.append(lines[i])
                i += 1
            continue

        # --- MyST directive blocks (:::{directive}) ---
        directive_match = re.match(r"^(:{3,})\{(.+?)\}", line)
        if directive_match:
            colon_count = len(directive_match.group(1))
            directive_name = directive_match.group(2)
            closing = ":" * colon_count

            # For figure directives, preserve everything (path, options, but translate caption)
            if directive_name == "figure":
                output.append(line)
                i += 1
                # Consume options and content until closing
                while i < len(lines) and lines[i] != closing:
                    opt_line = lines[i]
                    if opt_line.startswith(":") or opt_line.strip() == "":
                        output.append(opt_line)
                    else:
                        # This is caption text - translate it
                        output.append(translate_text(opt_line))
                    i += 1
                if i < len(lines):
                    output.append(lines[i])  # closing :::
                    i += 1
                continue

            # For admonitions - translate the title and body text
            if directive_name == "admonition":
                # Line format: :::{admonition} Title Text
                title_part = line.split("}", 1)
                if len(title_part) > 1 and title_part[1].strip():
                    translated_title = translate_text(title_part[1].strip())
                    output.append(title_part[0] + "} " + translated_title)
                else:
                    output.append(line)
                i += 1
                # Process body lines until closing
                while i < len(lines) and lines[i] != closing:
                    body_line = lines[i]
                    if body_line.startswith(":"):
                        # directive option - keep as is
                        output.append(body_line)
                    elif re.match(r"^(`{3,}|~{3,})", body_line):
                        # Code block inside directive - preserve
                        output.append(body_line)
                        i += 1
                        inner_fence = re.match(r"^(`{3,}|~{3,})", body_line)
                        fc = inner_fence.group(1)[0]
                        fl = len(inner_fence.group(1))
                        while i < len(lines):
                            if re.match(
                                r"^" + re.escape(fc) + r"{" + str(fl) + r",}\s*$",
                                lines[i],
                            ):
                                output.append(lines[i])
                                i += 1
                                break
                            output.append(lines[i])
                            i += 1
                        continue
                    elif body_line.strip() == "":
                        output.append(body_line)
                    else:
                        output.append(translate_text(body_line))
                    i += 1
                if i < len(lines):
                    output.append(lines[i])  # closing :::
                    i += 1
                continue

            # Other directives - preserve entirely
            output.append(line)
            i += 1
            while i < len(lines) and lines[i] != closing:
                output.append(lines[i])
                i += 1
            if i < len(lines):
                output.append(lines[i])
                i += 1
            continue

        # --- Display math blocks ($$ ... $$) ---
        if line.strip().startswith("$$"):
            output.append(line)
            i += 1
            if not line.strip().endswith("$$") or line.strip() == "$$":
                while i < len(lines):
                    output.append(lines[i])
                    if lines[i].strip().startswith("$$"):
                        i += 1
                        break
                    i += 1
            continue

        # --- Empty lines ---
        if line.strip() == "":
            output.append(line)
            i += 1
            continue

        # --- Lines that are references/links only ---
        if re.match(r"^\s*\[.*\]\(#.*\)\s*\.?\s*$", line):
            output.append(line)
            i += 1
            continue

        # --- Table rows (| ... |) ---
        if re.match(r"^\s*\|", line):
            # Separator row
            if re.match(r"^\s*\|[\s\-:|]+\|\s*$", line):
                output.append(line)
                i += 1
                continue
            # Data/header row - translate cell contents
            cells = line.split("|")
            translated_cells = []
            for cell in cells:
                stripped = cell.strip()
                if stripped and re.search(r"[a-zA-Z]{2,}", stripped):
                    translated_cells.append(" " + translate_text(stripped) + " ")
                else:
                    translated_cells.append(cell)
            output.append("|".join(translated_cells))
            i += 1
            continue

        # --- Regular text lines (headings, paragraphs, list items) ---
        # Preserve inline MyST roles like {cite:p}`...`, {ref}`...`, etc.
        # and inline math $...$
        translated_line = translate_prose_line(line)
        output.append(translated_line)
        i += 1

    return "\n".join(output)


def translate_prose_line(line):
    """Translate a single prose line, preserving inline roles, math, and links."""
    # Extract heading prefix
    heading_match = re.match(r"^(#{1,6}\s+)", line)
    prefix = ""
    text = line
    if heading_match:
        prefix = heading_match.group(1)
        text = line[len(prefix) :]

    # Extract list prefix
    list_match = re.match(r"^(\s*[-*+]\s+|\s*\d+\.\s+)", text)
    if list_match:
        prefix = prefix + list_match.group(1)
        text = text[len(list_match.group(1)) :]

    if not text.strip():
        return line

    # Protect inline elements from translation by replacing with placeholders
    placeholders = []
    counter = [0]

    def protect(match):
        placeholders.append(match.group(0))
        ph = f"XPHX{counter[0]}XPHX"
        counter[0] += 1
        return ph

    # Protect MyST roles: {role}`target`
    protected = re.sub(r"\{[a-zA-Z:_-]+\}`[^`]*`", protect, text)
    # Protect inline math: $...$
    protected = re.sub(r"(?<!\$)\$(?!\$)(.+?)(?<!\$)\$(?!\$)", protect, protected)
    # Protect inline code: `...`
    protected = re.sub(r"`[^`]+`", protect, protected)
    # Protect cross-ref links: [text](#target) or [](#target)
    protected = re.sub(r"\[([^\]]*)\]\(#[^)]+\)", protect, protected)

    if not re.search(r"[a-zA-Z]{2,}", protected):
        return line

    translated = translate_text(protected)

    # Restore placeholders
    for idx, original in enumerate(placeholders):
        translated = translated.replace(f"XPHX{idx}XPHX", original)

    return prefix + translated


def translate_md_file(src_path, dst_path):
    """Translate a single markdown file."""
    print(f"  Translating {os.path.relpath(src_path, ROOT_DIR)}")
    with open(src_path, "r", encoding="utf-8") as f:
        content = f.read()

    frontmatter, body = split_frontmatter(content)

    # Translate the frontmatter title and description if present
    if frontmatter:
        try:
            fm_data = yaml.safe_load(frontmatter.strip("- \n"))
            if "title" in fm_data and isinstance(fm_data["title"], str):
                fm_data["title"] = translate_text(fm_data["title"])
            if "description" in fm_data and isinstance(fm_data["description"], str):
                fm_data["description"] = translate_text(fm_data["description"])
            frontmatter = "---\n" + yaml.dump(fm_data, allow_unicode=True, default_flow_style=False) + "---\n"
        except Exception:
            pass  # keep original frontmatter on parse error

    translated_body = translate_markdown_body(body)

    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    with open(dst_path, "w", encoding="utf-8") as f:
        f.write(frontmatter + translated_body)


def translate_notebook(src_path, dst_path):
    """Translate markdown cells in a Jupyter notebook."""
    print(f"  Translating {os.path.relpath(src_path, ROOT_DIR)}")
    with open(src_path, "r", encoding="utf-8") as f:
        nb = json.load(f)

    for cell in nb.get("cells", []):
        if cell["cell_type"] != "markdown":
            continue
        # Join source lines, translate, split back
        content = "".join(cell["source"])
        frontmatter, body = split_frontmatter(content)

        if frontmatter:
            try:
                fm_data = yaml.safe_load(frontmatter.strip("- \n"))
                if "title" in fm_data and isinstance(fm_data["title"], str):
                    fm_data["title"] = translate_text(fm_data["title"])
                frontmatter = "---\n" + yaml.dump(fm_data, allow_unicode=True, default_flow_style=False) + "---\n"
            except Exception:
                pass

        translated_body = translate_markdown_body(body)
        translated = frontmatter + translated_body

        # Preserve original source format (list of lines)
        cell["source"] = [line + "\n" for line in translated.split("\n")]
        if cell["source"]:
            cell["source"][-1] = cell["source"][-1].rstrip("\n")

    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    with open(dst_path, "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)


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


def create_french_myst_yml():
    """Create a myst.yml for the French build."""
    with open(os.path.join(ROOT_DIR, "myst.yml"), "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    # Translate project title/subtitle
    project = config.get("project", {})
    if "title" in project:
        project["title"] = translate_text(project["title"])
    if "subtitle" in project:
        project["subtitle"] = translate_text(project["subtitle"])

    # Update site logo text
    site = config.get("site", {})
    options = site.get("options", {})
    if "logo_text" in options:
        options["logo_text"] = translate_text(options["logo_text"])

    # Remove null abbreviations (causes myst issues)
    if "abbreviations" in project and not project["abbreviations"]:
        del project["abbreviations"]

    # Translate TOC section titles
    toc = project.get("toc", [])
    for item in toc:
        if "title" in item:
            item["title"] = translate_text(item["title"])

    # Bibliography was copied into the translated dir, keep paths as-is

    # Exclude paths: just keep simple patterns, drop paths that don't apply
    if "exclude" in project:
        project["exclude"] = ["README.md", "LICENSE"]

    dst = os.path.join(TRANSLATED_DIR, "myst.yml")
    with open(dst, "w", encoding="utf-8") as f:
        yaml.dump(config, f, allow_unicode=True, default_flow_style=False)
    print(f"  Created {os.path.relpath(dst, ROOT_DIR)}")


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


def main():
    print("=== Translating MyST sources to French ===")

    # Clean previous translations
    if os.path.exists(TRANSLATED_DIR):
        shutil.rmtree(TRANSLATED_DIR)
    os.makedirs(TRANSLATED_DIR, exist_ok=True)

    # Read myst.yml
    with open(os.path.join(ROOT_DIR, "myst.yml"), "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    source_files = collect_source_files(config)
    print(f"Found {len(source_files)} source files to translate")

    for rel_path in source_files:
        src = os.path.join(ROOT_DIR, rel_path)
        dst = os.path.join(TRANSLATED_DIR, rel_path)

        if not os.path.exists(src):
            print(f"  Skipping {rel_path} (not found)")
            continue

        if rel_path.endswith(".ipynb"):
            translate_notebook(src, dst)
        elif rel_path.endswith(".md"):
            translate_md_file(src, dst)
        else:
            # Copy other files as-is
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)

    # Copy figures directory
    figures_src = os.path.join(ROOT_DIR, "figures")
    figures_dst = os.path.join(TRANSLATED_DIR, "figures")
    if os.path.exists(figures_src):
        shutil.copytree(figures_src, figures_dst, dirs_exist_ok=True)
        print("  Copied figures/")

    # Copy images directory (content figures, template logos, ...)
    images_src = os.path.join(ROOT_DIR, "images")
    images_dst = os.path.join(TRANSLATED_DIR, "images")
    if os.path.exists(images_src):
        shutil.copytree(images_src, images_dst, dirs_exist_ok=True)
        print("  Copied images/")

    # Copy bibliography
    bib_src = os.path.join(ROOT_DIR, "bibliography")
    bib_dst = os.path.join(TRANSLATED_DIR, "bibliography")
    if os.path.exists(bib_src):
        shutil.copytree(bib_src, bib_dst, dirs_exist_ok=True)
        print("  Copied bibliography/")

    # Copy any file referenced from site.options (favicon, logo, style, ...)
    copy_site_option_assets(config)

    # Create French myst.yml
    create_french_myst_yml()

    print("=== Translation complete ===")


if __name__ == "__main__":
    main()
