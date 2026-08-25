# French translation reliability — design

Date: 2026-08-25
Branch: `mb/tradfix`
Status: awaiting review

## 1. Problem

The deployed French site at `/fr/` ships a mix of French and English. Reported
symptom: the sidebar shows `Lab 1`, `Lab 2`, `Lab 3` but `Laboratoire 4`.

Reading the live page's embedded Remix state shows the problem is much wider
than the sidebar:

| Element | Live value |
| --- | --- |
| TOC section 1 | `Lectures` (English) |
| TOC section 2 | `Laboratoires` (French) |
| lab1, lab2, lab3, lab5 titles | English |
| lab4 title | `Laboratoire 4 — Sujet` |
| All five lecture titles | English |
| `index.md` body | entirely English |
| project title, subtitle, `logo_text` | English |

## 2. Evidence: this is a reliability bug, not a linguistic one

`Laboratoire 4` is not an inconsistent translation. It is the only string that
*succeeded*. The others were never translated at all.

Running `deep-translator`'s free `GoogleTranslator` against the identical
inputs three times in a row:

```
trial 1: 'Lab 4 — Subject'->FAIL   'Lectures'->FAIL          'Labs'->FAIL           'Term'->FAIL
trial 2: 'Lab 4 — Subject'->FAIL   'Lectures'->'Conférences' 'Labs'->FAIL           'Term'->FAIL
trial 3: 'Lab 4 — Subject'->'Laboratoire 4 — Sujet'          'Labs'->'Laboratoires' 'Term'->'Terme'
```

Identical inputs, different outcomes per run. The free endpoint raises
`TranslationNotFound` nondeterministically at roughly a 2-in-3 rate; content is
irrelevant. `translate_text()` (`translate-sources.py:63-65`) catches every exception, prints a
warning, and returns the English original. The build then exits 0 and deploys a half-English
site.

Note: `Lectures` translates to `Conférences`, not to itself. It is not a false
friend — it simply failed on the deploy run. (`Cours` is preferable to
`Conférences` for a course sidebar, but that is a phase-3 preference, not a bug.)

### Contributing causes

1. **Silent failure.** Every exception falls back to English and the build succeeds.
2. **No retry.** A single failed call permanently yields English for that string.
3. **No cache.** Every build re-translates the whole corpus, provoking throttling.
4. **Line-by-line segmentation.** `translate_markdown_body` iterates one line at
   a time, so hard-wrapped paragraphs are sent as mid-sentence fragments — e.g.
   `statistical practices, and a lack of transparency in how research is`.
5. **Unprotected external links.** Only `[...](#anchor)` is shielded
   (`translate-sources.py:279`); a
   `[text](https://...)` link is shipped to the translator URL and all.

## 3. Decisions

| Decision | Choice | Rationale |
| --- | --- | --- |
| Backend | Keep free Google via `deep-translator` | No key, no cost; failures are transient and retryable |
| Reliability | Retry with backoff + a persistent cache | ~1/3 success per call means 8 attempts exceeds 98% |
| Cache location | Orphan branch, bot-owned | Avoids JSON merge conflicts across parallel content branches |
| Term overrides | `translations/fr.overrides.json` in `main` | Human intent stays reviewable alongside content |
| Failure policy | Fail the build on unresolved strings | A half-English site becomes unshippable |
| Segmentation | Block-level rewrite of the walker | Fixes fragmenting; also cuts call volume |

## 4. Architecture

Today parsing, network calls, and error handling are interleaved in a single
line-walking loop. The rewrite separates them into four stages with one
injected seam:

```
sources ──▶ segment ──▶ resolve ──▶ render ──▶ _translated/fr/
                          │
                          ├─ override hit → use it   (no network)
                          ├─ cache hit    → use it   (no network)
                          ├─ miss         → translate(retry×8) → validate → cache
                          └─ unresolved   → collect
                                              │
                                      report + exit 1
```

`resolve` accepts `translate_fn` as a parameter. Production passes the
Google-with-retry callable; tests pass a deterministic fake. This is what makes
the parser testable without touching the network.

## 5. Components

### 5.1 `segment(body) -> list[Block]`

Returns typed blocks. Only the last four kinds are translatable:

