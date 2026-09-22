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


def test_zero_attempts_raises_a_real_exception():
    backend = Flaky(failures=0)
    translate = make_google_translator(attempts=0, translator=backend, sleep=lambda s: None)
    with pytest.raises(RuntimeError, match="0 attempt"):
        translate("Labs")
    assert backend.calls == 0


def test_modules_import_with_no_third_party_packages():
    """The CI test job installs only pytest and pyyaml, so the translation
    scripts must import using nothing but the standard library."""
    import os
    import subprocess
    import sys
    scripts = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts")
    code = (
        "import sys; sys.modules['deep_translator'] = None;"
        "sys.modules['requests'] = None;"
        "sys.path.insert(0, %r);"
        "import translator_backend, translate_sources;"
        "print('ok')" % scripts
    )
    result = subprocess.run([sys.executable, "-c", code],
                            capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert "ok" in result.stdout


# --- Cloud Translation API v2 backend -------------------------------------

import io
import json
import urllib.error

from translator_backend import (
    API_KEY_ENV,
    CloudTranslator,
    PermanentTranslationError,
)


class FakeResponse:
    def __init__(self, payload):
        self._body = json.dumps(payload).encode("utf-8")

    def read(self):
        return self._body

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def http_error(code, message="boom"):
    body = json.dumps({"error": {"code": code, "message": message}}).encode("utf-8")
    return urllib.error.HTTPError(
        "https://example", code, message, {}, io.BytesIO(body))


def opener_returning(*outcomes):
    """Each call yields the next outcome; exceptions are raised, others returned."""
    remaining = list(outcomes)
    calls = []

    def opener(request, timeout=None):
        calls.append(request)
        outcome = remaining.pop(0)
        if isinstance(outcome, Exception):
            raise outcome
        return FakeResponse(outcome)

    opener.calls = calls
    return opener


def translation_payload(text):
    return {"data": {"translations": [{"translatedText": text}]}}


def test_translates_through_the_cloud_api():
    opener = opener_returning(translation_payload("Création de compte"))
    client = CloudTranslator("KEY", opener=opener)
    assert client.translate("Account creation") == "Création de compte"
    assert len(opener.calls) == 1


def test_request_carries_key_and_language_pair():
    opener = opener_returning(translation_payload("Laboratoires"))
    CloudTranslator("SEKRIT", opener=opener).translate("Labs")
    body = opener.calls[0].data.decode("utf-8")
    assert "key=SEKRIT" in body
    assert "source=en" in body and "target=fr" in body
    assert "format=text" in body


def test_unescapes_html_entities_in_the_response():
    """v2 escapes its output even with format=text; &#39; must not reach the page."""
    opener = opener_returning(translation_payload("l&#39;environnement &amp; R&#39;D"))
    client = CloudTranslator("KEY", opener=opener)
    assert client.translate("the environment") == "l'environnement & R'D"


def test_permanent_http_error_is_not_retried():
    opener = opener_returning(http_error(403, "API key not valid"))
    translate = make_google_translator(
        attempts=8, translator=CloudTranslator("KEY", opener=opener),
        sleep=lambda s: None)
    with pytest.raises(PermanentTranslationError, match="API key not valid"):
        translate("Labs")
    assert len(opener.calls) == 1, "a rejected key must not be retried 8 times"


def test_transient_http_error_is_retried():
    opener = opener_returning(http_error(503, "backend error"),
                              translation_payload("Laboratoires"))
    translate = make_google_translator(
        translator=CloudTranslator("KEY", opener=opener), sleep=lambda s: None)
    assert translate("Labs") == "Laboratoires"
    assert len(opener.calls) == 2


def test_quota_429_is_retried_not_fatal():
    opener = opener_returning(http_error(429, "Quota exceeded"),
                              translation_payload("Laboratoires"))
    translate = make_google_translator(
        translator=CloudTranslator("KEY", opener=opener), sleep=lambda s: None)
    assert translate("Labs") == "Laboratoires"


def test_empty_translation_list_is_an_error():
    opener = opener_returning({"data": {"translations": []}})
    with pytest.raises(RuntimeError):
        CloudTranslator("KEY", opener=opener).translate("Labs")


def test_missing_api_key_is_permanent(monkeypatch):
    monkeypatch.delenv(API_KEY_ENV, raising=False)
    translate = make_google_translator(attempts=4, sleep=lambda s: None)
    with pytest.raises(PermanentTranslationError, match=API_KEY_ENV):
        translate("Labs")


def test_no_api_key_needed_until_a_string_is_translated(monkeypatch):
    """A build whose cache covers every string must not require the secret."""
    monkeypatch.delenv(API_KEY_ENV, raising=False)
    make_google_translator()          # must not raise


def test_permanent_errors_are_marked_for_the_resolver():
    assert PermanentTranslationError("x").permanent is True
