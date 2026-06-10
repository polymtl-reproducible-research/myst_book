---
title: Lab 3 — Building a Reproducible Open Science Project
date: 2026-05-24
label: lab3
numbering:
  heading_2: false
---

# Introduction
source: https://book.the-turing-way.org/

:::{attention}
TODO : Write the introduction part
:::
---

# GitHub Environment

## Create a repository

## Add and edit the README.md file
Template here : [Worldbank README template](https://github.com/worldbank/wb-reproducible-research-repository/blob/main/resources/README_Template.md)

## Add a license to your repository
Source : [Licensing a repository](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository)

## Add a Code of Conduct
Source : [Adding a code of conduct to your project](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/adding-a-code-of-conduct-to-your-project)

## Add CONTRIBUTING.md file
Source : [Adding a CONTRIBUTING.md file](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/setting-guidelines-for-repository-contributors)

## Add branch protection rules 
Source : [About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches)
### Protect main 
### PR required with one review at least
### Branch naming convention

## Add issues
- at least 3 issues,
- at least one assigned to each member,
- at least one closed via PR.

---
# Code environment

## Create a folder structure
example

project-root/ <br>
│ <br>
├── README.md <br>
├── environment.yml <br>
├── .gitignore <br>
├── data/ <br>
│   ├── raw/ <br>
│   └── processed/ <br>
├── scripts/ <br>
│   ├── download_data.py <br>
│   └── analyze.py <br>
├── notebooks/ <br>
├── figures/ <br>
└── results/ <br>

## Create a virtual environment

## Create a script to download the data
- load data from borealis

## Create a script to preprocess the data 
- missing values handling
- renaming / formatting columns
filtering rows (basic criteria)
- simple type conversion (string → numeric/date)
- removing obvious outliers if justified

## Create a script to analyse your data

Usage of pandas, NumPy and matplotlib are recommended libraries

### Compute 2–3 metrics 
- mean
- correlation 
- grouped statistics

### Produce 1–2 visualizations

A visualization must:

- be tied to the research question OR a computed metric
be interpretable without code
- include labels + short explanation

Examples:

- scatter plot + correlation
- bar plot of grouped means
- distribution plot + summary stats

### Comment your code

## Create a notebook to record the results

Figures should be presented and explained in the notebook.
:::{attention}
TODO : Explain further the notebook part
:::

## Export the virtual environment using Conda

Source form worldbank : [Isolating programming environments for Python using Conda](https://github.com/worldbank/wb-reproducible-research-repository/blob/main/resources/environment-instructions/python.md)

## Change the README.md file

## Create a gitignore file
You can use the GitHub gitgnore template

## Follow the appropriate workflow 
branches, commit, PR, merge

---

# Bonus — Continuous Integration (CI)

Continuous Integration (CI) is commonly used in open science projects to automatically verify that a project remains reproducible as it evolves.

Using GitHub Actions, implement at least one automated workflow for your repository.

Possible examples include:

- Run a linter on Python scripts (e.g., Ruff, Flake8, Pylint).
- Verify that the Conda environment can be created successfully.
- Execute the preprocessing and analysis scripts.
- Generate the notebook automatically from scripts.
- Check that required repository files are present (README, LICENSE, CONTRIBUTING, etc.).

## Requirements

- Create at least one GitHub Actions workflow in `.github/workflows/`.
- Document the workflow in the README.
- The workflow must execute automatically when a Pull Request is opened or updated.

---

# Evaluation 

| Task | Description | Points | Explanation |
| ---- | ----------- | ------ | ---------------------------------- |
| README.md | All required sections are complete and clearly documented | 15 | -2 if a section is incomplete. -3 if a section is missing. |
| License | An appropriate open-source license is provided for the repository | 5 | -5 if the license is missing or inappropriate. |
| Code of Conduct | A complete Code of Conduct is present in the repository | 5 | -2.5 if the Code of Conduct is incomplete. -5 if it is missing. |
| CONTRIBUTING.md | A complete CONTRIBUTING.md file is present in the repository | 5 | -2.5 if CONTRIBUTING.md is incomplete. -5 if it is missing. |
| Branch Protection Rules | Required branch protection rules are configured correctly | 3 | -1 for each missing or incorrectly configured rule. |
| Issues | Repository issues follow the assignment requirements | 6 | -2 for each missing issue. -1 for each unmet requirement. |
| Folder Structure | Repository follows the required project structure | 3 | -0.5 for each missing or incorrectly placed file/folder. |
| Virtual Environment | A working Conda environment is provided and documented | 3 | -1 if environment.yml is missing. -1 if the environment cannot be created. -1 if setup instructions are missing or unclear. |
| Scripts | Download, preprocessing, and analysis scripts are present and functional | 15 | 5 points per script. -1 per code smell (unused code, duplicated code, hard-coded paths, unclear variable names, etc.). |
| Notebook | Notebook clearly presents and explains the analysis results | 10 | -2 for each missing required section. -1 for each figure quality issue. (title, explanation, unit, etc.)|
| .gitignore | Appropriate files and directories are excluded from version control | 5 | -1 for each major omission (environment files, raw data, temporary files, caches, etc.). |
| Workflow | Git workflow demonstrates appropriate use of branches, commits, pull requests, and reviews | 20 | -5 if branches are not used appropriately. -5 if pull requests are missing. -5 if reviews are missing. -5 if commit history does not demonstrate regular project progression. |
| AI_Prompts | AI usage is properly documented and attributed | 5 | -2.5 if AI usage is partially documented. -5 if AI usage is not documented. |
