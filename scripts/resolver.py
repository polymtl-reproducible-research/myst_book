"""Resolve English strings to French: overrides, then cache, then translation.

The resolver never raises on a translation failure. It records the offending
string in `unresolved` and returns the English original, so the caller can
report every failure at once and exit non-zero.
"""

import json
import os
import re

from shielding import restore, shield, strip_placeholders, validate

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

        # A string whose only content is shielded markup has nothing to translate.
        # Guarding AFTER shielding keeps bare-placeholder strings off the network and,
        # critically, out of the cache -- they would all collide on the same key.
        if not HAS_WORDS_RE.search(strip_placeholders(protected)):
            return text

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
