# My Book Title

A MyST book template.

## Getting Started

### Prerequisites

- [conda](https://docs.conda.io/) (or [miniconda](https://docs.conda.io/en/latest/miniconda.html))

### Local Development

```bash
git clone https://github.com/polymtl-reproducible-research/myst_book.git
cd myst_book
conda create -n ing8100 python=3.12  # a fresh environment for this course
conda activate ing8100
conda install -c conda-forge mystmd   # brings Node with it
myst start   # opens the site at localhost, with live reload
```

### Building

```bash
myst build --html
```

The built site will be in `_build/html/`.

### Previews for pull requests

Warning: these steps deploy the preview to the main website. You should re-deploy the `main` branch as soon as you're done. (The `main` branch is also automatically re-deployed if any pull request gets merged, in which case you don't have to re-deploy it manually.)

To build and deploy a pull request preview of the website:

1. Go to the workflow page: https://github.com/polymtl-reproducible-research/myst_book/actions/workflows/deploy.yml
2. Click "Run workflow" on the right side.
3. Select the branch you want to preview.
4. Click "Run workflow".
5. This will build the website and make it visible at: https://reproducible-research.polymtl.ca/

<img width="950" height="508" alt="image" src="https://github.com/user-attachments/assets/4f057eb9-176e-4264-8fe2-bfdb56cadb11" />

### Deployment

To see the current status of the website (that is, which branch/commit is currently visible online), look at the latest deployment here: https://github.com/polymtl-reproducible-research/myst_book/deployments

[This workflow](https://github.com/polymtl-reproducible-research/myst_book/actions/workflows/deploy.yml) automatically re-deploys the `main` branch to https://reproducible-research.polymtl.ca/ whenever there is a push (including when a pull request is merged).

## Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project, including branch naming conventions, workflow, and development setup.

## Code of Conduct

All course participants are expected to follow the [Code of Conduct](CODE_OF_CONDUCT.md).

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
