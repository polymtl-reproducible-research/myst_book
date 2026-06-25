---
title: Lab 4 — Reproducibility Review and Collaborative Maintenance
date: 2026-06-17
label: lab4
numbering:
  heading_2: false
---

# Introduction

:::{important}
**Submission deadline:** *To be determined*  
:::

This laboratory places students in the role of external reviewers and contributors to an open science project developed by another team in the course.

The objective is to evaluate the reproducibility of another team's research repository, assess the quality of its documentation and research artifacts, and contribute to its improvement through established collaborative development practices.

This exercise simulates real-world scientific software and open-source development workflows, where reproducibility, transparency, communication, and collaborative maintenance are essential components of research quality.

# Laboratory Overview

Teams will be paired together. During the first phase of the laboratory, each team will evaluate the repository of another team.

The evaluation team will:

1. Fork and inspect the assigned repository.
2. Attempt to reproduce the project's results.
3. Evaluate the repository using the reviewer checklist provided with the lab.
4. Identify reproducibility issues, documentation problems, workflow deficiencies, or software defects.
5. Report discovered issues through GitHub Issues.
6. When possible, propose a fix by creating and submitting a Pull Request.

The team being evaluated will act as repository maintainers. Their responsibilities include:

1. Responding to issues opened by the reviewers.
2. Discussing potential solutions and fixing issues.
3. Reviewing incoming pull requests.
4. Integrating accepted contributions following an appropriate development workflow.

After the first evaluation cycle is completed, the roles will be reversed:

- The original reviewers become maintainers.
- The original maintainers become reviewers.

This ensures that every team experiences both perspectives of collaborative open science.

# Reviewer responsabilities

## Repository Evaluation

TODO : a custom checklist inspired by JOSS checklist.

## Reproducibility Attempt

The primary goal of the evaluation is to determine whether an independent team can successfully reproduce the project using the repository contents alone.

Reviewers should therefore:

- Follow the provided instructions without relying on external explanations from the authors.
- Record any missing information or ambiguities.
- Document all encountered errors.
- Assess whether the repository contains sufficient information to reproduce the reported results.

If reproduction is not successful, reviewers should clearly identify the blocking issue and communicate it through GitHub.

## Reporting Issues

When a reproducibility problem, documentation gap, or software defect is identified, the evaluation team must create a GitHub Issue in the repository of the evaluated team.

<!-- A high-quality issue should:

- Clearly describe the problem.
- Explain how the issue was discovered.
- Include reproduction steps when applicable.
- Provide logs, screenshots, or other relevant evidence.
- Propose possible directions for resolution. -->

Communication should remain professional, constructive, and focused on improving the project.

## Contributing Fixes

The evaluation team should attempt to resolve identified issues via a fork and a Pull Request.

An adequate workflow is expected and will be evaluated.
<!-- The expected workflow is:

1. Fork the repository.
2. Create a dedicated branch.
3. Implement the proposed fix.
4. Commit changes using meaningful commit messages.
5. Open a Pull Request describing the modification. -->

<!-- The Pull Request should explain:

- The identified problem.
- The implemented solution.
- Any limitations or assumptions.
- Evidence that the fix was tested. -->

# Maintainer Responsibilities

## Issue Management

The maintainer team is responsible for responding to issues opened by the reviewers.

Maintainers should:

- Acknowledge reported issues.
- Reproduce and investigate the reported problem.
- Discuss possible solutions with the reviewers.
- Implement and document fixes when appropriate.

All modifications should follow an appropriate development workflow and be performed through branches and Pull Requests.

## Reviewing Contributions

The maintainer team is responsible for reviewing Pull Requests submitted by the reviewers.

Maintainers should:

- Evaluate the proposed solution.
- Provide constructive feedback when improvements are needed.
- Request modifications when appropriate.
- Approve and merge satisfactory contributions.
- Explain and justify decisions when a contribution is rejected.

# Evaluation

Teams will be evaluated on both their reviewer and maintainer roles.

The assessment will consider:

| Criterion | Description |
|------------|-------------|
| Repository Evaluation | Thoroughness of the reproducibility review |
| Issue Reporting | Clarity, professionalism, and usefulness of GitHub Issues |
| Pull Request | Technical appropriatness and justification of proposed changes |
| Pull Request Review | Constructiveness and rigor of code and documentation reviews |
| Development Workflow | Appropriate use of branches, commits, Pull Requests, and repository maintenance practices |
| Communication | Professional interactions between reviewers and maintainers throughout the process |

The emphasis of this laboratory is not solely on identifying defects, but on demonstrating effective open science practices and collaborative maintenance workflows.

# Question (will be removed)
- How do we evaluate the checklist? Do we (chargés de lab) use the same checklist that the team will be provided in the lab3 and looks if the students checklist match what we have in lab3?
- Both team should try to fix the bug to encourage discussion or only one?
- How much info do we want to give them for the standards? Do uncomment the commented lines or not?
- If there is no problem? We will give them a repo with bugs but how will we evaluate the maintainer role?
  - 2 options :
    1. During the evaluation of TP3, we will see if it is a "perfect repo" with no bugs, so we could make a copy of their repo and introduce bugs and code with no bugs (they could do a diff to see the problem otherwise)
    2. We could provide students with a repository created by the teaching team (for example, the Lab 1 repository) that intentionally contains bugs. Students would act as maintainers of this repository, requiring them to work with a codebase they did not originally develop.
