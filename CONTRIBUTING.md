# Contributing

Thank you for your interest in contributing! We welcome contributions to improve this MyST book.

## Getting Started

### Fork and Clone

```bash
git clone https://github.com/YOUR_USERNAME/myst_book.git
cd myst_book
```

### Set Up Your Environment

Install the required tools:

```bash
npm install -g mystmd
pip install deep-translator pyyaml
```

## Workflow

### 1. Create a Feature Branch

Use the naming convention `(initials)/(topic)`:

```bash
git checkout -b mb/add-new-lab
```

where `mb` are your initials and `add-new-lab` describes your change.

### 2. Make Your Changes

- **Add content**: Edit files in `chapters/`, `labs/`, or `notebooks/`
- **Update figures**: Place images in `figures/` and reference them without `./` prefix
- **Add references**: Update `bibliography/references.bib`
- **Update TOC**: Edit `myst.yml` if adding new pages or chapters

### 3. Test Locally

Before pushing, build and preview locally:

```bash
myst start
```

This starts a dev server. For testing the full build (including French translation):

```bash
myst build --html
python3 scripts/build-french.py
python3 scripts/inject-language-switcher.py
```

Check the output in `_build/html/`.

### 4. Push and Create a Pull Request

```bash
git push origin mb/add-new-lab
```

Then open a pull request on GitHub with:
- **Title**: Brief description of what you added/changed
- **Description**: Explain the what, why, and how you tested it

### 5. Merge to Main

The live site builds and deploys automatically after merging to `main`.

## Important Notes

⚠️ **Do not edit `.github/workflows/deploy.yml`** to build from your branch. The deployment workflow is locked to `main` only. Modifying it could break the live site.

## What to Know About This Project

- **Source of truth**: English content (`en/` or direct chapters)
- **Translations**: French site is auto-generated from English via `build-french.py`. Do not manually edit translated files.
- **Build artifacts**: The `_build/` directory, `_translated/`, and related build folders are generated and not committed.
- **Naming conventions**:
  - Chapters: `chapters/NN-name.md` (e.g., `01-introduction.md`)
  - Lab worksheets: `labs/labN.md`
  - Notebook exercises: `notebooks/`
  - Figures: Reference as `figures/image-name.png` (no `./` prefix)

## Commit Best Practices

- Make focused, logical commits (one feature or fix per commit)
- Write clear commit messages
- Reference related issues if applicable

## Questions?

If you're unsure about something, open an issue first to discuss before starting work. This helps avoid duplicate effort and ensures alignment with project goals.

Thank you for contributing!
