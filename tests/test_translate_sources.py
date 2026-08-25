import json
import os
import re
import pytest
import translate_sources as ts
from resolver import Resolver

FENCE = re.compile(r"^(`{3,}|~{3,})")
UP = str.upper


def fences(text):
    """Every fenced code block in a document, as raw line lists."""
    out, buf, inside = [], [], False
    for line in text.split("\n"):
        if FENCE.match(line):
            buf.append(line)
            if inside:
                out.append(buf)
                buf = []
            inside = not inside
        elif inside:
            buf.append(line)
    return out


def test_report_lists_every_unresolved_string():
    report = ts.report_unresolved(["Labs", "Lectures"])
    assert "2 strings could not be translated" in report
    assert "Labs" in report and "Lectures" in report


def test_report_mentions_the_overrides_file():
    assert "translations/fr.overrides.json" in ts.report_unresolved(["Labs"])


def test_md_file_translates_prose_and_frontmatter_title(tmp_path):
    src = tmp_path / "a.md"
    src.write_text("---\ntitle: Lab 1\n---\n\nSome prose here.\n", encoding="utf-8")
    dst = tmp_path / "out" / "a.md"
    ts.translate_md_file(str(src), str(dst), UP)
    text = dst.read_text(encoding="utf-8")
    assert "LAB 1" in text
    assert "SOME PROSE HERE." in text


def test_md_file_preserves_code_blocks(tmp_path):
    src = tmp_path / "a.md"
    src.write_text("Intro line.\n\n```bash\ngit init\n```\n", encoding="utf-8")
    dst = tmp_path / "out" / "a.md"
    ts.translate_md_file(str(src), str(dst), UP)
    assert "git init" in dst.read_text(encoding="utf-8")


def test_notebook_translates_markdown_cells_only(tmp_path):
    nb = {"cells": [
        {"cell_type": "markdown", "source": ["Hello there.\n"]},
        {"cell_type": "code", "source": ["print('hi')\n"]},
    ]}
    src = tmp_path / "a.ipynb"
    src.write_text(json.dumps(nb), encoding="utf-8")
    dst = tmp_path / "out" / "a.ipynb"
    ts.translate_notebook(str(src), str(dst), UP)
    result = json.loads(dst.read_text(encoding="utf-8"))
    assert "HELLO THERE." in "".join(result["cells"][0]["source"])
    assert "print('hi')" in "".join(result["cells"][1]["source"])


def test_myst_yml_translates_titles_and_toc(tmp_path, monkeypatch):
    config = {
        "project": {"title": "My Book", "subtitle": "A course",
                    "toc": [{"file": "index.md"}, {"title": "Labs", "children": []}]},
        "site": {"options": {"logo_text": "My Book"}},
    }
    monkeypatch.setattr(ts, "TRANSLATED_DIR", str(tmp_path))
    ts.create_french_myst_yml(config, UP)
    text = (tmp_path / "myst.yml").read_text(encoding="utf-8")
    assert "MY BOOK" in text
    assert "A COURSE" in text
    assert "LABS" in text


@pytest.mark.parametrize("path", [
    "index.md", "labs/lab1.md", "labs/lab2.md", "labs/lab5.md", "lectures/lecture1.md",
])
def test_golden_real_sources_preserve_code_blocks(tmp_path, path):
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    src = os.path.join(root, path)
    if not os.path.exists(src):
        pytest.skip(path + " not present")
    dst = tmp_path / "out.md"
    ts.translate_md_file(src, str(dst), UP)
    original = open(src, encoding="utf-8").read()
    assert fences(dst.read_text(encoding="utf-8")) == fences(original)


def test_main_exits_nonzero_when_a_string_is_unresolved(tmp_path, monkeypatch):
    def always_fail(text):
        raise RuntimeError("nope")

    monkeypatch.setattr(ts, "make_google_translator", lambda **kw: always_fail)
    monkeypatch.setattr(ts, "ROOT_DIR", str(tmp_path))
    (tmp_path / "myst.yml").write_text(
        "project:\n  title: My Book\n  toc:\n  - file: index.md\n", encoding="utf-8")
    (tmp_path / "index.md").write_text("Some prose.\n", encoding="utf-8")
    monkeypatch.setattr(ts, "TRANSLATED_DIR", str(tmp_path / "_translated"))
    assert ts.main(["--cache", str(tmp_path / "c.json")]) == 1
