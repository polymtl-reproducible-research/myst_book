import json
import os
import re
import pytest
import translate_sources as ts
from resolver import Resolver

FENCE = re.compile(r"^(`{3,}|~{3,})")
FENCE_DIRECTIVE = re.compile(r"^(`{3,}|~{3,})\{")
UP = str.upper


def fences(text):
    """Plain fenced CODE blocks only. Fenced directives hold translatable prose."""
    out, buf, inside, is_directive = [], [], False, False
    for line in text.split("\n"):
        if FENCE.match(line):
            if not inside:
                is_directive = bool(FENCE_DIRECTIVE.match(line))
                inside, buf = True, [line]
            else:
                buf.append(line)
                if not is_directive:
                    out.append(buf)
                buf, inside = [], False
        elif inside:
            buf.append(line)
    return out


def test_report_lists_every_unresolved_string():
    report = ts.report_unresolved(["Labs", "Lectures"])
    assert "2 strings could not be translated" in report
    assert "Labs" in report and "Lectures" in report


def test_report_mentions_the_overrides_file():
    assert "translations/fr.overrides.json" in ts.report_unresolved(["Labs"])


def test_report_shows_the_exact_override_key_when_it_differs():
    report = ts.report_unresolved(["See [the guide](https://e.com) now."],
                                  ["See [the guide]XPHX0XPHX now."])
    assert "override key: See [the guide]XPHX0XPHX now." in report


def test_report_omits_the_key_when_identical():
    assert "override key" not in ts.report_unresolved(["Labs"], ["Labs"])


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


def untranslated_prose(original, translated):
    """Source prose lines that survived byte-identical => never reached the translator.

    Deliberately does NOT re-parse the source for structure. A coverage check that
    trusts the same block boundaries the segmenter produced would inherit the very
    bug it is meant to catch. Prose is identified purely by content: three or more
    lowercase words. Equations, paths, options and table rules do not qualify.
    """
    out = set(translated.split("\n"))
    suspects = []
    for line in original.split("\n"):
        s = line.strip()
        if s.startswith((":", "|", "$$")) or re.match(r"^(`{3,}|~{3,})", s):
            continue
        if len(re.findall(r"\b[a-z]{3,}\b", s)) >= 3 and line in out:
            suspects.append(s)
    return suspects


@pytest.mark.parametrize("path", [
    "index.md", "labs/lab1.md", "labs/lab2.md", "labs/lab5.md", "lectures/lecture1.md",
])
def test_golden_real_sources_translate_all_their_prose(tmp_path, path):
    """Coverage guard: catches a segmenter bug that swallows prose into a verbatim
    block. An integrity check cannot see this, because swallowed content is preserved
    perfectly and only the translation is missing."""
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    src = os.path.join(root, path)
    if not os.path.exists(src):
        pytest.skip(path + " not present")
    dst = tmp_path / "out.md"
    ts.translate_md_file(src, str(dst), UP)
    original = open(src, encoding="utf-8").read()
    missed = untranslated_prose(original, dst.read_text(encoding="utf-8"))
    assert missed == [], "prose never reached the translator: %r" % missed[:3]


def test_main_exits_nonzero_when_a_string_is_unresolved(tmp_path, monkeypatch):
    def always_fail(text):
        raise RuntimeError("nope")

    monkeypatch.setattr(ts, "make_google_translator", lambda **kw: always_fail)
    monkeypatch.setattr(ts, "ROOT_DIR", str(tmp_path))
    (tmp_path / "myst.yml").write_text(
        "project:\n  title: My Book\n  toc:\n  - file: index.md\n", encoding="utf-8")
    (tmp_path / "index.md").write_text("Some prose.\n", encoding="utf-8")
    monkeypatch.setattr(ts, "TRANSLATED_DIR", str(tmp_path / "_translated"))
    monkeypatch.setattr(ts, "OVERRIDES_PATH", str(tmp_path / "overrides.json"))
    assert ts.main(["--cache", str(tmp_path / "c.json")]) == 1


def test_non_mapping_frontmatter_warns_and_is_left_alone(capsys):
    fm = "---\n- a\n- b\n---\n"
    assert ts._translate_frontmatter(fm, UP, ("title",)) == fm
    assert "not a mapping" in capsys.readouterr().err


def test_malformed_yaml_frontmatter_warns_and_is_left_alone(capsys):
    fm = "---\ntitle: [unclosed\n---\n"
    assert ts._translate_frontmatter(fm, UP, ("title",)) == fm
    assert "not valid YAML" in capsys.readouterr().err


def test_a_resolver_error_is_not_swallowed():
    def boom(text):
        raise ValueError("resolver bug")
    with pytest.raises(ValueError):
        ts._translate_frontmatter("---\ntitle: Lab 1\n---\n", boom, ("title",))


def test_main_succeeds_and_writes_the_cache(tmp_path, monkeypatch):
    monkeypatch.setattr(ts, "make_google_translator", lambda **kw: (lambda t: "FR:" + t))
    monkeypatch.setattr(ts, "ROOT_DIR", str(tmp_path))
    monkeypatch.setattr(ts, "TRANSLATED_DIR", str(tmp_path / "_translated"))
    monkeypatch.setattr(ts, "OVERRIDES_PATH", str(tmp_path / "overrides.json"))
    (tmp_path / "myst.yml").write_text(
        "project:\n  title: My Book\n  toc:\n  - file: index.md\n", encoding="utf-8")
    (tmp_path / "index.md").write_text("Some prose.\n", encoding="utf-8")
    cache = tmp_path / "c.json"
    assert ts.main(["--cache", str(cache)]) == 0
    assert cache.exists()
    assert json.loads(cache.read_text(encoding="utf-8"))
