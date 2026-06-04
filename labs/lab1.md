---
title: Lab 1 — Reproducibility and Replicability
date: 2026-03-27
label: lab1
numbering:
  heading_2: false
---

# Introduction

:::{important}
**Submission deadline:** *To be determined*  
**Team formation:** This laboratory must be completed in teams of two students.
:::

This first laboratory introduces the fundamental concepts of reproducibility and replicability in open and computational science. Students will work through the complete setup of a collaborative scientific workflow, including account creation, local environment preparation, and organizational setup.

The laboratory culminates in two complementary activities:

1. reproducing an existing computational result using the original environment and methodology;
2. replicating the experiment under modified conditions or environments.

# Laboratory procedure

:::{important}
Before starting the laboratory, ensure that you have selected a team on the course Moodle page and identified a teammate.
:::

## Account creation

### GitHub

Create a [GitHub](https://github.com/signup) account and provide both your username and your teammate’s username to the course staff.

This account is required in order to grant your team access to a dedicated repository, which will be used throughout the laboratory activities and for the organizational setup phase.

### Borealis

Create an account on [Borealis](https://borealisdata.ca/loginpage.xhtml) using your institutional email address.

## Local setup

### Visual Studio Code

Install [Visual Studio Code](https://code.visualstudio.com/download), which will be used as the primary code editor throughout the laboratory.

### Git

As discussed in class, Git will be used for version control of both code and data. Install [Git](https://git-scm.com/install/) on your system.

### Miniforge

Install [Miniforge](https://conda-forge.org/download/).

Miniforge is a lightweight Conda distribution used to create and manage reproducible Python environments. It is configured by default to use the community-maintained `conda-forge` package repository, which is widely adopted in scientific and research environments.

### GitHub Desktop

*To be determined.*

## Organizational setup

Accept the invitation to the GitHub organization that will be sent to the email address associated with your GitHub account.

## Onboarding with GitHub

### Modify a file from the GitHub interface

Modify the `README.md` file directly from the GitHub web interface.

*Screenshot to add*

Select the option **Create a new branch and start a pull request**.

### Open the pull request
*Screenshot to add*

### Merge the pull request
*Screenshot to add*

## Reproducibility

:::{hint}
If you see text enclosed in angle brackets (`<...>`), replace it with your own value and remove the brackets.

For example:

```bash
git clone https://github.com/johndoe/notarealrepo.git
```
:::

:::{hint}
Use git status to take a look at what is going on.
:::

### Clone the repository

```bash
git clone <repository-url>
```

### Create a new branch

```bash
git switch -c <branch-name>
```

:::{note}
The `-c` option creates a new branch. Use a meaningful and descriptive branch name.
:::

### Create the virtual environment

Follow the instructions provided in the `README.md` file.

### Data analysis

Follow the instructions provided in the `README.md` file.

### Add modified files to the staging area

Add the generated figure using:

```bash
git add <file-name>
```

or:

```bash
git add .
```

to stage all modified, added, or deleted files.

### Create a commit

```bash
git commit -m "<commit-message>"
```

:::{note}
Use a meaningful and descriptive commit message.
:::

### Push the changes

```bash
git push
```

The first push of a new branch must set the upstream branch:

```bash
git push --set-upstream origin <branch-name>
```

### Create a pull request
Use the GitHub interface to create the pull request (PR). 

### Merge the pull request
The person who did not create the PR must merge the PR

### Delete the branch
Once the PR is merged, delete the source branch (not `main`).

## Replicability

### Return to the `main` branch

```bash
git switch main
```

### Pull the latest changes

```bash
git pull origin main
```

### Create a new branch

```bash
git switch -c <branch-name>
```

:::{note}
Use a meaningful and descriptive branch name.
:::

### Modify the analysis parameters

Open the `analysis.py` file and change the values of:

```python
START_YEAR = ...
END_YEAR = ...
```

This modification represents a new experimental configuration, which is part of the concept of replicability.

### Run the analysis again

Execute the analysis using the instructions provided in the `README.md` file.

### Create a commit

Use the VS Code Source Control interface to create your commit.

:::{note}
Use a meaningful and descriptive commit message.
:::

### Push the branch

Use the VS Code Source Control interface to synchronize the changes.

### Create a pull tequest

Use the GitHub interface to create a pull request for the new branch.

### Review the pull request
A pull request review differs from a simple comment.  
When starting a review, GitHub groups comments together and allows the reviewer to formally approve the changes or request modifications.

The other teammate must:
- start a review on GitHub
- leave a comment requesting a modification to the selected year range

### Apply the requested changes

Modify the `START_YEAR` and/or `END_YEAR` values again according to the review comments.

### Resolve the review

After applying the requested changes:

```bash
git add .
git commit -m "<commit-message>"
git push
```

Then resolve the review conversation on GitHub.

### Merge the pull request

Once the review is approved, merge the pull request into `main`.

### Delete the branch

After the merge is completed, delete the source branch (not `main`).

# Evaluation
*To be determined*
