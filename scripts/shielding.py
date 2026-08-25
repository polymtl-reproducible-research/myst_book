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
    r"\([^)]*\)",                               # link targets: (url) and (#ref)
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
