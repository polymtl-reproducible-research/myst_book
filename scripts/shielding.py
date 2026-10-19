"""Protect non-translatable inline markup from the translator.

Spans that must survive translation byte-for-byte (MyST roles, inline math,
inline code, link targets) are replaced with XPHX<n>XPHX placeholders before
the text is sent out, and substituted back afterwards.
"""

import html
import re

PLACEHOLDER = "XPHX{}XPHX"
_PH_RE = re.compile(r"XPHX(\d+)XPHX")

# Applied in order. Inline code before math to prevent math pattern from consuming
# $ delimiters inside backticks. Link targets last so code/math inside link text
# are shielded first.
_PATTERNS = (
    r"\{[a-zA-Z:_-]+\}`[^`]*`",                 # MyST roles: {cite:p}`key`
    r"`[^`]+`",                                 # inline code: `code`
    r"(?<!\$)\$(?!\$)(?!\d)[^$\n]+\$(?!\$)",    # inline math: $x$ (not $5 currency)
    r"(?<=\])\([^)]*\)",                        # link targets: ](url) and ](#ref)
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
    """Substitute placeholders back into text in descending index order.

    Processes indices from high to low, ensuring each placeholder is expanded
    exactly once. A shielded span can only contain LOWER-numbered placeholders
    (since patterns are applied sequentially), so descending order prevents
    re-expansion of restored content.

    Raises KeyError if the text references a placeholder that does not exist.
    """
    for index in range(len(placeholders) - 1, -1, -1):
        text = text.replace(PLACEHOLDER.format(index), placeholders[index])
    leftover = _PH_RE.search(text)
    if leftover and int(leftover.group(1)) >= len(placeholders):
        raise KeyError(leftover.group(0))
    return text


def strip_placeholders(text):
    """Remove every placeholder token, leaving only the surrounding literal text."""
    return _PH_RE.sub("", text)


def repair_placeholder_spacing(text):
    """Undo the translator's habit of inserting space between `]` and a placeholder.

    Google reliably renders `[text]XPHX0XPHX` as `[text] XPHX0XPHX`. Left alone that
    is a broken markdown link, and validate() rightly rejects it -- but the artifact is
    deterministic, so repairing it is better than failing a string that is otherwise a
    perfectly good translation.
    """
    return re.sub(r"\]\s+(XPHX\d+XPHX)", r"]\1", text)


def to_html(protected):
    """Render shielded text as HTML for a translator called with format=html.

    In plain text, Google treats placeholders and `**` as noise and drops them
    from long, markup-heavy sentences. Tags are preserved, so links, bold and
    italics become tags and every other placeholder is marked translate="no".
    Cache and override keys stay in placeholder form; only the request changes.
    """
    text = html.escape(protected, quote=False)
    # Empty-text links ([](#label)) have nothing to translate; keep them whole.
    text = re.sub(r"\[\]XPHX(\d+)XPHX", r'<span translate="no">[]XPHX\1XPHX</span>', text)
    text = re.sub(r"\[([^\[\]]+)\]XPHX(\d+)XPHX", r'<a id="\2">\1</a>', text)
    # A sentence-ending period rides inside the span: Google drops a period that
    # follows one ("en pratique XPHX0XPHX Les articles").
    text = re.sub(r"(?<!\])XPHX(\d+)XPHX(\.(?=\s|$))?",
                  r'<span translate="no">XPHX\1XPHX\2</span>', text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<![*\w])\*(?=\S)([^*]+?)(?<=\S)\*(?![*\w])", r"<i>\1</i>", text)
    return text


def from_html(translated):
    """Turn a format=html translation back into shielded markdown.

    Google spaces tags as if they were words: it writes `l' <b>`, `</a> ,` and
    `<b>, texte</b>`. Those spaces and leading punctuation are moved back out
    of the markup, since `** gras**` is not bold in markdown and `[arXiv] )`
    reads as a typo.
    """
    text = re.sub(r"([’'])\s+(?=<(?:a|b|i|span)\b)", r"\1", translated)
    text = re.sub(r"(</(?:a|b|i|span)>)\s+(?=[,.)])", r"\1", text)
    text = re.sub(r'<span translate="no">(.*?)</span>', r"\1", text)
    text = _unwrap(text, "<b>", "</b>", lambda m: "**%s**" % m.group("inner"))
    text = _unwrap(text, "<i>", "</i>", lambda m: "*%s*" % m.group("inner"))
    text = _unwrap(text, r'<a id="(?P<id>\d+)">', "</a>",
                   lambda m: "[%s]XPHX%sXPHX" % (m.group("inner"), m.group("id")))
    return html.unescape(text)


_TAG_RE = r"(?P<before>\s*){}(?P<punct>[,;:]?)(?P<lead>\s*)(?P<inner>.*?)(?P<trail>\s*){}"


def _unwrap(text, open_tag, close_tag, render):
    """Replace one tag pair with markdown, keeping spaces and punctuation outside it."""
    def _sub(match):
        gap = " " if match.group("before") or match.group("lead") or match.group("punct") else ""
        return match.group("punct") + gap + render(match) + match.group("trail")
    return re.sub(_TAG_RE.format(open_tag, close_tag), _sub, text)


def validate(source_protected, translated_protected):
    """True if the translation preserved every structural marker.

    Checks placeholder identity, bracket balance (which is how link damage
    shows up once targets are shielded), bold-marker parity, and adjacency
    of link-target placeholders to their brackets.
    """
    if _placeholder_ids(source_protected) != _placeholder_ids(translated_protected):
        return False
    for marker in ("[", "]", "**"):
        if source_protected.count(marker) != translated_protected.count(marker):
            return False
    if _bracketed_ids(source_protected) != _bracketed_ids(translated_protected):
        return False
    return True


def _placeholder_ids(text):
    return sorted(int(n) for n in _PH_RE.findall(text))


def _bracketed_ids(text):
    """Placeholder ids that sit immediately after a closing bracket (link targets)."""
    return sorted(int(n) for n in re.findall(r"(?<=\])XPHX(\d+)XPHX", text))
