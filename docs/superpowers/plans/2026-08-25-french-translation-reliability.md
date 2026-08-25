# French Translation Reliability Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the French build deterministic and fail-loud, so `/fr/` can never ship a mix of French and English.

**Architecture:** Split the monolithic line-walking translator into four stages — shield, segment, resolve, render — with the translator injected as a callable so the parser is testable without network access. A bot-owned cache on an orphan branch plus a human-owned overrides file in `main` make repeat builds hit zero network calls; retry with backoff covers genuine misses; anything still unresolved fails the build.

**Tech Stack:** Python 3.14, `deep-translator`, `pyyaml`, pytest, GitHub Actions, mystmd.

**Spec:** `docs/superpowers/specs/2026-08-25-french-translation-reliability-design.md`

## Global Constraints

- **Remote:** `staging` (`mathieuboudreau/myst_book-staging`) ONLY. Never push to `origin`. Always name the remote explicitly — the branch's tracking is `staging/mb/tradfix`.
- **Branch:** all work on `mb/tradfix`.
- Runtime dependencies stay exactly `deep-translator` + `pyyaml`. No new runtime deps. pytest is test-only.
- Resolution order is always: **overrides → cache → translate → unresolved**.
- Cache JSON is written `sort_keys=True, indent=2, ensure_ascii=False`, trailing newline.
- The cache writer **only adds keys; it never overwrites an existing key.**
- Default retry attempts: **8**. Backoff 1s doubling, capped at 30s, with jitter.
- Machine cache: `fr.cache.json` on orphan branch `translation-cache`.
- Human overrides: `translations/fr.overrides.json` on `mb/tradfix`/`main`.
- Cache write-back commit message must contain `[skip ci]`.
- Placeholder token format is `XPHX{n}XPHX`.
- Every module in `scripts/` is imported by bare name (the script's own directory is on `sys.path`); tests rely on `tests/conftest.py` to replicate that.

---

### Task 1: Shielding and validation

**Files:**
- Create: `scripts/shielding.py`
- Create: `tests/conftest.py`
- Test: `tests/test_shielding.py`

**Interfaces:**
- Consumes: nothing.
- Produces: `shield(text) -> (str, list[str])`, `restore(text, placeholders) -> str`, `validate(source_protected, translated_protected) -> bool`.

- [ ] **Step 1: Write `tests/conftest.py` so `scripts/` is importable**

```python
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
```

- [ ] **Step 2: Write the failing tests**

```python
import pytest
from shielding import shield, restore, validate


def test_shields_myst_role():
    protected, ph = shield("See {cite:p}`smith2020` for detail.")
    assert protected == "See XPHX0XPHX for detail."
    assert ph == ["{cite:p}`smith2020`"]


def test_shields_inline_code_and_math():
    protected, ph = shield("Run `git init` when $x > 0$.")
    assert "`git init`" not in protected
    assert "$x > 0$" not in protected
    assert len(ph) == 2


def test_shields_external_link_target_but_not_link_text():
    protected, ph = shield('See [the MyST guide](https://mystmd.org/guide).')
    assert protected == "See [the MyST guide]XPHX0XPHX."
    assert ph == ["](https://mystmd.org/guide)"]


def test_shields_crossref_link_target():
    protected, ph = shield("Defined in [Lab 2](#lab2).")
    assert protected == "Defined in [Lab 2]XPHX0XPHX."


def test_round_trip_is_identity_when_untranslated():
    original = 'Use `x` and [a link](https://e.com) and {ref}`lab1`.'
    protected, ph = shield(original)
    assert restore(protected, ph) == original


def test_restore_raises_on_unknown_placeholder():
    with pytest.raises(KeyError):
        restore("XPHX7XPHX", [])


def test_validate_accepts_faithful_translation():
    src, _ = shield("See [the guide](https://e.com) and `code`.")
    dst = "Voir [le guide]XPHX0XPHX et XPHX1XPHX."
    assert validate(src, dst) is True


def test_validate_rejects_dropped_placeholder():
    src, _ = shield("Run `git init` now.")
    assert validate(src, "Lancez maintenant.") is False


def test_validate_rejects_broken_brackets():
    src, _ = shield("See [the guide](https://e.com).")
    assert validate(src, "Voir le guide]XPHX0XPHX.") is False


def test_validate_rejects_broken_emphasis():
    src, _ = shield("This is **important** here.")
    assert validate(src, "Ceci est *important* ici.") is False
```

- [ ] **Step 3: Run the tests to verify they fail**

Run: `python3 -m pytest tests/test_shielding.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'shielding'`

- [ ] **Step 4: Implement `scripts/shielding.py`**

```python
"""Protect non-translatable inline markup from the translator.

Spans that must survive translation byte-for-byte (MyST roles, inline math,
inline code, link targets) are replaced with XPHX<n>XPHX placeholders before
the text is sent out, and substituted back afterwards.
"""

import re

PLACEHOLDER = "XPHX{}XPHX"
_PH_RE = re.compile(r"XPHX(\d+)XPHX")

# Applied in order. Link targets come last so that inline code inside link
# text is shielded first.
_PATTERNS = (
    r"\{[a-zA-Z:_-]+\}`[^`]*`",                 # MyST roles: {cite:p}`key`
    r"(?<!\$)\$(?!\$)(?:.+?)(?<!\$)\$(?!\$)",   # inline math: $x$
    r"`[^`]+`",                                 # inline code: `code`
    r"\]\([^)]*\)",                             # link targets: ](url) and ](#ref)
)


def shield(text):
    """Replace non-translatable spans with placeholders.

    Returns (protected_text, placeholders) where placeholders[i] is the
    original span for XPHX<i>XPHX.
    """
    placeholders = []

    def _sub(match):
        placeholders.append(match.group(0))
        return PLACEHOLDER.format(len(placeholders) - 1)

    protected = text
    for pattern in _PATTERNS:
        protected = re.sub(pattern, _sub, protected)
    return protected, placeholders


def restore(text, placeholders):
    """Substitute placeholders back into text.

    Raises KeyError if the text references a placeholder that does not exist.
    """

    def _sub(match):
        index = int(match.group(1))
        if index >= len(placeholders):
            raise KeyError(match.group(0))
        return placeholders[index]

    return _PH_RE.sub(_sub, text)


def validate(source_protected, translated_protected):
    """True if the translation preserved every structural marker.

    Checks placeholder identity, bracket balance (which is how link damage
    shows up once targets are shielded), and bold-marker parity.
    """
    if _placeholder_ids(source_protected) != _placeholder_ids(translated_protected):
        return False
    for marker in ("[", "]", "**"):
        if source_protected.count(marker) != translated_protected.count(marker):
            return False
    return True


def _placeholder_ids(text):
    return sorted(int(n) for n in _PH_RE.findall(text))
```

- [ ] **Step 5: Run the tests to verify they pass**

Run: `python3 -m pytest tests/test_shielding.py -v`
Expected: 10 passed

- [ ] **Step 6: Commit**

```bash
git add scripts/shielding.py tests/conftest.py tests/test_shielding.py
git commit -m "Add inline-markup shielding with structural validation"
```

---

### Task 2: Block segmenter

**Files:**
- Create: `scripts/md_segmenter.py`
- Test: `tests/test_md_segmenter.py`

**Interfaces:**
- Consumes: nothing (pure text in, text out).
- Produces: `Block(kind, lines, meta)`, `segment(body) -> list[Block]`, `render(blocks, translate) -> str`, `translate_body(body, translate) -> str`. `translate` is `Callable[[str], str]`. Block kinds: `fence`, `math`, `directive`, `table`, `heading`, `list_item`, `paragraph`, `blank`.

- [ ] **Step 1: Write the failing tests**

```python
from md_segmenter import segment, translate_body

UP = str.upper


def kinds(body):
    return [b.kind for b in segment(body)]


def test_wrapped_paragraph_becomes_one_block():
    body = "Modern research depends on code\nand data pipelines."
    assert kinds(body) == ["paragraph"]
    assert translate_body(body, UP) == "MODERN RESEARCH DEPENDS ON CODE AND DATA PIPELINES."


def test_blank_line_separates_paragraphs():
    assert kinds("One line.\n\nTwo line.") == ["paragraph", "blank", "paragraph"]


def test_fenced_code_is_preserved_verbatim():
    body = "```python\nx = 1  # keep me\n```"
    assert kinds(body) == ["fence"]
    assert translate_body(body, UP) == body


def test_math_block_is_preserved_verbatim():
    body = "$$\na = b\n$$"
    assert translate_body(body, UP) == body


def test_heading_keeps_prefix():
    assert translate_body("## Some heading", UP) == "## SOME HEADING"


def test_list_item_keeps_marker_and_indent():
    assert translate_body("  - a point", UP) == "  - A POINT"


def test_list_items_are_separate_blocks():
    assert kinds("- one\n- two") == ["list_item", "list_item"]


def test_table_separator_row_is_preserved():
    body = "| Term | Definition |\n|------|------------|\n| Data | Facts |"
    out = translate_body(body, UP).split("\n")
    assert out[1] == "|------|------------|"
    assert out[0] == "| TERM | DEFINITION |"


def test_unknown_directive_is_preserved_verbatim():
    body = ":::{iframe} https://example.com/slides\n:width: 100%\n:::"
    assert translate_body(body, UP) == body


def test_admonition_translates_title_and_body():
    body = ":::{note} Key takeaway\nThis matters.\n:::"
    out = translate_body(body, UP)
    assert out.startswith(":::{note} KEY TAKEAWAY")
    assert "THIS MATTERS." in out
    assert out.endswith(":::")


def test_admonition_preserves_nested_code_block():
    body = ":::{tip} Try it\n```bash\ngit init\n```\n:::"
    assert "git init" in translate_body(body, UP)
    assert "GIT INIT" not in translate_body(body, UP)


def test_figure_translates_caption_but_not_options():
    body = ":::{figure} images/x.png\n:width: 50%\nA caption here.\n:::"
    out = translate_body(body, UP).split("\n")
    assert out[0] == ":::{figure} images/x.png"
    assert out[1] == ":width: 50%"
    assert out[2] == "A CAPTION HERE."


def test_body_with_no_prose_is_unchanged():
    body = "```\ncode\n```\n\n$$\nx\n$$"
    assert translate_body(body, UP) == body
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python3 -m pytest tests/test_md_segmenter.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'md_segmenter'`

- [ ] **Step 3: Implement `scripts/md_segmenter.py`**

```python
"""Split a MyST markdown body into typed blocks and render them back.

Prose is translated a block at a time rather than a line at a time, so a
hard-wrapped paragraph reaches the translator as one coherent sentence
instead of a series of mid-sentence fragments.
"""

import re
from dataclasses import dataclass, field

# Admonition directives whose title and body are translated. Every other
# directive except `figure` is preserved verbatim.
ADMONITION_DIRECTIVES = {
    "admonition", "attention", "caution", "danger", "error", "hint",
    "important", "note", "seealso", "tip", "warning",
}

FENCE_RE = re.compile(r"^(`{3,}|~{3,})")
DIRECTIVE_RE = re.compile(r"^(:{3,})\{(.+?)\}")
TABLE_RE = re.compile(r"^\s*\|")
TABLE_SEP_RE = re.compile(r"^\s*\|[\s\-:|]+\|\s*$")
HEADING_RE = re.compile(r"^(#{1,6}\s+)(.*)$")
LIST_RE = re.compile(r"^(\s*(?:[-*+]|\d+\.)\s+)(.*)$")
HAS_WORDS_RE = re.compile(r"[a-zA-Z]{2,}")


@dataclass
class Block:
    kind: str
    lines: list
    meta: dict = field(default_factory=dict)


def segment(body):
    """Split a markdown body into typed blocks."""
    lines = body.split("\n")
    blocks = []
    para = []
    i = 0

    def flush():
        if para:
            blocks.append(Block("paragraph", list(para)))
            para.clear()

    while i < len(lines):
        line = lines[i]

        fence = FENCE_RE.match(line)
        if fence:
            flush()
            char = fence.group(1)[0]
            close = re.compile(r"^" + re.escape(char) + r"{" + str(len(fence.group(1))) + r",}\s*$")
            buf = [line]
            i += 1
            while i < len(lines):
                buf.append(lines[i])
                closed = close.match(lines[i])
                i += 1
                if closed:
                    break
            blocks.append(Block("fence", buf))
            continue

        directive = DIRECTIVE_RE.match(line)
        if directive:
            flush()
            closing = ":" * len(directive.group(1))
            buf = [line]
            i += 1
            while i < len(lines) and lines[i] != closing:
                buf.append(lines[i])
                i += 1
            closed = i < len(lines)
            if closed:
                buf.append(lines[i])
                i += 1
            blocks.append(Block("directive", buf, {"name": directive.group(2), "closed": closed}))
            continue

        if line.strip().startswith("$$"):
            flush()
            buf = [line]
            i += 1
            if line.strip() == "$$" or not line.strip().endswith("$$"):
                while i < len(lines):
                    buf.append(lines[i])
                    ends = lines[i].strip().endswith("$$")
                    i += 1
                    if ends:
                        break
            blocks.append(Block("math", buf))
            continue

        if not line.strip():
            flush()
            blocks.append(Block("blank", [line]))
            i += 1
            continue

        if TABLE_RE.match(line):
            flush()
            buf = []
            while i < len(lines) and TABLE_RE.match(lines[i]):
                buf.append(lines[i])
                i += 1
            blocks.append(Block("table", buf))
            continue

        if HEADING_RE.match(line):
            flush()
            blocks.append(Block("heading", [line]))
            i += 1
            continue

        if LIST_RE.match(line):
            flush()
            blocks.append(Block("list_item", [line]))
            i += 1
            continue

        para.append(line)
        i += 1

    flush()
    return blocks


def translate_body(body, translate):
    """Convenience wrapper: segment a body and render it translated."""
    return render(segment(body), translate)


def render(blocks, translate):
    out = []
    for block in blocks:
        out.extend(render_block(block, translate))
    return "\n".join(out)


def render_block(block, translate):
    if block.kind in ("fence", "math", "blank"):
        return list(block.lines)
    if block.kind == "heading":
        return [_render_prefixed(block.lines[0], HEADING_RE, translate)]
    if block.kind == "list_item":
        return [_render_prefixed(block.lines[0], LIST_RE, translate)]
    if block.kind == "paragraph":
        return [translate(" ".join(line.strip() for line in block.lines))]
    if block.kind == "table":
        return [_render_table_row(line, translate) for line in block.lines]
    if block.kind == "directive":
        return _render_directive(block, translate)
    raise ValueError("unknown block kind: " + block.kind)


def _render_prefixed(line, pattern, translate):
    prefix, text = pattern.match(line).groups()
    if not HAS_WORDS_RE.search(text):
        return line
    return prefix + translate(text)


def _render_table_row(line, translate):
    if TABLE_SEP_RE.match(line):
        return line
    cells = []
    for cell in line.split("|"):
        stripped = cell.strip()
        if stripped and HAS_WORDS_RE.search(stripped):
            cells.append(" " + translate(stripped) + " ")
        else:
            cells.append(cell)
    return "|".join(cells)


def _render_directive(block, translate):
    name = block.meta["name"]
    opening, inner, closing = _split_directive(block)

    if name == "figure":
        rendered = []
        for line in inner:
            if line.startswith(":") or not line.strip():
                rendered.append(line)
            else:
                rendered.append(translate(line.strip()))
        return [opening] + rendered + closing

    if name in ADMONITION_DIRECTIVES:
        head, _, title = opening.partition("}")
        first = head + "} " + translate(title.strip()) if title.strip() else opening
        # Recurse so nested code blocks, lists and paragraphs are handled.
        body = render(segment("\n".join(inner)), translate).split("\n") if inner else []
        return [first] + body + closing

    return list(block.lines)


def _split_directive(block):
    """Return (opening_line, inner_lines, closing_lines)."""
    if block.meta.get("closed") and len(block.lines) >= 2:
        return block.lines[0], block.lines[1:-1], [block.lines[-1]]
    return block.lines[0], block.lines[1:], []
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `python3 -m pytest tests/test_md_segmenter.py -v`
Expected: 13 passed

- [ ] **Step 5: Commit**

```bash
git add scripts/md_segmenter.py tests/test_md_segmenter.py
git commit -m "Add block-level markdown segmenter"
```

---

### Task 3: Resolver

**Files:**
- Create: `scripts/resolver.py`
- Test: `tests/test_resolver.py`

**Interfaces:**
- Consumes: `shield`, `restore`, `validate` from Task 1.
- Produces: `Resolver(translate_fn, cache=None, overrides=None)` with `.resolve(text) -> str`, `.unresolved -> list[str]`, `.cache -> dict`, `.added -> int`; module functions `load_json(path) -> dict`, `save_json(path, data) -> None`.

- [ ] **Step 1: Write the failing tests**

```python
import json
from resolver import Resolver, load_json, save_json


def fake(mapping, fail=()):
    def translate(text):
        if text in fail:
            raise RuntimeError("boom")
        return mapping.get(text, "FR:" + text)
    return translate


def test_cache_hit_skips_the_network():
    calls = []

    def translate(text):
        calls.append(text)
        return "never"

    r = Resolver(translate, cache={"Labs": "Laboratoires"})
    assert r.resolve("Labs") == "Laboratoires"
    assert calls == []


def test_override_wins_over_cache():
    r = Resolver(fake({}), cache={"Lectures": "Conferences"}, overrides={"Lectures": "Cours"})
    assert r.resolve("Lectures") == "Cours"


def test_miss_is_translated_and_cached():
    r = Resolver(fake({"Labs": "Laboratoires"}))
    assert r.resolve("Labs") == "Laboratoires"
    assert r.cache["Labs"] == "Laboratoires"
    assert r.added == 1


def test_cache_is_never_overwritten():
    r = Resolver(fake({"Labs": "NEW"}), cache={"Labs": "PINNED"})
    r.resolve("Labs")
    assert r.cache["Labs"] == "PINNED"


def test_failure_records_unresolved_and_keeps_english():
    r = Resolver(fake({}, fail={"Labs"}))
    assert r.resolve("Labs") == "Labs"
    assert r.unresolved == ["Labs"]


def test_invalid_translation_is_treated_as_failure():
    # Translator drops the placeholder for `git init`.
    r = Resolver(fake({"Run XPHX0XPHX now.": "Lancez maintenant."}))
    assert r.resolve("Run `git init` now.") == "Run `git init` now."
    assert r.unresolved == ["Run `git init` now."]


def test_placeholders_survive_a_cache_hit():
    r = Resolver(fake({}), cache={"See [the guide]XPHX0XPHX.": "Voir [le guide]XPHX0XPHX."})
    assert r.resolve("See [the guide](https://e.com).") == "Voir [le guide](https://e.com)."


def test_text_without_words_is_returned_unchanged():
    calls = []
    r = Resolver(lambda t: calls.append(t))
    assert r.resolve("  42 — 7  ") == "  42 — 7  "
    assert calls == []


def test_save_json_is_sorted_and_unicode(tmp_path):
    path = tmp_path / "fr.cache.json"
    save_json(str(path), {"b": "café", "a": "thé"})
    text = path.read_text(encoding="utf-8")
    assert text.index('"a"') < text.index('"b"')
    assert "café" in text
    assert text.endswith("\n")


def test_load_json_returns_empty_for_missing_file(tmp_path):
    assert load_json(str(tmp_path / "nope.json")) == {}
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python3 -m pytest tests/test_resolver.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'resolver'`

- [ ] **Step 3: Implement `scripts/resolver.py`**

```python
"""Resolve English strings to French: overrides, then cache, then translation.

The resolver never raises on a translation failure. It records the offending
string in `unresolved` and returns the English original, so the caller can
report every failure at once and exit non-zero.
"""

import json
import os
import re

from shielding import restore, shield, validate

HAS_WORDS_RE = re.compile(r"[a-zA-Z]{2,}")


def load_json(path):
    """Read a JSON object, returning {} when the file does not exist."""
    if not path or not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def save_json(path, data):
    """Write a JSON object sorted, indented, and readable in diffs."""
    parent = os.path.dirname(os.path.abspath(path))
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


class Resolver:
    def __init__(self, translate_fn, cache=None, overrides=None):
        self.translate_fn = translate_fn
        self.cache = dict(cache or {})
        self.overrides = dict(overrides or {})
        self.unresolved = []
        self.added = 0

    def resolve(self, text):
        stripped = text.strip()
        if not stripped or not HAS_WORDS_RE.search(stripped):
            return text

        protected, placeholders = shield(stripped)

        if protected in self.overrides:
            return restore(self.overrides[protected], placeholders)
        if protected in self.cache:
            return restore(self.cache[protected], placeholders)

        try:
            result = self.translate_fn(protected)
        except Exception:
            result = None

        if not result or not validate(protected, result):
            self.unresolved.append(stripped)
            return text

        if protected not in self.cache:   # never overwrite an existing entry
            self.cache[protected] = result
            self.added += 1
        return restore(result, placeholders)
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `python3 -m pytest tests/test_resolver.py -v`
Expected: 10 passed

- [ ] **Step 5: Commit**

```bash
git add scripts/resolver.py tests/test_resolver.py
git commit -m "Add override/cache/translate resolver with never-overwrite cache"
```

---

### Task 4: Google backend with retry

**Files:**
- Create: `scripts/translator_backend.py`
- Test: `tests/test_translator_backend.py`

**Interfaces:**
- Consumes: nothing from earlier tasks.
- Produces: `make_google_translator(attempts=8, sleep=time.sleep, translator=None) -> Callable[[str], str]`. Raises the last exception when every attempt fails.

- [ ] **Step 1: Write the failing tests**

```python
import pytest
from translator_backend import make_google_translator


class Flaky:
    """Fails `failures` times, then succeeds."""

    def __init__(self, failures, result="Laboratoires"):
        self.failures = failures
        self.result = result
        self.calls = 0

    def translate(self, text):
        self.calls += 1
        if self.calls <= self.failures:
            raise RuntimeError("TranslationNotFound")
        return self.result


def test_succeeds_on_first_attempt():
    backend = Flaky(failures=0)
    translate = make_google_translator(translator=backend, sleep=lambda s: None)
    assert translate("Labs") == "Laboratoires"
    assert backend.calls == 1


def test_retries_until_success():
    backend = Flaky(failures=5)
    translate = make_google_translator(translator=backend, sleep=lambda s: None)
    assert translate("Labs") == "Laboratoires"
    assert backend.calls == 6


def test_raises_after_exhausting_attempts():
    backend = Flaky(failures=99)
    translate = make_google_translator(attempts=3, translator=backend, sleep=lambda s: None)
    with pytest.raises(RuntimeError):
        translate("Labs")
    assert backend.calls == 3


def test_empty_result_counts_as_failure():
    backend = Flaky(failures=0, result="")
    translate = make_google_translator(attempts=2, translator=backend, sleep=lambda s: None)
    with pytest.raises(Exception):
        translate("Labs")
    assert backend.calls == 2


def test_backoff_grows_and_is_capped():
    delays = []
    backend = Flaky(failures=99)
    translate = make_google_translator(attempts=8, translator=backend, sleep=delays.append)
    with pytest.raises(RuntimeError):
        translate("Labs")
    assert len(delays) == 7          # one sleep between each pair of attempts
    assert delays[0] < delays[3]     # grows
    assert max(delays) <= 30.0       # capped (jitter multiplier is <= 1.5 of cap/2)


def test_no_sleep_after_the_final_attempt():
    delays = []
    backend = Flaky(failures=0)
    translate = make_google_translator(translator=backend, sleep=delays.append)
    translate("Labs")
    assert delays == []
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python3 -m pytest tests/test_translator_backend.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'translator_backend'`

- [ ] **Step 3: Implement `scripts/translator_backend.py`**

```python
"""Google Translate backend with retry and backoff.

The free endpoint raises TranslationNotFound nondeterministically at roughly a
2-in-3 rate regardless of content, so a single attempt is not meaningful. This
is the only module that knows about the network.
"""

import random
import time

BASE_DELAY = 1.0
MAX_DELAY = 30.0


def make_google_translator(attempts=8, sleep=time.sleep, translator=None):
    """Return a callable that translates English to French, retrying on failure."""
    if translator is None:
        from deep_translator import GoogleTranslator

        translator = GoogleTranslator(source="en", target="fr")

    def translate(text):
        delay = BASE_DELAY
        last_error = None
        for attempt in range(attempts):
            try:
                result = translator.translate(text)
                if result:
                    return result
                last_error = ValueError("empty translation for: " + text)
            except Exception as error:
                last_error = error
            if attempt < attempts - 1:
                capped = min(delay, MAX_DELAY)
                sleep(capped * (0.5 + random.random()) / 1.5)
                delay *= 2
        raise last_error

    return translate
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `python3 -m pytest tests/test_translator_backend.py -v`
Expected: 6 passed

- [ ] **Step 5: Commit**

```bash
git add scripts/translator_backend.py tests/test_translator_backend.py
git commit -m "Add Google translate backend with retry and backoff"
```

---

### Task 5: Rewire `translate_sources.py`

**Files:**
- Rename: `scripts/translate-sources.py` → `scripts/translate_sources.py`
- Modify: whole file (rewrite of `translate_text`, `translate_markdown_body`, `translate_prose_line`, `main`)
- Test: `tests/test_translate_sources.py`

**Interfaces:**
- Consumes: `Resolver`, `load_json`, `save_json` (Task 3); `translate_body` (Task 2); `make_google_translator` (Task 4).
- Produces: `translate_md_file(src, dst, resolve)`, `translate_notebook(src, dst, resolve)`, `create_french_myst_yml(config, resolve)`, `report_unresolved(unresolved) -> str`, `main(argv=None) -> int`.

The file keeps its existing helpers unchanged: `split_frontmatter`, `collect_source_files`, `copy_site_option_assets`. `translate_text`, `translate_markdown_body`, and `translate_prose_line` are deleted — the module-level `TRANSLATOR` global goes with them.

- [ ] **Step 1: Rename the file so it can be imported**

```bash
git mv scripts/translate-sources.py scripts/translate_sources.py
```

- [ ] **Step 2: Write the failing tests**

```python
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
```

- [ ] **Step 3: Run the tests to verify they fail**

Run: `python3 -m pytest tests/test_translate_sources.py -v`
Expected: FAIL — `AttributeError: module 'translate_sources' has no attribute 'report_unresolved'`

- [ ] **Step 4: Rewrite the changed parts of `scripts/translate_sources.py`**

Replace the imports and the deleted functions with the following. `split_frontmatter`, `collect_source_files`, and `copy_site_option_assets` stay exactly as they are.

```python
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
```

Then the translating helpers, each now taking a `resolve` callable:

```python
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
```

And the new `main`:

```python
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
```

- [ ] **Step 5: Run the new tests**

Run: `python3 -m pytest tests/test_translate_sources.py -v`
Expected: all pass

- [ ] **Step 6: Run the whole suite**

Run: `python3 -m pytest tests/ -v`
Expected: all pass, no network access

- [ ] **Step 7: Commit**

```bash
git add scripts/translate_sources.py tests/test_translate_sources.py
git commit -m "Rewire translator around segmenter, resolver, and retry backend"
```

---

### Task 6: Orchestrator passthrough and test workflow

**Files:**
- Modify: `scripts/build-french.py:4` (docstring), `:36` (script reference), `main()` (argument passthrough)
- Create: `.github/workflows/tests.yml`

**Interfaces:**
- Consumes: `translate_sources.main` CLI flags from Task 5.
- Produces: `python3 scripts/build-french.py [--cache PATH] [--attempts N]`.

- [ ] **Step 1: Add argument parsing to `main()`**

In `scripts/build-french.py`, add `import argparse` at the top, change the
signature to `def main(argv=None):`, and insert at the top of the body:

```python
    parser = argparse.ArgumentParser(description="Build the French version of the book.")
    parser.add_argument("--cache", help="path to the machine cache JSON")
    parser.add_argument("--attempts", type=int, help="translation attempts per string")
    args = parser.parse_args(argv)

    forwarded = []
    if args.cache:
        forwarded += ["--cache", args.cache]
    if args.attempts is not None:
        forwarded += ["--attempts", str(args.attempts)]
```

Change the entry point at the bottom of the file to `sys.exit(main())`.

- [ ] **Step 2: Update the script reference and docstring**

In `scripts/build-french.py`, change line 4 from `translate-sources.py` to `translate_sources.py`, and line 36 from:

```python
    run([sys.executable, os.path.join(ROOT_DIR, "scripts", "translate-sources.py")])
```

to:

```python
    cmd = [sys.executable, os.path.join(ROOT_DIR, "scripts", "translate_sources.py")]
    cmd += forwarded
    run(cmd)
```

- [ ] **Step 3: Verify the flags are accepted**

Run: `python3 scripts/build-french.py --help`
Expected: usage text listing `--cache` and `--attempts`

- [ ] **Step 4: Create `.github/workflows/tests.yml`**

PRs do not currently build anything, so a parser regression would otherwise only surface after merge.

```yaml
name: Tests

on:
  pull_request:
  push:
    branches:
      - '**'

jobs:
  pytest:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-python@v7
        with:
          python-version: "3.14"
      - run: pip install pytest pyyaml
      - run: python3 -m pytest tests/ -v
```

- [ ] **Step 5: Run the suite once more**

Run: `python3 -m pytest tests/ -v`
Expected: all pass

- [ ] **Step 6: Commit**

```bash
git add scripts/build-french.py .github/workflows/tests.yml
git commit -m "Forward cache options through build-french and run tests in CI"
```

---

### Task 7: Deploy workflow — cache branch and write-back

**Files:**
- Modify: `.github/workflows/deploy.yml`
- Create: `translations/fr.overrides.json`

**Interfaces:**
- Consumes: `--cache` from Task 6.
- Produces: a build that reads `.tcache/fr.cache.json` from branch `translation-cache` and pushes updates back to it.

- [ ] **Step 1: Create the empty overrides file**

```bash
mkdir -p translations
printf '{}\n' > translations/fr.overrides.json
```

- [ ] **Step 2: Add `contents: write` and `BASE_URL` to the build job**

In `.github/workflows/deploy.yml`, inside `jobs.build`, above `steps:`:

```yaml
    permissions:
      contents: write
    env:
      BASE_URL: ${{ vars.BASE_URL }}
```

`vars.BASE_URL` is unset on `origin`, evaluating to `""`, which is exactly the current production behavior. On staging it is set to `/myst_book-staging`.

- [ ] **Step 3: Add the cache checkout after the existing content checkout**

```yaml
      - name: Checkout translation cache
        uses: actions/checkout@v7
        continue-on-error: true
        with:
          ref: translation-cache
          path: .tcache
```

`continue-on-error` tolerates the branch not existing yet; the resolver then starts from an empty cache.

- [ ] **Step 4: Pass the cache path to the build**

Change the French build step to:

```yaml
      - name: Translate and build French book
        run: python3 scripts/build-french.py --cache .tcache/fr.cache.json
```

- [ ] **Step 5: Add the write-back step immediately after it**

It must come before the slower deploy so `cancel-in-progress: true` cannot discard newly translated entries.

```yaml
      - name: Commit refreshed translation cache
        continue-on-error: true
        working-directory: .tcache
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git add fr.cache.json
          if git diff --cached --quiet; then
            echo "cache unchanged"
          else
            git commit -m "Update French translation cache [skip ci]"
            git pull --rebase origin translation-cache
            git push origin HEAD:translation-cache
          fi
```

- [ ] **Step 6: Verify the workflow parses**

Run: `python3 -c "import yaml,sys; yaml.safe_load(open('.github/workflows/deploy.yml')); yaml.safe_load(open('.github/workflows/tests.yml')); print('both valid')"`
Expected: `both valid`

- [ ] **Step 7: Commit**

```bash
git add .github/workflows/deploy.yml translations/fr.overrides.json
git commit -m "Read translation cache from its own branch and write updates back"
```

---

### Task 8: Bootstrap the cache and create the orphan branch

**Files:**
- Create: `fr.cache.json` on new orphan branch `translation-cache` (staging)
- Modify: `scripts/TRANSLATION.md`

**Interfaces:**
- Consumes: the full pipeline from Tasks 1-7.
- Produces: a populated cache on `staging/translation-cache`, so the first CI build makes zero network calls.

- [ ] **Step 1: Install the runtime dependencies locally**

```bash
python3 -m venv .venv-translate
./.venv-translate/bin/pip install deep-translator pyyaml
```

Note: `myst` is NOT required. The cache is populated by the translation pass alone.

- [ ] **Step 2: Run the translation pass with patient retries**

Expect roughly 200 strings and 10-20 minutes; the free endpoint succeeds about one call in three.

```bash
./.venv-translate/bin/python scripts/translate_sources.py --cache ./fr.cache.json --attempts 30
```

Expected: exit 0 and `Cached N new translations`. If it exits 1, re-run — cached entries persist, so each run only retries what is still missing.

- [ ] **Step 3: Review the bootstrapped translations**

```bash
python3 -c "import json;d=json.load(open('fr.cache.json'));print(len(d));[print(repr(k),'->',repr(v)) for k,v in sorted(d.items())[:40]]"
```

Check the sidebar-visible strings specifically: all five `Lab N — ...` titles, all five lecture titles, `Labs`, and `Lectures`.

- [ ] **Step 4: Pin any preferred terms**

If `Lectures` resolved to `Conférences`, pin the course-appropriate wording:

```bash
cat > translations/fr.overrides.json <<'JSON'
{
  "Lectures": "Cours"
}
JSON
```

- [ ] **Step 5: Ignore the local-only bootstrap artifacts**

```bash
printf '\n.venv-translate/\n.tcache/\nfr.cache.json\n' >> .gitignore
git add .gitignore && git commit -m "Ignore local translation bootstrap artifacts"
```

- [ ] **Step 6: Create the orphan branch on staging from a temp directory**

Build the branch in a throwaway repo rather than with `git checkout --orphan`
in the working tree. `git checkout --orphan` would require a `git clean -fdx`
to empty the tree, which deletes ignored directories such as `_build/` — do
not do that here.

```bash
tmp=$(mktemp -d)
cp fr.cache.json "$tmp/"
git -C "$tmp" init -q -b translation-cache
git -C "$tmp" add fr.cache.json
git -C "$tmp" -c user.name="Mathieu Boudreau" -c user.email="emb6150@gmail.com" \
    commit -q -m "Bootstrap French translation cache"
git -C "$tmp" push https://github.com/mathieuboudreau/myst_book-staging.git \
    translation-cache
rm -rf "$tmp"
```

The working tree is never touched, and `mb/tradfix` stays checked out throughout.

- [ ] **Step 7: Confirm the branch exists on staging and nowhere else**

```bash
git ls-remote --heads staging translation-cache
git ls-remote --heads origin translation-cache   # must print nothing
```

- [ ] **Step 8: Document the new workflow in `scripts/TRANSLATION.md`**

Delete the `- **Translation corrections**: ...` bullet from the Customization
section and append this section to the end of the file:

```markdown
## Translation cache and preferred terms

Every English string resolves in this order:

1. `translations/fr.overrides.json` — hand-picked wording, versioned with content
2. `fr.cache.json` on the `translation-cache` branch — machine translations
3. Google Translate, retried up to 8 times with backoff

Anything that fails all three fails the build. The site is never deployed
half-English.

### The cache is bot-owned

The machine cache lives on the orphan `translation-cache` branch, not on
`main`. CI reads it, fills in anything new, and commits it back with
`[skip ci]`. Keeping it off `main` means parallel content branches never
produce merge conflicts in a large generated JSON file.

Do not hand-edit `fr.cache.json` — CI owns it. Use the overrides file instead.

### Pinning a preferred term

Machine translation is literal. To force a wording, add it to
`translations/fr.overrides.json`:

```json
{
  "Lectures": "Cours"
}
```

Overrides win over the cache and are never overwritten. The key is the
English source string; if it contains inline code, links, or MyST roles,
those appear as `XPHX0XPHX` placeholders — copy the key exactly as it is
reported in a build failure.

### Contributors do not need to run anything

Editing English content requires no local translation step. CI translates
what changed and updates the cache itself.

If you do want to fill the cache locally — for example to review the initial
translations — `mystmd` is not required, only the translation pass:

    python3 -m venv .venv-translate
    ./.venv-translate/bin/pip install deep-translator pyyaml
    ./.venv-translate/bin/python scripts/translate_sources.py \
        --cache ./fr.cache.json --attempts 30

Cached entries persist between runs, so re-running only retries what is
still missing.
```

- [ ] **Step 9: Commit the docs and overrides**

```bash
git add scripts/TRANSLATION.md translations/fr.overrides.json
git commit -m "Document cache, overrides, and fail-loud translation workflow"
git push staging mb/tradfix
```

---

### Task 9: Verify on staging

**Files:** none modified. This task is verification only.

**Interfaces:**
- Consumes: everything above.
- Produces: evidence that `/fr/` is fully French and that the miss and failure paths behave.

All commands target `mathieuboudreau/myst_book-staging`. Nothing touches `origin`.

- [ ] **Step 1: Set the staging BASE_URL variable**

```bash
gh variable set BASE_URL --body "/myst_book-staging" -R mathieuboudreau/myst_book-staging
```

- [ ] **Step 2: Dispatch the deploy for `mb/tradfix`**

`mb/tradfix` inherits `main`'s trigger (`push: main` + `workflow_dispatch`), so a push does not deploy — it must be dispatched.

```bash
gh workflow run "MyST GitHub Pages Deploy" -R mathieuboudreau/myst_book-staging --ref mb/tradfix
gh run watch -R mathieuboudreau/myst_book-staging
```

Expected: the job succeeds, and the log shows zero or very few new translations because the cache is complete.

- [ ] **Step 3: Assert every sidebar string is French**

```bash
curl -sL https://mathieuboudreau.github.io/myst_book-staging/fr/ \
  | grep -o '"title":"[^"]*"' | sort -u
```

Expected: no `Lab N — Subject`, no English lecture titles, `Lectures` rendered as the French wording, `Laboratoires` present.

- [ ] **Step 4: Assert the index body is French**

```bash
curl -sL https://mathieuboudreau.github.io/myst_book-staging/fr/ \
  | grep -o 'Modern research increasingly depends' || echo "OK: English intro absent"
```

Expected: `OK: English intro absent`

- [ ] **Step 5: Negative test — a cache miss is translated and written back**

```bash
printf '\nUne phrase de test pour la mise en cache.\n' >> index.md
git commit -am "Temp: cache miss test" && git push staging mb/tradfix
gh workflow run "MyST GitHub Pages Deploy" -R mathieuboudreau/myst_book-staging --ref mb/tradfix
gh run watch -R mathieuboudreau/myst_book-staging
git log --oneline -1 staging/translation-cache
```

Expected: the run succeeds, the log reports `Cached 1 new translations`, and `translation-cache` has a new `[skip ci]` commit.

- [ ] **Step 6: Failure test — an unresolvable string fails the build**

```bash
./.venv-translate/bin/python scripts/translate_sources.py --cache /tmp/empty.json --attempts 0; echo "exit=$?"
```

Expected: `exit=1` and a report listing untranslated strings. Confirms a half-English site cannot ship.

- [ ] **Step 7: Revert the temporary test content**

```bash
git revert --no-edit HEAD~0 2>/dev/null || git reset --hard HEAD~1
git push --force-with-lease staging mb/tradfix
```

- [ ] **Step 8: Report results**

Summarize for review: run URLs, the before/after sidebar strings, cache size, and any terms worth pinning in `fr.overrides.json`. Do not merge or push anything to `origin`.

---

## Out of scope for this branch

Spec section 12.2 (rollout to `origin`) is deliberately not a task here. This
session is staging-only. When the work does land on `origin`, the
`translation-cache` orphan branch must be created there and seeded with the
bootstrapped `fr.cache.json` **before** the first production deploy —
otherwise that build starts from an empty cache and must translate ~200
strings in a single run, which is exactly the throttling condition that
caused the original bug.

Recommended rollout order:

1. Push `translation-cache` (with its bootstrapped cache) to `origin`.
2. Confirm `vars.BASE_URL` is unset on `origin` so production keeps its
   current root-domain behavior.
3. Merge `mb/tradfix` to `main`.
