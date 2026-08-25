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
FENCE_DIRECTIVE_RE = re.compile(r"^(`{3,}|~{3,})\{(.+?)\}")
DIRECTIVE_RE = re.compile(r"^(:{3,})\{(.+?)\}")
TABLE_RE = re.compile(r"^\s*\|")
TABLE_SEP_RE = re.compile(r"^\s*\|[\s\-:|]+\|\s*$")
HEADING_RE = re.compile(r"^(#{1,6}\s+)(.*)$")
LIST_RE = re.compile(r"^(\s*(?:[-*+]|\d+\.)\s+)(.*)$")
HAS_WORDS_RE = re.compile(r"[a-zA-Z]{2,}")
RULE_RE = re.compile(r"^\s*([-*_])\1{2,}\s*$")
HARD_BREAK_RE = re.compile(r"\S {2,}$")
DIRECTIVE_OPTION_RE = re.compile(r"^:[a-zA-Z_][a-zA-Z0-9_-]*:")


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

        fenced_directive = FENCE_DIRECTIVE_RE.match(line)
        if fenced_directive:
            flush()
            char = fenced_directive.group(1)[0]
            close = re.compile(r"^" + re.escape(char)
                               + r"{" + str(len(fenced_directive.group(1))) + r",}\s*$")
            buf = [line]
            i += 1
            while i < len(lines) and not close.match(lines[i]):
                buf.append(lines[i])
                i += 1
            closed = i < len(lines)
            if closed:
                buf.append(lines[i])
                i += 1
            blocks.append(Block("directive", buf,
                                {"name": fenced_directive.group(2), "closed": closed}))
            continue

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
            single = line.strip() != "$$" and line.strip().endswith("$$")
            if not single:
                while i < len(lines):
                    buf.append(lines[i])
                    # A closing fence may carry a MyST label: `$$ (eq-name)`.
                    closes = lines[i].strip().startswith("$$")
                    i += 1
                    if closes:
                        break
            blocks.append(Block("math", buf))
            continue

        if not line.strip():
            flush()
            blocks.append(Block("blank", [line]))
            i += 1
            continue

        if RULE_RE.match(line):
            flush()
            blocks.append(Block("rule", [line]))
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

        if (blocks and blocks[-1].kind == "list_item" and not para
                and line[:1].isspace() and line.strip()):
            blocks[-1].lines.append(line)
            i += 1
            continue

        para.append(line)
        i += 1
        if HARD_BREAK_RE.search(line):
            flush()

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
    if block.kind in ("fence", "math", "blank", "rule"):
        return list(block.lines)
    if block.kind == "heading":
        return [_render_prefixed(block.lines[0], HEADING_RE, translate)]
    if block.kind == "list_item":
        prefix, first = LIST_RE.match(block.lines[0]).groups()
        text = " ".join([first.strip()] + [l.strip() for l in block.lines[1:]]).strip()
        if not HAS_WORDS_RE.search(text):
            return list(block.lines)
        trailing = "  " if HARD_BREAK_RE.search(block.lines[-1]) else ""
        return [prefix + translate(text) + trailing]
    if block.kind == "paragraph":
        text = " ".join(line.strip() for line in block.lines)
        trailing = "  " if HARD_BREAK_RE.search(block.lines[-1]) else ""
        return [translate(text) + trailing]
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
        # Directive options sit at the very start of the body and are not prose.
        options, rest = [], list(inner)
        while rest and DIRECTIVE_OPTION_RE.match(rest[0]):
            options.append(rest.pop(0))
        body = render(segment("\n".join(rest)), translate).split("\n") if rest else []
        return [first] + options + body + closing

    return list(block.lines)


def _split_directive(block):
    """Return (opening_line, inner_lines, closing_lines)."""
    if block.meta.get("closed") and len(block.lines) >= 2:
        return block.lines[0], block.lines[1:-1], [block.lines[-1]]
    return block.lines[0], block.lines[1:], []
