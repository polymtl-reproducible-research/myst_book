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


def test_markup_only_strings_never_reach_the_translator():
    calls = []
    r = Resolver(lambda t: calls.append(t) or "should not happen")
    for probe in ["`git init`", "[](#lab2)", "{cite:p}`smith2020`"]:
        assert r.resolve(probe) == probe
    assert calls == []


def test_markup_only_strings_never_enter_the_cache():
    r = Resolver(lambda t: "FR:" + t)
    r.resolve("`git init`")
    r.resolve("{cite:p}`smith2020`")
    assert r.cache == {}


def test_prose_containing_markup_is_still_translated():
    r = Resolver(lambda t: "FR:" + t)
    out = r.resolve("See [the guide](https://e.com) now.")
    assert out == "FR:See [the guide](https://e.com) now."
    assert len(r.cache) == 1
