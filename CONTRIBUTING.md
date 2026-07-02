# Contributing

Thank you for your interest in contributing! We welcome contributions to improve this MyST book.

## Getting Started

### Clone

```bash
git clone https://github.com/polymtl-reproducible-research/myst_book.git
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

⚠️ **Never weaken the deployment gate in `.github/workflows/deploy.yml`.** Deployment is controlled by the `BUILD_BRANCH` repository variable (set to `main` in this repo). Do not remove or modify the `if: github.ref_name == vars.BUILD_BRANCH` condition — it is the only thing preventing feature branches from deploying over the live site.

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

## Optional: Set Up a Personal Staging Site

If you want to preview your branch as a live site (e.g., to share with others or test the full
deployed build including the French translation) without touching the production site, you can
deploy your branch to GitHub Pages on a repo under your personal account.

No workflow changes are needed: the deploy workflow triggers on every branch, but deployment
is gated by the `BUILD_BRANCH` repository variable. In the main repo it's set to `main`, so
pushes to feature branches only produce skipped runs there. In your staging repo, you'll set
it to your branch.

### 1. Create an empty repo on your personal account

On github.com (logged into your personal account), create a new **public** repository
(e.g., `myst_book-staging`). Leave it empty — no README or license.
(Pages on private repos requires GitHub Pro.)

### 2. Add it as a second remote

```bash
git remote add staging https://github.com/YOUR_USERNAME/myst_book-staging.git
git remote -v   # you should now see both origin and staging
```

### 3. Push your branch to your staging repo

```bash
git push -u staging mb/add-new-lab
```

The `-u` flag makes future `git push` from this branch go to your staging repo by default.
To push to the main repo (e.g., for a PR), use `git push origin mb/add-new-lab` explicitly.

### 4. Configure the staging repo

In your staging repo on GitHub:

1. **Settings → Pages → Source**: select **GitHub Actions**
2. **Settings → Environments → New environment**: create one named `gh-pages`
   (no protection rules needed)
3. **Settings → Secrets and variables → Actions → Variables tab → New repository variable**:
   - Name: `BUILD_BRANCH`
   - Value: your branch name (e.g., `mb/add-new-lab`)

### 5. Trigger a build

If the first push ran before Pages was enabled, go to the **Actions** tab in your staging
repo and re-run the failed workflow (or push a small commit). Once it goes green, your
preview site is live at:

```
https://YOUR_USERNAME.github.io/myst_book-staging/
```

The `BASE_URL` in the workflow adapts to the repo name automatically, so links and assets
will work without changes.

### Day-to-day loop

```bash
# iterate: builds your staging preview
git push

# when ready for review: opens the door to a PR on the main repo
git push origin mb/add-new-lab
```

### Switching to a new branch later

The `BUILD_BRANCH` variable points at one branch. When you start a new feature branch,
update the variable in your staging repo's settings to the new branch name.

## Questions?

If you're unsure about something, open an issue first to discuss before starting work. This helps avoid duplicate effort and ensures alignment with project goals.

Thank you for contributing!
