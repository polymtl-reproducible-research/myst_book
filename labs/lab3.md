---
title: Lab 3 — Building a Reproducible Open Science Project
date: 2026-05-24
label: lab3
numbering:
  heading_2: false
---

# Introduction

This laboratory introduces the principles of reproducible research through the development of a complete open science project. You will organize a repository following community best practices, manage a reproducible computational environment, and build a documented data analysis workflow using Git and GitHub.

---

# GitHub Environment

## Create a repository

## Add and edit the `README.md` file

The `README.md` file is the entry point to your project. It provides the information needed for others to understand your work, reproduce your results, and reuse your repository. 

You may use the following template as a starting point:

Template: [World Bank README template](https://github.com/worldbank/wb-reproducible-research-repository/blob/main/resources/README_Template.md)

The `README.md` should be updated throughout the lab as you build your project.

## Add a license to your repository

A [license](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository) defines how others are allowed to use, modify, and share your project. 

## Add a Code of Conduct

A [Code of Conduct](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/adding-a-code-of-conduct-to-your-project) establishes clear expectations for respectful and inclusive collaboration within your project. 

## Add CONTRIBUTING.md file

A [`CONTRIBUTING.md`](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/setting-guidelines-for-repository-contributors) file explains how others can participate in your project. It defines clear guidelines for submitting changes, reporting issues, and following project conventions. 

## Add branch protection rules 

[Branch protection](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches) rules help maintain the integrity of your repository by preventing direct or unreviewed changes to critical branches. 

### Protect `main`

The `main` branch should always remain stable and represent a working version of the project. Direct pushes to this branch must be prevented so that all changes go through a controlled review process.

### Pull requests required with at least one review

All changes must be submitted through pull requests and reviewed by at least one other team member. This ensures that no one approves their own changes and promotes collaborative validation of the work.

### Branch naming convention

A consistent branch naming convention must be followed to keep the project history clear and readable. This helps avoid confusion and makes it easier to understand the purpose of each branch.

## Add issues

You must use GitHub Issues to structure and track the work of your project. Each issue should represent a clear task or objective, and the work should be distributed across the team. 

You need:
- At least 3 issues,
- At least one assigned to each member,
- At least one closed via PR.

---
# Code environment

## Create a folder structure

A clear folder structure separates raw data, processed data, code, results, and documentation in a consistent way, making the workflow easier to understand and navigate. 

For example :

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

Create a virtual environment to isolate project dependencies and ensure a reproducible computational setup. This prevents conflicts with other projects and avoids polluting your global environment.

## Create a script to download the data

Create a script that retrieves the dataset from Borealis. This step ensures that data acquisition is automated and reproducible, rather than performed manually.

## Create a script to preprocess the data

Create a preprocessing script to clean and standardize the raw data before analysis. This may include :
- missing values handling
- renaming / formatting columns
filtering rows (basic criteria)
- simple type conversion (string → numeric/date)
- removing obvious outliers if justified

## Create a script to analyze your data

Create a script that performs the data analysis and generates the results. The script should compute summary metrics and produce visualizations that help answer your research question. The use of Pandas, NumPy, and Matplotlib is recommended.

### Compute 2–3 metrics

Compute at least two or three meaningful metrics from your dataset. Typical examples include:

- Mean
- Correlation
- Grouped statistics

### Produce 1–2 visualizations

Produce one or two visualizations that communicate your results effectively. Each visualization must:

- Be directly related to the research question or a computed metric.
- Be understandable without reading the source code.
- Include appropriate axis labels, a title, and a short explanation.

Examples include:

- Scatter plot with a correlation analysis.
- Bar plot of grouped means.
- Distribution plot with summary statistics.

### Comment your code

Write clear, readable code and include comments where they improve understanding. Comments should explain the purpose or reasoning behind the code rather than restating what individual statements do. Refer to the [MIT Communication Lab guidelines on coding and comment style](https://mitcommlab.mit.edu/broad/commkit/coding-and-comment-style/) for recommendations.

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
| Report | Report clearly presents and explains the analysis results | 10 | -2 for each missing required section. -1 for each figure quality issue. (title, explanation, unit, etc.)|
| .gitignore | Appropriate files and directories are excluded from version control | 5 | -1 for each major omission (environment files, raw data, temporary files, caches, etc.). |
| Workflow | Git workflow demonstrates appropriate use of branches, commits, pull requests, and reviews | 20 | -5 if branches are not used appropriately. -5 if pull requests are missing. -5 if reviews are missing. -5 if commit history does not demonstrate regular project progression. |
| AI_Prompts | AI usage is properly documented and attributed | 5 | -2.5 if AI usage is partially documented. -5 if AI usage is not documented. |
