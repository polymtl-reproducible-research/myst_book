"""Google Translate backend with retry and backoff.

The free endpoint raises TranslationNotFound nondeterministically at roughly a
2-in-3 rate regardless of content, so a single attempt is not meaningful. This
is the only module that knows about the network.
"""

import random
import time

BASE_DELAY = 1.0
MAX_DELAY = 30.0


def make_google_translator(attempts=8, sleep=time.sleep, translator=None):
    """Return a callable that translates English to French, retrying on failure."""
    if translator is None:
        from deep_translator import GoogleTranslator

        translator = GoogleTranslator(source="en", target="fr")

    def translate(text):
        delay = BASE_DELAY
        last_error = None
        for attempt in range(attempts):
            try:
                result = translator.translate(text)
                if result:
                    return result
                last_error = ValueError("empty translation for: " + text)
            except Exception as error:
                last_error = error
            if attempt < attempts - 1:
                capped = min(delay, MAX_DELAY)
                sleep(capped * (0.5 + random.random()) / 1.5)
                delay *= 2
        raise last_error or RuntimeError(
            "translation failed after %d attempt(s): %s" % (attempts, text))

    return translate
