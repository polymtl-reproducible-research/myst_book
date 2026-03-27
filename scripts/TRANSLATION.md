# Automatic French Translation for MyST Books

This document explains how the build-time French translation system works and how to reuse it in another MyST book project.

## How it works

The translation runs entirely at build time during the GitHub Actions deployment. No client-side translation APIs are used. The result is two fully independent MyST sites: English at `/` and French at `/fr/`.

### Build pipeline

The deployment workflow (`.github/workflows/deploy.yml`) runs these steps in order:

1. `myst build --html` -- builds the English site to `_build/html/`
2. `python3 scripts/build-french.py` -- translates sources and builds the French site
3. `python3 scripts/inject-language-switcher.py` -- injects the EN/FR flag widget into all pages

### Step-by-step breakdown

#### 1. Source translation (`scripts/translate-sources.py`)

Reads `myst.yml` to discover all source files from the table of contents, then for each file:

- **Markdown files (`.md`)**: Parses YAML frontmatter and translates the `title` and `description` fields. Walks the body line-by-line, translating prose while preserving:
  - Code blocks (fenced with `` ``` `` or `~~~`)
  - Math blocks (`$$...$$`)
  - MyST directives (```{figure}```, `:::{admonition}`, etc.) -- translates caption/body text but not directive names, labels, or options
  - Inline roles (`{cite:p}`, `{ref}`, etc.)
  - Inline math (`$...$`)
  - Inline code (`` `...` ``)
  - Cross-reference links (`[](#label)`)
  - Table structure (translates cell text, preserves separators)
- **Jupyter notebooks (`.ipynb`)**: Translates markdown cells only; code cells and outputs are untouched.
- **Other assets**: Copies `figures/` and `bibliography/` directories as-is.

Translation uses `deep-translator` (GoogleTranslator), which calls Google Translate for free with no API key. Calls are rate-limited with 300ms delays to avoid throttling.

Output goes to `_translated/fr/`, mirroring the original directory structure.

#### 2. French site build (`scripts/build-french.py`)

1. Runs `translate-sources.py`
2. Creates a translated `myst.yml` in `_translated/fr/` with:
   - Translated project title, subtitle, logo text, and TOC section titles
   - Same theme, bibliography, and configuration as the original
3. Runs `myst build --html` inside `_translated/fr/` with `BASE_URL` set to include `/fr`
4. Copies the French build output from `_translated/fr/_build/html/` into `_build/html/fr/`

This produces a fully self-contained MyST site under `/fr/` with its own JSON data files, config, and HTML -- meaning React/Remix SPA navigation works correctly within the French version.

#### 3. Language switcher (`scripts/language-switcher.js` + `scripts/inject-language-switcher.py`)

The inject script copies `language-switcher.js` into both the English and French build directories, then injects a `<script>` tag and a `<meta name="base-url">` tag into the `<head>` of every HTML file.

The language switcher JS works around a key constraint: MyST uses Remix (React) with `hydrateRoot(document)`, meaning React owns the entire DOM tree and will remove any injected DOM elements during SPA navigation.

The solution uses zero DOM injection:

- **Visual widget**: Rendered as a `body::after` CSS pseudo-element via `document.adoptedStyleSheets`. Pseudo-elements are CSS constructs, not DOM nodes -- React cannot remove them. The adopted stylesheet is a property on the Document object, also invisible to React.
- **Click handling**: A `document.addEventListener('click', fn, true)` listener in capture phase detects clicks by checking if the mouse coordinates fall within the widget's fixed position (bottom-right corner). Left half = English, right half = French.
- **Navigation**: Clicking a flag does `window.location.href = ...` (full page load), switching between `/` and `/fr/` paths.
- **Preference persistence**: Stores the language choice in `localStorage` under `myst-lang`. On page load, auto-redirects to the preferred language. Defaults to French if no preference is set.

## Reusing in another MyST book

### Files to copy

Copy the entire `scripts/` directory into your new project:

```
scripts/
  translate-sources.py    # Translates .md and .ipynb source files
  build-french.py         # Orchestrates the French build
  inject-language-switcher.py  # Injects the widget into HTML files
  language-switcher.js    # EN/FR flag widget (CSS + click handling)
```

### Workflow changes

Add these steps to your `.github/workflows/deploy.yml` **after** `myst build --html` and **before** uploading artifacts:

```yaml
- name: Install Python dependencies
  run: pip install deep-translator pyyaml

- name: Translate and build French site
  run: python3 scripts/build-french.py

- name: Inject Language Switcher
  run: python3 scripts/inject-language-switcher.py
```

### .gitignore

Add this line to prevent committing generated translation files:

```
_translated/
```

### Requirements

- Python 3 (available by default on `ubuntu-latest` GitHub Actions runners)
- `deep-translator` and `pyyaml` Python packages (installed in the workflow)
- `mystmd` (already required for any MyST book)
- No API keys or secrets needed

### Customization

- **Default language**: In `language-switcher.js`, the auto-redirect defaults to French. Change `|| 'fr'` to `|| 'en'` to default to English.
- **Target language**: In `translate-sources.py`, change `GoogleTranslator(source="en", target="fr")` to any language pair supported by Google Translate.
- **Flag icons**: The SVG flags are embedded as base64 data URIs in `language-switcher.js`. Replace the `ukUri` and `qcUri` variables with your own flag SVGs.
- **Widget position**: Adjust the `PAD_BOTTOM`, `PAD_RIGHT`, `W`, and `H` constants in `language-switcher.js` (and matching values in the CSS string).
- **Translation corrections**: Add post-translation term corrections in `translate-sources.py` if Google Translate consistently mistranslates domain-specific terms.
