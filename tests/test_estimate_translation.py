import json
import os
import subprocess

import pytest

import estimate_translation as et


# --- summarising -----------------------------------------------------------

def test_summarise_counts_strings_characters_and_words():
    s = et.summarise(["Hello there", "Fork the repository"])
    assert s["strings"] == 2
    assert s["characters"] == len("Hello there") + len("Fork the repository")
    assert s["words"] == 5


def test_summarise_prices_at_twenty_dollars_per_million():
    s = et.summarise(["x" * 1_000_000])
    assert s["cost_usd"] == pytest.approx(20.0)


def test_summarise_of_nothing_is_zero_not_an_error():
    s = et.summarise([])
    assert s == {"strings": 0, "characters": 0, "words": 0, "cost_usd": 0.0}


# --- the month-to-date ledger ---------------------------------------------

def git(cwd, *args, **env):
    e = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@e",
             GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@e", **env)
    return subprocess.run(["git", *args], cwd=cwd, env=e,
                          capture_output=True, text=True, check=True)


def commit_cache(repo, mapping, date):
    with open(os.path.join(repo, "fr.cache.json"), "w", encoding="utf-8") as fh:
        json.dump(mapping, fh)
    git(repo, "add", "fr.cache.json")
    git(repo, "commit", "-m", "cache", "--date", date,
        GIT_COMMITTER_DATE=date)


@pytest.fixture
def cache_repo(tmp_path):
    repo = str(tmp_path / "tcache")
    os.makedirs(repo)
    git(repo, "init", "-q", "-b", "translation-cache")
    return repo


def test_month_to_date_counts_only_keys_added_this_month(cache_repo):
    commit_cache(cache_repo, {"old one": "fr"}, "2026-08-15T10:00:00+00:00")
    commit_cache(cache_repo, {"old one": "fr", "added now": "fr"},
                 "2026-09-10T10:00:00+00:00")
    mtd = et.month_to_date(cache_repo, now=et.datetime(2026, 9, 23, tzinfo=et.timezone.utc))
    assert mtd == len("added now")


def test_month_to_date_is_zero_when_nothing_was_added(cache_repo):
    commit_cache(cache_repo, {"old one": "fr"}, "2026-08-15T10:00:00+00:00")
    mtd = et.month_to_date(cache_repo, now=et.datetime(2026, 9, 23, tzinfo=et.timezone.utc))
    assert mtd == 0


def test_month_to_date_counts_everything_when_the_branch_starts_this_month(cache_repo):
    commit_cache(cache_repo, {"first": "fr"}, "2026-09-02T10:00:00+00:00")
    mtd = et.month_to_date(cache_repo, now=et.datetime(2026, 9, 23, tzinfo=et.timezone.utc))
    assert mtd == len("first")


def test_month_to_date_survives_a_missing_cache_repo(tmp_path):
    assert et.month_to_date(str(tmp_path / "nope")) == 0


# --- the verdict -----------------------------------------------------------

def test_under_budget_passes():
    v = et.verdict(pr_characters=5_000, month_to_date=10_000)
    assert v["status"] == "ok" and v["exit_code"] == 0


def test_eighty_percent_warns_but_does_not_block():
    v = et.verdict(pr_characters=1_000, month_to_date=405_000)
    assert v["status"] == "warn"
    assert v["exit_code"] == 0, "a warning must not block a merge"


def test_exceeding_the_budget_blocks():
    v = et.verdict(pr_characters=100_000, month_to_date=450_000)
    assert v["status"] == "over" and v["exit_code"] == 1


def test_the_boundary_itself_is_allowed():
    v = et.verdict(pr_characters=1, month_to_date=et.FREE_TIER_CHARACTERS - 1)
    assert v["status"] != "over" and v["exit_code"] == 0


# --- the comment -----------------------------------------------------------

def test_comment_carries_the_marker_so_it_can_be_updated_in_place():
    body = et.render(et.summarise(["hello"]), month_to_date=0)
    assert et.MARKER in body


def test_comment_reports_the_numbers():
    body = et.render(et.summarise(["Fork the repository"]), month_to_date=12_394)
    assert "19" in body            # characters in this PR
    assert "12,394" in body        # month to date
    assert "500,000" in body       # the budget


def test_comment_says_plainly_when_nothing_is_translated():
    body = et.render(et.summarise([]), month_to_date=0)
    assert "No new strings" in body


def test_comment_explains_why_it_blocks():
    body = et.render(et.summarise(["x" * 100_000]), month_to_date=450_000)
    assert "exceeds" in body.lower()


# --- integration against the real book -------------------------------------

def test_the_real_book_against_its_real_cache_needs_nothing(tmp_path):
    """The committed cache covers main, so an estimate on main is zero.

    This exercises the true pipeline -- TOC walk, shielding, overrides -- so
    the estimate cannot drift from what the deploy would actually send.
    """
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cache = subprocess.run(["git", "show", "origin/translation-cache:fr.cache.json"],
                           cwd=root, capture_output=True, text=True)
    if cache.returncode != 0:
        pytest.skip("translation-cache branch not fetched")
    pending = et.collect_pending(json.loads(cache.stdout), str(tmp_path / "out"))
    assert et.summarise(pending)["characters"] == 0


# --- what is actually chargeable ------------------------------------------

def test_nothing_is_chargeable_inside_the_free_allowance():
    assert et.chargeable_characters(pr_characters=6_227, month_to_date=15_272) == 0


def test_only_the_part_past_the_allowance_is_chargeable():
    """A PR straddling the threshold is charged for the overage alone."""
    assert et.chargeable_characters(
        pr_characters=10_000, month_to_date=495_000) == 5_000


def test_everything_is_chargeable_once_the_allowance_is_spent():
    assert et.chargeable_characters(
        pr_characters=10_000, month_to_date=600_000) == 10_000


def test_landing_exactly_on_the_allowance_is_still_free():
    assert et.chargeable_characters(
        pr_characters=1, month_to_date=et.FREE_TIER_CHARACTERS - 1) == 0


def test_comment_says_free_credit_rather_than_a_price_when_nothing_is_owed():
    body = et.render(et.summarise(["Fork the repository"]), month_to_date=15_272)
    assert "free credit" in body.lower()
    assert "$0.00" not in body, "quoting a price implies money changes hands"


def test_comment_quotes_a_price_only_for_the_chargeable_part():
    body = et.render(et.summarise(["x" * 10_000]), month_to_date=495_000)
    assert "$0.10" in body          # 5,000 chargeable characters at $20/M
    assert "5,000" in body
