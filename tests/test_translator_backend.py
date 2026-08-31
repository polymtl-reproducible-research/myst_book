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


def test_modules_import_without_deep_translator_installed():
    """The CI test job installs only pytest and pyyaml, so the deep_translator
    import must stay lazy. A module-level import would break the whole job."""
    import os
    import subprocess
    import sys
    scripts = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts")
    code = (
        "import sys; sys.modules['deep_translator'] = None;"
        "sys.path.insert(0, %r);"
        "import translator_backend, translate_sources;"
        "print('ok')" % scripts
    )
    result = subprocess.run([sys.executable, "-c", code],
                            capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert "ok" in result.stdout
