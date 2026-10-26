"""Estimate what a pull request will send to Cloud Translation.

Runs the real pipeline with the network backend swapped for a recorder, so the
figure is not a guess: it is the identical TOC walk, shielding and override
lookup the deploy will perform, diffed against the committed cache. The only
way it can drift is if translation-cache moves between the estimate and the
merge.

Needs no API key and makes no network calls, so it is safe on any pull request.

Month-to-date spend is read from the cache branch's own history. The cache is
append-only, so keys present now but absent at the last commit before the month
began are exactly what was bought this month -- no credentials, no billing API.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import translate_sources as ts          # noqa: E402
from resolver import load_json, save_json  # noqa: E402

PRICE_PER_MILLION_USD = 20.0
FREE_TIER_CHARACTERS = 500_000
WARN_FRACTION = 0.8
MARKER = "<!-- translation-estimate -->"


# --- what this PR would send ----------------------------------------------

def collect_pending(cache, work_dir):
    """Return the strings the deploy would send, via the real pipeline."""
    os.makedirs(work_dir, exist_ok=True)
    cache_path = os.path.join(work_dir, "cache.json")
    save_json(cache_path, cache)

    sent = []

    def recorder(attempts=8, **kwargs):
        def translate(text):
            sent.append(text)
            return text      # echoing back satisfies structural validation
        return translate

    real_backend = ts.make_google_translator
    real_dir = ts.TRANSLATED_DIR
    ts.make_google_translator = recorder
    ts.TRANSLATED_DIR = os.path.join(work_dir, "_translated")
    try:
        ts.main(["--cache", cache_path])
    finally:
        ts.make_google_translator = real_backend
        ts.TRANSLATED_DIR = real_dir
    return sent


def summarise(strings):
    characters = sum(len(s) for s in strings)
    return {
        "strings": len(strings),
        "characters": characters,
        "words": sum(len(s.split()) for s in strings),
        "cost_usd": characters / 1_000_000 * PRICE_PER_MILLION_USD,
    }


# --- what has already been spent this month -------------------------------

def _month_start(now=None):
    now = now or datetime.now(timezone.utc)
    return now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)


def _git(cwd, *args):
    result = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else ""


def _cache_at(repo, rev, path):
    raw = _git(repo, "show", "%s:%s" % (rev, path))
    try:
        return json.loads(raw) if raw else {}
    except ValueError:
        return {}


def month_to_date(cache_repo, cache_file="fr.cache.json", ref="HEAD", now=None):
    """Characters added to the cache since the month began."""
    if not os.path.isdir(cache_repo):
        return 0
    since = _month_start(now).isoformat()
    base_rev = _git(cache_repo, "rev-list", "-1", "--before=" + since, ref)
    current = _cache_at(cache_repo, ref, cache_file)
    base = _cache_at(cache_repo, base_rev, cache_file) if base_rev else {}
    return sum(len(key) for key in set(current) - set(base))


# --- the verdict -----------------------------------------------------------

def chargeable_characters(pr_characters, month_to_date, budget=FREE_TIER_CHARACTERS):
    """Characters of this PR that fall beyond the month's free allowance.

    The allowance arrives as a $10 monthly credit, so nothing is owed until it
    is spent. A pull request straddling the threshold is charged for the
    overage alone, not for all of itself.
    """
    overage = (pr_characters + month_to_date) - budget
    return max(0, min(pr_characters, overage))


def verdict(pr_characters, month_to_date, budget=FREE_TIER_CHARACTERS):
    projected = pr_characters + month_to_date
    if projected > budget:
        status = "over"
    elif projected >= budget * WARN_FRACTION:
        status = "warn"
    else:
        status = "ok"
    return {
        "status": status,
        "projected": projected,
        "budget": budget,
        "exit_code": 1 if status == "over" else 0,
    }


def _cost_phrase(pr_characters, month_to_date, budget):
    chargeable = chargeable_characters(pr_characters, month_to_date, budget)
    if chargeable == 0:
        return "none - covered by the monthly free credit"
    return "$%.2f USD for the %s characters past the free credit" % (
        chargeable / 1_000_000 * PRICE_PER_MILLION_USD, f"{chargeable:,}")


def render(estimate, month_to_date, budget=FREE_TIER_CHARACTERS):
    v = verdict(estimate["characters"], month_to_date, budget)
    percent = v["projected"] / budget * 100 if budget else 0.0

    lines = [MARKER, "### Translation estimate", ""]
    if estimate["characters"] == 0:
        lines += ["No new strings. Everything this branch renders is already in "
                  "the translation cache, so the deploy will make no API calls.", ""]
    else:
        lines += [
            "| | |",
            "|---|---|",
            "| This PR | %s strings · **%s characters** · %s words |"
            % (f"{estimate['strings']:,}", f"{estimate['characters']:,}",
               f"{estimate['words']:,}"),
            "| Cost | %s |" % _cost_phrase(estimate["characters"], month_to_date, budget),
            "",
        ]

    lines += [
        "Month to date: **%s** characters. Projected total **%s / %s** (%.1f%% of the free tier)."
        % (f"{month_to_date:,}", f"{v['projected']:,}", f"{budget:,}", percent),
        "",
    ]

    if v["status"] == "over":
        lines.append(
            "> **Blocked.** This PR exceeds the monthly free allowance. Check the "
            "diff for an accidental text dump before overriding; if it is genuinely "
            "this large, an admin can merge past this check."
        )
    elif v["status"] == "warn":
        lines.append(
            "> **Heads up.** This would put the month above %d%% of the free "
            "allowance. Not blocking." % int(WARN_FRACTION * 100)
        )

    lines += ["", "<sub>Estimated by running the real translation pipeline with the "
              "network stubbed out. No API calls were made.</sub>"]
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", required=True, help="path to fr.cache.json")
    parser.add_argument("--cache-repo", help="checkout of the translation-cache branch")
    parser.add_argument("--comment", help="write the rendered comment here")
    parser.add_argument("--budget", type=int, default=FREE_TIER_CHARACTERS)
    args = parser.parse_args(argv)

    work_dir = tempfile.mkdtemp(prefix="translation-estimate-")
    try:
        pending = collect_pending(load_json(args.cache), work_dir)
    finally:
        shutil.rmtree(work_dir, ignore_errors=True)

    estimate = summarise(pending)
    spent = month_to_date(args.cache_repo) if args.cache_repo else 0
    body = render(estimate, spent, args.budget)

    if args.comment:
        with open(args.comment, "w", encoding="utf-8") as handle:
            handle.write(body + "\n")
    print(body)

    return verdict(estimate["characters"], spent, args.budget)["exit_code"]


if __name__ == "__main__":
    sys.exit(main())