| Kind | Handling |
| --- | --- |
| `fence` | verbatim (``` / ~~~) |
| `math_block` | verbatim (`$$`) |
| `directive` | recursive; see below |
| `blank` | verbatim |
| `heading` | translate text, preserve `#` prefix |
| `list_item` | translate text, preserve marker and indent |
| `table` | translate each cell, preserve separators |
| `paragraph` | consecutive prose lines joined and translated as **one** unit |

Directive handling is unchanged in policy: admonitions translate title and body,
`figure` translates the caption only, all others are preserved verbatim.

Translated paragraphs are emitted unwrapped on a single line. `_translated/` is
gitignored, so line width there is irrelevant, and unwrapped output cannot
reintroduce the fragmenting bug on a later pass.

Measured effect on the current corpus: 318 line-level calls become 199
block-level calls (1.6x). The ratio is higher on real prose — `lecture1.md`
goes 77 to 33 (2.3x) — and will improve as placeholder stubs are filled in.

### 5.2 Shielding and validation

Existing shielding is retained (MyST roles, inline math, inline code,
cross-reference links; `translate-sources.py:273-279`) and extended to
**external link URLs**, which are currently unprotected.

Rather than adding one regex per mangling class, every translation is validated
before acceptance:

- every `XPHX<n>XPHX` placeholder present in the input is present in the output
- markdown link count is preserved
- emphasis marker parity (`**`, `*`, `_`) is preserved

A validation failure is treated exactly like a network failure: retry, then
record as unresolved. This catches placeholder loss, `**Reproducibility**`
mangling, and link damage generically.

### 5.3 Resolution order

```
overrides → cache → translate(retry) → unresolved
```

Cache keys are the **shielded** string (after placeholder substitution), so
editing a URL or a code span does not invalidate the surrounding sentence's
translation.

The cache writer **only adds keys; it never overwrites an existing one.**

### 5.4 Retry

8 attempts, exponential backoff (1s, 2s, 4s, 8s, 16s, capped at 30s) with
jitter, on `TranslationNotFound` and network errors. Attempt count is
configurable via CLI so the initial bootstrap can be run more patiently.

## 6. Cache and overrides layout

```
main branch (human-owned)
  translations/fr.overrides.json    ← hand-edited; starts as {}
      { "Lectures": "Cours" }

translation-cache branch (orphan, bot-owned)
  fr.cache.json                     ← CI only; never hand-edited
      { "Labs": "Laboratoires", ... }
```

The orphan branch shares no history with `main` and contains only the cache
file. Content branches never touch it, so cache updates cannot produce merge
conflicts with content work. The cache is also global rather than per-branch,
which makes read-only PR builds possible later if wanted.

JSON is written sorted, 2-space indent, `ensure_ascii=False`, so diffs are
readable.

## 7. Failure policy

Any string that is neither overridden, nor cached, nor successfully translated
and validated within 8 attempts is collected and reported:

```
=== 3 strings could not be translated ===
  index.md:8      "Modern research increasingly depends on code, data..."
  labs/lab2.md:41 "Choose a dataset that meets the following criteria..."

Re-run the job, or pin a translation in translations/fr.overrides.json.
```

The script then exits 1. `build-french.py:29` already propagates a nonzero exit
into a failed job, so no change is needed there beyond the rename.

## 8. CI workflow changes

The build job gains a second checkout, a cache path argument, and a write-back
step:

```yaml
permissions:
  contents: write          # required for cache write-back

- uses: actions/checkout@v7            # content
- uses: actions/checkout@v7            # cache
  with: { ref: translation-cache, path: .tcache }
  continue-on-error: true              # tolerate a missing branch

- run: python3 scripts/build-french.py --cache .tcache/fr.cache.json

- name: Commit refreshed translation cache
  continue-on-error: true
  run: |
    cd .tcache
    git add fr.cache.json
    git diff --cached --quiet || git commit -m "Update translation cache [skip ci]"
    git pull --rebase && git push
```

Notes:

- `build-french.py` gains a `--cache PATH` option that it forwards verbatim to
  `translate_sources.py`; both default to `.tcache/fr.cache.json` when omitted.
  The overrides path is fixed at `translations/fr.overrides.json` and is not
  configurable.
- `[skip ci]` rather than `paths-ignore:` — `paths-ignore` would prevent a
  redeploy when a human edits the overrides file, which is the opposite of the
  desired behavior.
- Write-back runs **immediately after translation**, before the slower deploy,
  so `cancel-in-progress: true` cannot discard newly translated entries.
- Write-back is `continue-on-error`: a failed push costs one re-translation on
  the next build, not correctness.
- The existing `concurrency` group serializes deploys, so pushes to the cache
  branch cannot race.

### 8.1 Staging divergence (discovered during design)

The staging repo's default branch is `mb/lecture3`, whose `deploy.yml` differs
from `main`'s:

| | `main` | staging default branch |
| --- | --- | --- |
| Trigger | push to `main` + `workflow_dispatch` | push to any branch |
| `BASE_URL` | unset | `/myst_book-staging` |
| Jobs | split build / deploy | single job |
| `contents` permission | unset | `read` |

`mb/tradfix` is based on `main`, so pushing it does **not** trigger a deploy;
it must be run via `workflow_dispatch`. That is desirable — no accidental
deploys from this branch.

Staging Pages is a project site at
`https://mathieuboudreau.github.io/myst_book-staging/`. Because `main`'s
workflow does not set `BASE_URL`, a staging build from this branch would have
broken asset paths. See open item 12.1.

## 9. Testing

`scripts/translate-sources.py` is renamed to `scripts/translate_sources.py` so
it can be imported (the hyphen currently prevents this). The reference in
`build-french.py:36` is updated.

New `tests/test_translate_sources.py`, run under pytest with a fake
`translate_fn` and no network access:

- segmentation: each block kind, and prose joining across wrapped lines
- shield/restore round-trip, including external links
- validation rejects dropped placeholders, lost links, broken emphasis
- cache: hit, miss, and the never-overwrite property
- overrides take precedence over cache
- unresolved strings produce a report and exit code 1
- golden test over the real sources with a fake translator, asserting code
  blocks, math blocks, and non-admonition directives are byte-identical

A `tests.yml` workflow runs pytest on `pull_request` and `push`. This is worth
adding because PRs do not currently build anything, so a parser regression
would otherwise surface only after merge.

## 10. Verification plan — staging only

All verification runs against `mathieuboudreau/myst_book-staging`. Nothing is
pushed to `origin`.

1. Bootstrap the cache locally (translation pass only — no `myst` required).
2. Create the `translation-cache` orphan branch on staging with the result.
3. Review the bootstrapped translations; pin any obvious term fixes in
   `fr.overrides.json`.
4. Push `mb/tradfix` to staging; run the deploy via `workflow_dispatch`.
5. Assert on the built output that all five lab titles, all five lecture titles,
   both TOC sections, the project title/subtitle/logo_text, and the `index.md`
   body are French.
6. Negative test: add an English sentence, re-dispatch, and confirm the miss is
   translated, the site deploys, and the cache branch received a write-back
   commit.
7. Failure test: run with retries forced to 0 against an uncached string and
   confirm the build fails with the report rather than deploying English.

## 11. Non-goals

- Phase 3: curated glossary and preferred-term tooling. The overrides file is a
  seam only; no tooling is built for it here.
- Changing the target language or adding languages.
- The language switcher (`language-switcher.js`, `inject-language-switcher.py`).
- Any change to English source content.
- Reconciling the staging and `main` workflow variants.

## 12. Open items for review

### 12.1 `BASE_URL` for staging verification

`main`'s workflow does not set `BASE_URL`, so a staging deploy from this branch
would render with broken asset paths. Options:

- **(a)** Add `env: BASE_URL: ${{ vars.BASE_URL }}` to the workflow and set the
  repo variable on staging only. Unset on `origin` yields `""`, preserving
  current production behavior exactly. One line, prod-safe.
- **(b)** Leave the workflow alone and verify by inspecting the build artifact
  and the embedded Remix JSON rather than the rendered page. The JSON carries
  every string being verified, so this is sufficient for correctness — the
  staging page just looks broken.

Recommendation: (a).

### 12.2 Rollout to `origin`

When this eventually lands on `origin`, the `translation-cache` orphan branch
must be created there too, and the initial cache pushed to it. Otherwise the
first production build starts from an empty cache and must translate ~200
strings in one run.
