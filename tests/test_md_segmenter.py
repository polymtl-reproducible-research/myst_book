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


def test_iframe_translates_caption_but_not_options():
    body = ":::{iframe} https://example.com/embed\n:width: 100%\nA caption here.\n:::"
    out = translate_body(body, UP).split("\n")
    assert out[0] == ":::{iframe} https://example.com/embed"
    assert out[1] == ":width: 100%"
    assert out[2] == "A CAPTION HERE."


def test_body_with_no_prose_is_unchanged():
    body = "```\ncode\n```\n\n$$\nx\n$$"
    assert translate_body(body, UP) == body


def test_thematic_break_is_preserved_and_not_joined_into_prose():
    body = "This rule is 80 chars long:\n" + "-" * 80
    out = translate_body(body, UP).split("\n")
    assert out[0] == "THIS RULE IS 80 CHARS LONG:"
    assert out[1] == "-" * 80


def test_hard_line_break_is_preserved():
    body = "**Deadline:** *TBD*  \n**Teams:** two students."
    out = translate_body(body, UP).split("\n")
    assert len(out) == 2
    assert out[0].endswith("  ")


def test_admonition_option_line_is_preserved_verbatim():
    body = ":::{note}\n:class: dropdown\nSome prose here.\n:::"
    out = translate_body(body, UP).split("\n")
    assert out[1] == ":class: dropdown"
    assert out[2] == "SOME PROSE HERE."


def test_admonition_options_precede_translated_title_and_body():
    body = ":::{admonition} Key takeaway\n:class: important\nThis matters.\nAnd more.\n:::"
    out = translate_body(body, UP).split("\n")
    assert out[0] == ":::{admonition} KEY TAKEAWAY"
    assert out[1] == ":class: important"
    assert out[2] == "THIS MATTERS. AND MORE."


def test_admonition_without_options_is_unchanged():
    body = ":::{note}\nNo options here.\n:::"
    out = translate_body(body, UP).split("\n")
    assert out[1] == "NO OPTIONS HERE."


def test_labeled_math_block_closes():
    body = "$$\nE = mc^2\n$$ (eq-energy)\n\nProse after the equation."
    out = translate_body(body, UP).split("\n")
    assert out[:3] == ["$$", "E = mc^2", "$$ (eq-energy)"]
    assert out[-1] == "PROSE AFTER THE EQUATION."


def test_single_line_math_still_works():
    assert translate_body("$$ x = 1 $$", UP) == "$$ x = 1 $$"


def test_fenced_directive_reaches_the_directive_renderer():
    body = "```{figure} img/x.png\n:alt: A picture\nA caption here.\n```"
    out = translate_body(body, UP).split("\n")
    assert out[0] == "```{figure} img/x.png"
    assert out[1] == ":alt: A picture"
    assert out[2] == "A CAPTION HERE."


def test_plain_code_fence_is_still_verbatim():
    body = "```python\nx = 1  # keep\n```"
    assert translate_body(body, UP) == body


def test_wrapped_list_item_is_translated_as_one_unit():
    body = "- Findable — data are assigned an identifier and\n  are described richly enough."
    sent = []
    translate_body(body, lambda t: sent.append(t) or "<T>")
    assert sent == ["Findable — data are assigned an identifier and are described richly enough."]


def test_list_item_hard_break_is_preserved():
    body = "- Dissemination with Borealis  \n- Collaboration workflow"
    out = translate_body(body, UP).split("\n")
    assert out[0].endswith("  ")
    assert out[1] == "- COLLABORATION WORKFLOW"


def test_nested_sublist_is_not_absorbed_into_its_parent():
    assert translate_body("- top\n  - nested", UP) == "- TOP\n  - NESTED"


def test_indented_line_after_a_paragraph_is_not_absorbed_into_a_list():
    body = "- an item\n\nSome paragraph\n  continued here."
    out = translate_body(body, UP).split("\n")
    assert out[0] == "- AN ITEM"
    assert "SOME PARAGRAPH CONTINUED HERE." in out
