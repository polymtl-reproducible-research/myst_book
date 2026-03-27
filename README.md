# My Book Title

A MyST book template.

## Getting Started

### Prerequisites

- [Node.js](https://nodejs.org/) (v18 or later)
- [mystmd](https://mystmd.org/) (`npm install -g mystmd`)

### Local Development

```bash
myst start
```

This will start a local development server with live reload.

### Building

```bash
myst build --html
```

The built site will be in `_build/html/`.

### Deployment

This repository includes a GitHub Actions workflow that automatically deploys to GitHub Pages on push to `main`. Enable GitHub Pages in your repository settings (Settings > Pages > Source: GitHub Actions).

## Project Structure

```
.
├── myst.yml                  # Main configuration
├── index.md                  # Landing page
├── chapters/
│   ├── 01-introduction.md    # Chapter 1
│   ├── 02-methods.md         # Chapter 2
│   └── 03-results.md         # Chapter 3
├── notebooks/
│   └── example-notebook.ipynb
├── bibliography/
│   └── references.bib
├── figures/
│   └── placeholder.png
└── .github/workflows/
    └── deploy.yml            # GitHub Pages deployment
```

## License

MIT
