---
title: Open Development and Scientific Collaboration
date: 2026-07-23
label: lecture2
---

:::{iframe} https://docs.google.com/presentation/d/1ijGraNw6-um2RGUOEXWkiuJj1TtAihA5M9XOFJVw5Gg/embed?start=false&loop=false&delayms=3000
:width: 100%
:align: center
:title: Lecture 2 slides

Lecture 2 slides
:::

[Open in Google Slides ↗](https://docs.google.com/presentation/d/1ijGraNw6-um2RGUOEXWkiuJj1TtAihA5M9XOFJVw5Gg/edit?usp=sharing) — the embed above doesn't support text selection or the "Google Slides" button in its own toolbar.

## Auditing a Research Project

For each of five components, ask a simple question, then rate it 🟢 (usable
independently), 🟡 (usable with help), 🔴 (hard or impossible), or ⚪ (n/a):

| Component | Question |
|---|---|
| Data | Can the exact dataset be identified and accessed? |
| Code | Can the exact code version be retrieved? |
| Environment | Can the software environment be reconstructed? |
| Documentation | Can someone execute the workflow independently? |
| Governance | Would the project survive the departure of its main developer? |

Run this on one of your own projects — the result is usually the clearest
motivation for the rest of this lecture.

## Where an Open Project Actually Lives

An open project lives across several channels, each solving a specific
problem: **notebooks and docs** (the entry point for a newcomer), **issues**
(what is broken, planned, or decided), **pull requests** (why the code
changed, not just that it did), **discussions/forums** (questions from
people who are not you), **CI** (the claim that it still works, checked
continuously), and **releases** (versions someone can cite). None of these
were invented for industry — each replaces something a lab used to keep in
one person's head.

## Shell and Notebooks

Shell commands, unlike menus, don't change between OS versions and can be
pasted into an issue, a README, or a methods section:

```bash
pwd; ls -la; cd; less; history
```

Notebooks are a great teaching medium, but they hide a trap: cells can be
edited and re-run out of order, so the code shown may not be the code that
produced the output. Try it yourself in the
[course notebook](https://polymtl-reproducible-research.github.io/notebook-example/lab/):
change a variable, skip re-running a dependent cell, and watch the output go
stale. `Kernel → Restart & Run All` is the way to check whether a notebook
is even internally reproducible. Of 1.16 million notebooks on GitHub, only
24% ran without error and 4% reproduced their own stored outputs
{cite:p}`pimentel2019`. Of roughly 27,000 notebooks attached to
biomedical papers, only 1,203 ran to completion, and 879 reproduced the
published result {cite:p}`samuel2024` — for a reproducible artifact,
convert the notebook to a script.

## Contributing: Issues and Review

You don't need to write code to contribute — a typo, a broken example, or a
confusing error message is a real, useful report. A good issue is
reproducible by a stranger: what you expected vs. what happened, the exact
command and versions, the smallest failing example, and what you already
tried. A bad issue costs the maintainer several round-trips to fix.

Some journals now check the code instead of just trusting it: **JOSS**
reviews happen as a public GitHub issue where reviewers install and run the
software; **ACM's Artifact Review & Badging** prints badges for
availability, functionality, and reproduced/replicated results. You'll use
the JOSS reviewer checklist yourselves in Lab 4.

:::{admonition} Activity
:class: tip
Open a real issue on [this course's repository](http://github.com/polymtl-reproducible-research/myst_book) — something unclear, broken, or missing — then read a classmate's issue and say what you'd still need to act on it.
:::

## CI: A Robot That Checks Your Work

A CI server runs your commands on every push, on a clean machine with none
of your local mess. It answers one question — does this still work for
someone who is not you? This course's own site is built, translated to
French, and deployed automatically by a
[GitHub Action](https://github.com/polymtl-reproducible-research/myst_book/actions)
on every push.

## Governance

:::{figure} https://imgs.xkcd.com/comics/dependency.png
:alt: xkcd 2347, "Dependency" — a nearly toppling tower of blocks labeled with all of modern digital infrastructure, resting on one small, precarious block labeled "A project some random person in Nebraska has thanklessly maintained since 2003"
:width: 400px
:align: center

[xkcd 2347](https://xkcd.com/2347/), "Dependency" (CC BY-NC 2.5)
:::

Your project depends on software nobody was funded to maintain; if it stops
being maintained, your project can break with the next dependency or
hardware change. Governance
varies widely — from a single grant-funded lab team
([SpineReport](https://github.com/ivadomed/SpineReport)), to volunteer
steering groups ([BIDS](https://bids.neuroimaging.io/collaboration/governance.html)),
to industrialized maintenance
([scikit-learn](http://scikit-learn.org/stable/governance.html),
[PyTorch](https://pytorch.org/)). The underlying question is always the
same: who is allowed to say no, and who is paid to say yes?

For your own project, write down who actually *owns* each piece — the
GitHub org and repo, the data folder, the compute allocation, the domain
name — and ask: if that person's account were deactivated tonight, what
would you lose? Internal documentation (access, provenance, decisions,
ownership, an exit checklist) can and should live in version control too —
see [NeuroPoly's wiki](http://intranet.neuro.polymtl.ca) as an example. And
for data specifically: get consent for secondary uses at collection time,
not later — retrofitting it is usually impossible.

(use-of-ai-in-open-development)=
## Use of AI in Open Development

Use AI assistants well rather than pretending you didn't: they genuinely
help with docs, tests, commit messages, and reading unfamiliar code. But
running the same prompt twice can yield different results (try it — compare
two models on the same task), and neither run is recorded anywhere. Good
practice is to commit the prompt alongside the code it produced (e.g., a
trailer like `Assisted-by: Claude Opus 5`), and to review AI-generated code
as you would a stranger's pull request — you remain accountable for every
line. Several journals (JOSS, Wiley, Nature, Elsevier) now require an AI
usage disclosure — {cite:p}`resnik2025` discusses when such disclosure
should be mandatory, optional, or unnecessary.

:::{admonition} This book practices what it teaches
:class: important
See the [AI disclosure](../index.md#ai-disclosure) on the homepage.
:::

Agentic AI — agents that open issues and submit pull requests with little
human oversight — is a growing presence: contributing is now cheap, but
reviewing is not, and some projects have started
[refusing AI-generated contributions outright](https://github.com/melissawm/open-source-ai-contribution-policies).

## Further Resources

- **[How to open a GitHub issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-an-issue)**
- **[The Unix Shell (Software Carpentry)](https://swcarpentry.github.io/shell-novice/)**
- **[This course's notebook example](https://github.com/polymtl-reproducible-research/notebook-example)** and the **[Jupyter docs](https://docs.jupyter.org/en/latest/)**
- **[BIDS](https://bids.neuroimaging.io/collaboration/governance.html)** and **[scikit-learn](http://scikit-learn.org/stable/governance.html)** governance documents
