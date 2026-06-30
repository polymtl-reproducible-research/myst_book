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

## Repository

Create a repository in the ING8100 organization.

## `README.md` file

The `README.md` file is the entry point to your project. It provides the information needed for others to understand your work, reproduce your results, and reuse your repository. 

You may use the following template as a starting point:

Template: [World Bank README template](https://github.com/worldbank/wb-reproducible-research-repository/blob/main/resources/README_Template.md)

The `README.md` should be updated throughout the lab as you build your project.

## License

A [license](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository) defines how others are allowed to use, modify, and share your project. 

## Code of Conduct

A [Code of Conduct](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/adding-a-code-of-conduct-to-your-project) establishes clear expectations for respectful and inclusive collaboration within your project. 

## CONTRIBUTING.md file

A [`CONTRIBUTING.md`](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/setting-guidelines-for-repository-contributors) file explains how others can participate in your project. It defines clear guidelines for submitting changes, reporting issues, and following project conventions. 

## AI_Prompts file


Create an `AI_Prompts.md` file that documents any prompts used during this assignment. Recording your prompts promotes transparency and allows others to better understand how AI was used throughout the project.

When writing your prompts, pay particular attention to the **Description** component of the [4D Framework](https://www-cdn.anthropic.com/334975cdec18f744b4fa511dc8518bd8d119d29d.pdf), as providing clear context is essential for obtaining useful and reproducible results. To learn more about effective prompting, you are encouraged to explore Anthropic's free [AI Fluency Framework Foundations](https://anthropic.skilljar.com/ai-fluency-framework-foundations) course. 

## Branch protection rules 

[Branch protection](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches) rules help maintain the integrity of your repository by preventing direct or unreviewed changes to critical branches. 

### Protect `main`

The `main` branch should always remain stable and represent a working version of the project. Direct pushes to this branch must be prevented so that all changes go through a controlled review process.

### Pull requests required with at least one review

All changes must be submitted through pull requests and reviewed by at least one other team member. This ensures that no one approves their own changes and promotes collaborative validation of the work.

### Branch naming convention

A consistent branch naming convention must be followed to keep the project history clear and readable. This helps avoid confusion and makes it easier to understand the purpose of each branch.

## Issues

You must use GitHub Issues to structure and track the work of your project. Each issue should represent a clear task or objective, and the work should be distributed across the team. 

You need:
- At least 3 issues,
- At least one assigned to each member,
- At least one closed via PR.

---
# Code environment

## Folder structure

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

## Virtual environment

Create a virtual environment to isolate project dependencies and ensure a reproducible computational setup. This prevents conflicts with other projects and avoids polluting your global environment.

## Download the data

Create a script that retrieves the dataset from Borealis. This step ensures that data acquisition is automated and reproducible, rather than performed manually.

## Preprocess the data

Create a preprocessing script to clean and standardize the raw data before analysis. This may include :
- missing values handling
- renaming / formatting columns
filtering rows (basic criteria)
- simple type conversion (string → numeric/date)
- removing obvious outliers if justified

## Analyze your data

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

## Report

Create a report in Markdown (`.md`) format that presents your project and communicates the results of your analysis. The report should briefly introduce the research question, describe the dataset, summarize the methodology, and discuss the main findings.

Include the figures generated by your analysis and explain what they show. Each figure should be referenced in the text and accompanied by a short interpretation that relates it to your research question.

## Virtual environment export

Export your Conda environment to an `environment.yml` file. This file captures the project's dependencies and allows others to recreate the same computational environment, improving the reproducibility of your analysis.

Refer to [Isolating programming environments for Python using Conda](https://github.com/worldbank/wb-reproducible-research-repository/blob/main/resources/environment-instructions/python.md).

## `.gitignore` file

The `.gitignore` file specifies which files and directories should not be tracked by Git. It is commonly used to exclude temporary files, caches, virtual environments, and large or generated data files that should not be stored in the repository. Keeping these files out of version control helps maintain a clean and reproducible project.

You may use the GitHub `.gitignore` template as a starting point. 

## Collaborative Git workflow

Follow the collaborative Git workflow introduced in the first lab. Develop your work on separate branches, write meaningful commit messages, and integrate changes through pull requests. This workflow improves traceability, facilitates code review, and helps maintain a stable project history.

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

| Criterion | Weight | Description |
|---|---|---|
| --- | --- | --- |
| README.md | 15% | The README.md contains all required sections and clearly documents the project. |
| License | 5% | An appropriate open-source license is included in the repository. |
| Code of Conduct | 5% | A complete Code of Conduct is provided. |
| CONTRIBUTING.md | 5% | A complete CONTRIBUTING.md file defines contribution guidelines. |
| Branch Protection Rules | 3% | Branch protection rules are configured according to the assignment requirements. |
| Issues | 6% | GitHub Issues are used to plan and track project work according to the assignment requirements. |
| Folder Structure | 3% | The repository follows the required project organization. |
| Virtual Environment | 3% | A reproducible Conda environment is provided and documented. |
| Scripts | 15% | Download, preprocessing, and analysis scripts are complete, functional, and well written. |
| Report | 10% | The report clearly presents the project, methodology, and analysis results. |
| .gitignore | 5% | The repository excludes unnecessary files from version control. |
| Development Workflow | 20% | Appropriate use of branches, commits, pull requests, reviews, and repository maintenance practices. |
| AI Prompt Documentation | 5% | AI usage is transparently documented through an AI_Prompts.md file. |


<!-- Guidelines for evaluators : 
| Criterion | Weight | Description | Evaluation |
|---|---|---|---|
| README.md | 15% | The README.md contains all required sections and clearly documents the project. | −2% for each incomplete section. −3% for each missing section. |
| License | 5% | An appropriate open-source license is included in the repository. | Full weight lost if the license is missing or inappropriate. |
| Code of Conduct | 5% | A complete Code of Conduct is provided. | −2.5% if incomplete. Full weight lost if missing. |
| CONTRIBUTING.md | 5% | A complete CONTRIBUTING.md file defines contribution guidelines. | −2.5% if incomplete. Full weight lost if missing. |
| Branch Protection Rules | 3% | Branch protection rules are configured according to the assignment requirements. | −1% for each missing or incorrectly configured rule. |
| Issues | 6% | GitHub Issues are used to plan and track project work according to the assignment requirements. | −2% for each missing issue. −1% for each unmet requirement (assignment, closure through PR, etc.). |
| Folder Structure | 3% | The repository follows the required project organization. | −0.5% for each missing or incorrectly placed file or directory. |
| Virtual Environment | 3% | A reproducible Conda environment is provided and documented. | −1% if environment.yml is missing. −1% if the environment cannot be created. −1% if setup instructions are missing or unclear. |
| Scripts | 15% | Download, preprocessing, and analysis scripts are complete, functional, and well written. | 5% per required script. −1% per code smell (unused code, duplicated code, hard-coded paths, unclear variable names, etc.). |
| Report | 10% | The report clearly presents the project, methodology, and analysis results. | −2% for each missing required section. −1% for each figure quality issue (missing title, labels, explanation, units, etc.). |
| .gitignore | 5% | The repository excludes unnecessary files from version control. | −1% for each major omission (virtual environments, caches, generated files, large datasets, etc.). |
| Development Workflow | 20% | Appropriate use of branches, commits, pull requests, reviews, and repository maintenance practices. | −5% if branches are not used appropriately. −5% if pull requests are missing. −5% if reviews are missing. −5% if the commit history does not demonstrate regular project progression. |
| AI Prompt Documentation | 5% | AI usage is transparently documented through an AI_Prompts.md file. | −2.5% if AI usage is partially documented. Full weight lost if no documentation is provided. |
 -->
