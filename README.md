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
├── poly.css                  # Custom CSS styling
├── favicon.ico               # Polytechnique icon
├── lectures/
│   ├── lecture1.md           # Lecture 1
│   ├── lecture2.md           # Lecture 2
│   ├── lecture3.md           # Lecture 3
│   ├── lecture4.md           # Lecture 4
│   └── lecture5.md           # Lecture 5
├── labs/
│   ├── lab1.md               # Lab 1
│   ├── lab2.md               # Lab 2
│   ├── lab3.md               # Lab 3
│   ├── lab4.md               # Lab 4
│   └── lab5.md               # Lab 5
├── images
│   ├── *.png                 # Site images
│   └── lab1                  # Images for lab1, etc.
│       └── *.png
├── bibliography/
│   └── references.bib        # Bibtex references
├── LICENSE
├── README.md                 # This file
└── scripts                   # French translation scripts
│   ├── build-french.py
│   ├── inject-language-switcher.py
│   ├── language-switcher.js
│   ├── translate-sources.py
│   └── TRANSLATION.md        # Scripts explanation
└── .github/workflows/
    └── deploy.yml            # GitHub Pages deployment
```

## License

MIT
