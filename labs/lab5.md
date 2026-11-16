---
title: Lab 5 — Reflection on Reproducible Research and Open Science
date: 2026-06-10
label: lab5
numbering:
  heading_2: false
---

# Introduction

:::{important}
**Submission deadline:** November 24th, 2026  
**Team formation:** This laboratory must be completed in teams of two students.
:::

Throughout this course, you have built a reproducible research project (Lab 3), reproduced and reviewed another team's project (Lab 4), and had your own project reviewed in return.

The purpose of this final laboratory is to step back and reflect: what worked, what broke, what it cost, and whether your project will still be usable in five years.

---

# Presentation

- The presentation must be prepared using **Google Slides**.
- Duration: **10 minutes per team**. Both team members must present.
- A **5-minute question period** with the class follows each presentation. Discussion is encouraged.
- **Publish your slides:** before the session, paste a view-only link to your Google Slides in your team's row of the shared spreadsheet, available on Moodle (section **Laboratoire**, *Lab 5 : présentations orales*). The same spreadsheet gives the link to each team's evaluation form.

:::{important}
Your slides must be **self-explanatory**: every claim must be backed by a link (issue, PR, commit, DOI). This is good practice for slides and for scientific reports in general.

This presentation is a reflection, not a demo of tools. Explain *why* you made your choices, *what* went wrong, and *what* you learned.
:::

## Structure

### 1. The project in brief (~1 min)

- Research question
- Choice of data
- Links to your repository and code

### 2. What you built (Lab 3, ~2 min)

- Two or three design choices, justified: repository structure, environment, branching strategy, licence, etc.
- What you would do differently if you started over.

### 3. Will your project still exist in 5 years? (~3 min)

- **Analysis of one major dependency of your project** (e.g. numpy, pytorch): activity level, maintainer responsiveness, robustness of your code to future versions.
- **Long-term maintainability of your project**: governance, bus factor, required expertise, potential for community contributions.

### 4. Reproducing another study (Lab 4, ~3 min)

- What worked and what broke when you reproduced the other team's study.
- What the review of your own project revealed: strengths, weaknesses, suggestions for improvement.
- Show one or two specific issues or PRs (with links) and what was fixed.

### 5. Wrap-up (~1 min)

- Cost and benefit of reproducibility in your case.
- One recommendation for next year's cohort.

---

# Evaluation

The presentation is evaluated through a Google Form (one form per presenting team, linked in the same spreadsheet on Moodle), completed by both peers and the teaching staff. Enter your matricule in the form; self-evaluations are not counted.

The final grade is composed equally of peer evaluation and instructor evaluation (50% each). Each criterion is rated on a 1–5 scale.

## Evaluation criteria

| Criterion                                 | Weight | Description                                                                                                                         |
| ----------------------------------------- | -----: | ----------------------------------------------------------------------------------------------------------------------------------- |
| Design choices (Lab 3)                    |    15% | Two or three design choices clearly justified, with a critical look at what would be done differently.                              |
| Sustainability analysis                   |    20% | Evidence-based analysis of a major dependency and of the team's own project's long-term maintainability (governance, bus factor, community).     |
| Reproduction and review (Lab 4)           |    25% | Honest account of what worked and what broke, both as reproducer and as reviewed team, backed by specific issues/PRs and their fixes. |
| Wrap-up and recommendation                |    10% | Clear assessment of the cost and benefit of reproducibility, and a concrete recommendation for next year's cohort.                  |
| Self-explanatory slides                   |    10% | Every claim is backed by a link (issue, PR, commit, DOI); slides are understandable without the speakers.                           |
| Clarity of presentation and answers       |    10% | Logical flow, clear explanations, and relevant answers to questions from the class.                                                 |
| Time management                           |    10% | The 10-minute duration and the required structure are respected.                                                                   |
