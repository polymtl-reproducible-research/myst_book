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

# From Reproducibility to Collaboration

Lecture 1 introduced reproducibility and replicability as properties of a
research artifact. This lecture turns to the *practice* that produces those
properties: how open projects are organized, who does the work of keeping
them alive, and which everyday tools and habits make collaboration possible
at all.

## Auditing a Research Project

Before looking at tools, it helps to know where a project actually stands.
For each of five components, ask a simple question:

| Component | Question |
|---|---|
| Data | Can the exact dataset be identified and accessed? |
| Code | Can the exact code version be retrieved? |
| Environment | Can the software environment be reconstructed? |
| Documentation | Can someone execute the workflow independently? |
| Governance | Would the project survive the departure of its main developer? |

:::{admonition} Rating scale
:class: tip
🟢 another researcher could use it independently · 🟡 usable with substantial
help · 🔴 difficult or impossible to reproduce · ⚪ not applicable or unknown
:::

Run this audit on one of your own projects. The result is usually the
clearest motivation for everything that follows in this lecture.

## Where an Open Project Actually Lives

An open project is not just a pile of code. It lives across several
channels, each solving a specific problem:

- **Notebooks and docs** — the entry point for a newcomer
- **Issues** — what is broken, what is planned, what was decided
- **Pull requests** — why the code changed, not just that it did
- **Discussions / forums** — questions from people who are not you
- **CI** — the claim that it still works, checked continuously
- **Releases** — versions someone can cite

None of these were invented for industry. Each one replaces something a lab
used to keep in one person's head, or one person's inbox.

## The Issue as an Open Lab Notebook

