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
    assert ph == ["(https://mystmd.org/guide)"]


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
    dst = "Voir [le guide]XPHX1XPHX et XPHX0XPHX."
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


def test_does_not_shield_ordinary_prose_parentheses():
    protected, ph = shield("Research outputs (data and code) must be shared.")
    assert protected == "Research outputs (data and code) must be shared."
    assert ph == []


def test_round_trip_exact_for_code_span_containing_dollars():
    original = "Run `echo $HOME $PATH` now."
    protected, ph = shield(original)
    assert restore(protected, ph) == original
    assert "XPHX" not in restore(protected, ph)


def test_currency_amounts_are_not_treated_as_math():
    protected, ph = shield("This costs $5 and that costs $10 today.")
    assert protected == "This costs $5 and that costs $10 today."
    assert ph == []


def test_inline_math_is_still_shielded():
    protected, ph = shield("Solve $x > 0$ here.")
    assert protected == "Solve XPHX0XPHX here."


def test_validate_rejects_placeholder_detached_from_its_bracket():
    src, _ = shield("See [the guide](https://e.com).")
    # Same bracket and placeholder counts; only the adjacency differs.
    assert validate(src, "Voir [le guide] XPHX0XPHX.") is False


def test_round_trip_survives_literal_placeholder_shaped_content():
    original = "Code `XPHX0XPHX` and [l](#r)."
    protected, ph = shield(original)
    assert restore(protected, ph) == original
