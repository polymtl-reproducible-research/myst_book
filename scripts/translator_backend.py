"""Cloud Translation API (v2) backend with retry and backoff.

This is the only module that knows about the network. It calls the official API
rather than scraping translate.google.com: Google gated the scraped endpoints in
September 2026, and every request to them now returns 429 behind a CAPTCHA.

Failures split in two. A permanent one -- a missing or rejected key, an API that
is not enabled -- cannot be fixed by trying again, so it is raised at once with
whatever Google said about it. Everything else (5xx, a genuine quota 429, a
dropped connection) is retried with exponential backoff.

The key is read from GOOGLE_TRANSLATE_API_KEY only when a string actually needs
translating, so a build whose cache already covers the site needs no secret.
"""

import html
import json
import os
import random
import time
import urllib.error
import urllib.parse
import urllib.request

ENDPOINT = "https://translation.googleapis.com/language/translate/v2"
API_KEY_ENV = "GOOGLE_TRANSLATE_API_KEY"
BASE_DELAY = 1.0
MAX_DELAY = 30.0
TIMEOUT = 30

# Statuses no amount of retrying will get past.
PERMANENT_STATUSES = (400, 401, 403, 404)


class PermanentTranslationError(RuntimeError):
    """A failure retrying cannot fix: bad key, disabled API, malformed request.

    `permanent` lets the resolver re-raise these without importing this module,
    so one bad key fails the build immediately instead of being reported as
    several hundred separately unresolved strings.
    """

    permanent = True


def _error_detail(error):
    """Pull Google's human-readable message out of an HTTPError body."""
    try:
        body = json.loads(error.read().decode("utf-8", "replace"))
    except Exception:
        return error.reason or "no detail"
    return body.get("error", {}).get("message") or error.reason or "no detail"


class CloudTranslator:
    """Translates one string per call through Cloud Translation v2."""

    def __init__(self, api_key, source="en", target="fr", opener=None):
        self.api_key = api_key
        self.source = source
        self.target = target
        self._open = opener or urllib.request.urlopen

    def translate(self, text):
        payload = urllib.parse.urlencode({
            "key": self.api_key,
            "q": text,
            "source": self.source,
            "target": self.target,
            "format": "text",
        }).encode("utf-8")
        request = urllib.request.Request(ENDPOINT, data=payload)
        try:
            with self._open(request, timeout=TIMEOUT) as response:
                body = json.load(response)
        except urllib.error.HTTPError as error:
            detail = _error_detail(error)
            if error.code in PERMANENT_STATUSES:
                raise PermanentTranslationError(
                    "Cloud Translation rejected the request (HTTP %d): %s"
                    % (error.code, detail))
            raise RuntimeError(
                "Cloud Translation HTTP %d: %s" % (error.code, detail))

        translations = body.get("data", {}).get("translations") or []
        if not translations:
            raise RuntimeError("Cloud Translation returned nothing for: " + text)
        # v2 HTML-escapes its output even with format=text, so entities such as
        # &#39; have to be unwound or they reach the page verbatim.
        return html.unescape(translations[0].get("translatedText", ""))


def _require_api_key():
    key = os.environ.get(API_KEY_ENV, "").strip()
    if not key:
        raise PermanentTranslationError(
            "%s is not set. Cloud Translation needs an API key to translate new "
            "strings; a build whose cache already covers every string needs none."
            % API_KEY_ENV)
    return key


def make_google_translator(attempts=8, sleep=time.sleep, translator=None):
    """Return a callable that translates English to French, retrying on failure.

    `translator` is the seam for tests. When it is None the real client is built
    on first use, so constructing this does not require a key.
    """
    backend = translator

    def resolve_backend():
        nonlocal backend
        if backend is None:
            backend = CloudTranslator(_require_api_key())
        return backend

    def translate(text):
        delay = BASE_DELAY
        last_error = None
        for attempt in range(attempts):
            try:
                result = resolve_backend().translate(text)
                if result:
                    return result
                last_error = ValueError("empty translation for: " + text)
            except PermanentTranslationError:
                raise
            except Exception as error:
                last_error = error
            if attempt < attempts - 1:
                capped = min(delay, MAX_DELAY)
                sleep(capped * (0.5 + random.random()) / 1.5)
                delay *= 2
        raise last_error or RuntimeError(
            "translation failed after %d attempt(s): %s" % (attempts, text))

    return translate