A GitHub issue can be more than a bug report — it can be a lab notebook page
anyone can read. In one real example from the
[ivadomed](https://github.com/ivadomed/ivadomed/issues/841) project, a single issue
documents a new feature, communication with international teams, experiments, datasets named, commands pasted,
results plotted — in public, while the work was still in progress.

## Working from the Command Line

Many open-source tools are driven from the command line: Git, Python, CI,
the compute cluster. Menus change between versions and operating systems;
shell commands do not. A command can be pasted into an issue, a README, or a
methods section. A sequence of clicks cannot be pasted, cannot be diffed,
and cannot be re-run.

A few commands to get comfortable with:

```bash
pwd       # where am I
ls -la    # what is here, including hidden files
cd        # move
less      # read a file without opening an editor (q to quit)
history   # what did I just do
```

:::{admonition} Try it
:class: tip
```bash
echo $SHELL   # which shell did you get?
git clone https://github.com/polymtl-reproducible-research/ing8100.git
cd ing8100
ls -la        # .git and .github, neither is visible in Finder
git log -5    # the history of the syllabus on your Moodle
```

You can build this course's own material locally the same way: 

```bash
git clone https://github.com/polymtl-reproducible-research/myst_book.git
cd myst_book
conda create -n ing8100 python=3.12   # a fresh environment for this course
conda activate ing8100
conda install -c conda-forge mystmd   # brings Node with it
myst start                            # opens the site at localhost, with live reload
```
:::

## Jupyter Notebooks: Convenient but Fragile

Notebooks are an excellent teaching and exploration medium — narrative,
code, and output live in one artifact, and changing a parameter to see a new
figure is immediate. They also make several failure modes easy:

- Git sees JSON, not markdown or Python — a one-character change can produce
  a 400-line diff, and code review becomes unreadable.
- Binary outputs get committed. Base64-encoded images bloat the repository,
  permanently.
- Cells can be edited and re-run out of order, so the code shown is not
  necessarily the code that produced the output.

Two studies make the scale of the problem concrete. Of 1.16 million
notebooks on GitHub, only 24% ran without error and just 4% reproduced the
outputs already stored inside them (Pimentel et al., 2019). Of roughly
27,000 notebooks attached to biomedical papers, 1,203 ran to completion and
879 reproduced the published result (GigaScience, 2024).

:::{admonition} Recommendation
:class: important
For a reproducible artifact, convert your notebook to a script — or start
directly from a script. Use Kernel → Restart & Run All as a quick check of
whether a notebook is even internally reproducible.
:::

## The Contribution Ladder

You do not need to write code to contribute to an open project. A typo in
the documentation, a broken example in a README, or an error message that
does not say what to do next are all real, useful reports. Nobody starts at
the top of the ladder:

1. **Report** — a well-documented issue
2. **Propose** — a conceptual solution, before writing any code
3. **Document** — fix the docs, add the missing example
4. **Submit** — a pull request
5. **Sustain** — answer other people's questions, review other people's code

Report and Document are where the shortage is.

### Anatomy of a Good Issue

A good issue is reproducible by a stranger:

- What you expected, what happened, and the exact command
- Versions: software, OS, and the commit hash if on a development version
- The smallest example that still shows the problem
- What you already tried
- Whether you are willing to work on it

A bad issue costs the maintainer three round-trips to become a good one —
and each round-trip is a day.

## Evaluating Software Like a Reviewer

Two models make software review itself reproducible:

- **[JOSS](https://joss.theoj.org/)** (Journal of Open Source Software) — the
  peer review *is* the code review. It happens in a public GitHub issue; the
  reviewers install the software and run it.
- **[ACM Artifact Review & Badging](https://www.acm.org/publications/policies/artifact-review-and-badging-current)** — badges printed on the paper: Artifacts
  Available, Artifacts Evaluated (Functional / Reusable), Results
  Reproduced, Results Replicated.

The [JOSS reviewer checklist](https://joss.readthedocs.io/en/latest/review_checklist.html#) covers:

- **General** — repository reachable, OSI-approved license, appropriate
  authorship, scholarly significance
- **Development history** — sustained development over months, developed
  openly, more than one contributor, releases and a contribution pathway
- **Functionality** — installation proceeds as documented, functional and
  performance claims confirmed
- **Documentation** — statement of need, dependencies listed, example usage,
  API documented, automated tests, community guidelines
- **Paper** — summary, statement of need, state of the field, software
  design, research impact, AI usage disclosure

You will use this checklist yourself in Lab 4, on another team's project.

## This Course Builds Itself

The syllabus you download from Moodle is not typed and uploaded by a human
— it is compiled by a robot. Editing one line of the LaTeX source and
pushing it triggers GitHub Actions, which compiles the document in a clean
container and attaches the PDF to a release. The release URL is what Moodle
points at. No human copies a PDF anywhere: the document you are holding is
traceable to a specific commit.

That is what continuous integration (CI) is for: a claim that a project
still works, checked automatically, every time.

## Who Pays for the Commons

Every dependency in your stack is software that somebody, somewhere,
maintains — often without being funded to do so
([xkcd 2347](https://xkcd.com/2347/) is the classic illustration). "Free"
means free of charge, not free of cost. Maintainer burnout is a documented
failure mode of scientific infrastructure. The tool you depend on being
alive in five years is a research risk you are carrying, whether or not you
think about it — so be a contributor to the commons, not just a user of it.

## Governance: Personal, Lab, Community

Projects sit somewhere on a spectrum from a single person's laptop to a
community-run standard. Three real examples show how differently governance
can be structured:

- **[BIDS](https://bids.neuroimaging.io/)** — run entirely by volunteers. A
  steering group of 5, elected by contributors; 13 self-nominated
  maintainers approved by majority. Changes go through a public proposal:
  draft → pull request → at least 10 days of community comment → merge.
- **[DIPY](https://dipy.org/)** — a scientific library, grant-funded. The
  core team sits inside an academic lab; governance follows the funding, and
  continuity depends on the next grant renewal.
- **[scikit-learn](https://scikit-learn.org/)** — a library that
  industrialized its own maintenance. Started at Inria; a spin-out company
  now employs most core maintainers full-time, with further funded posts
  from other foundations and donated CI/hosting.

Three governance models, one underlying question: who is allowed to say no,
and who is paid to say yes?

### The Permissions Inventory

For your own project, write the list: who owns the GitHub organization
(owner, not just admin)? Whose account holds the data folder? Whose PI
account holds the compute allocation? Whose credit card pays for the domain
name? Whose ORCID is on the data repository deposit?

:::{admonition} Test
:class: warning
If that person's account were deactivated tonight, what would you lose?
:::

### A Lab Manual, in Version Control

Internal documentation can be a repository too. NeuroPoly's internal wiki
(hosted at intranet.neuro.polymtl.ca, sourced from
[github.com/neuropoly/intranet.neuro.polymtl.ca](https://github.com/neuropoly/intranet.neuro.polymtl.ca))
covers onboarding by role, computing resources, dataset curation, equipment,
and practical life in Montreal. Any lab member can improve it — because
improving it is a pull request.

A useful internal-documentation checklist:

- **Access** — how to get on each system, and who grants it
- **Provenance** — where each dataset came from, who collected it, under
  what protocol
- **Decisions** — why the pipeline changed, and when
- **Ownership** — the permissions inventory, kept current
- **Exit checklist** — what a departing member hands over, and to whom

Write the onboarding document while you are being onboarded.

### Consent, Secondary Use, and Retention

Data governance decisions are easiest to get right at collection time, not
later. Will there be secondary uses of this data? Get consent for them
now — retrofitting consent later is usually impossible. Store the
permissions next to the data, not in an email. Retention has two ends: a
minimum period you may be legally required to keep data, and a maximum
after which you may be required to destroy it. Polytechnique's data
management policy (see Annex 2) spells out what a data management plan
should contain.

## Use of AI in Open Development

You may use AI assistants in this course — the expectation is that you use
them well, not that you pretend you did not. They genuinely help with
documentation and docstrings, tests for code that has none, changelogs and
commit messages, reading an unfamiliar codebase, and a first-pass review of
your own work.

They also introduce a specific hazard for reproducibility. Running the same
prompt twice can produce different code, with different variable names or a
different approach — and neither run is recorded anywhere in your
repository. The model behind a given name changes over time, and old
versions are retired. "Generated with an assistant" is not a version.

:::{admonition} Good practice
:class: important
Record the model and version you used (e.g., Claude Opus 5) and the prompt,
alongside the commit. Treat AI-generated code as a contribution that still
needs review — the same review a stranger's pull request would get. You
remain the author, and you are accountable for every line.
:::

JOSS now requires an AI usage disclosure section in submitted papers.

:::{admonition} Activity
:class: tip
Take a function generated by an AI assistant and review it as you would a
pull request from someone you have never met: Does it do what it claims in
every case? What is untested? What would you have to ask the author? Would
you merge it — and what would you need in the commit message to understand
it in a year?
:::

## Where This Goes Next

- **Lab 1** — onboarding: accounts, environment, and your first documented
  issue
- **Lecture 3** — version control: the Code and Environment rows of the
  audit
- **Lab 4** — you use the JOSS reviewer checklist on another team's project

:::{admonition} Note
:class: note
The audit you ran at the start of this lecture is the one that will
eventually be run on you.
:::
