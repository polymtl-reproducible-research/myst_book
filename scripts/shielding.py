"""Protect non-translatable inline markup from the translator.

Spans that must survive translation byte-for-byte (MyST roles, inline math,
inline code, link targets) are replaced with XPHX<n>XPHX placeholders before
the text is sent out, and substituted back afterwards.
"""

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
    """Substitute placeholders back into text.

    Raises KeyError if the text references a placeholder that does not exist.
    Iterates to a fixed point to handle nested placeholders.
    """

    def _sub(match):
        index = int(match.group(1))
        if index >= len(placeholders):
            raise KeyError(match.group(0))
        return placeholders[index]

    for _ in range(len(placeholders) + 1):
        expanded = _PH_RE.sub(_sub, text)
        if expanded == text:
            return expanded
        text = expanded
    return text


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
