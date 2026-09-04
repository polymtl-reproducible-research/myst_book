---
title: Version Control and Distribution of Code
date: 2026-07-30
label: lecture3
---

:::{iframe} https://docs.google.com/presentation/d/18YuN3zLDkFI7wXzsOqVnSGbh2wbge-g2bqXqamUJbeE/embed?start=false&loop=false&delayms=3000
:width: 100%
:align: center
:title: Lecture 3 slides

[Open in Google Slides](https://docs.google.com/presentation/d/18YuN3zLDkFI7wXzsOqVnSGbh2wbge-g2bqXqamUJbeE/edit?usp=sharing)
:::

## Why Version Control

:::{figure} https://phdcomics.com/comics/archive/phd101212s.gif
:alt: PhD Comics strip "FINAL".doc — a grad student's file goes through FINAL.doc, FINAL_rev.2.doc, FINAL_rev.6.COMMENTS.doc, FINAL_rev.8.comments5.CORRECTIONS.doc, FINAL_rev.18.comments7.corrections9.MORE.30.doc, and finally FINAL_rev.22.comments49.corrections.10.#@$%WHYDIDICOMETOGRADSCHOOL????.doc
:width: 400px
:align: center

["Final".doc](https://phdcomics.com/comics/archive.php?comicid=1531), Jorge Cham, PHD Comics
:::

If you've ever ended up with `Final.doc`, then `Final_v2.doc`, then
`Final_v2_reallyfinal.doc` — you've already felt the problem a version
control system (VCS) solves. A VCS keeps a repository of every version of
every file, replicated on each contributor's machine, and can answer: what
changed between the run that worked and now? Who changed the code or data,
and why? Can I get back exactly what we had before? Git is the dominant
example — a *distributed* VCS, meaning every clone carries the full history,
not just a snapshot {cite:p}`chacon2014`.

## Branching, Merging, and Pull Requests

A branch is an independent line of work off the main history; `git branch`
shows which one you're on. Two people can each commit to their own branch,
then merge one into the other — Git resolves this automatically when the
changes don't overlap, and asks you to resolve a conflict by hand when they
do (e.g., two different values proposed for the same line).

A **pull request** (or "merge request" on GitLab) is a proposal to merge one
branch into another, opened for discussion and review before it happens —
the mechanism, on GitHub, by which an outside contributor proposes a change
without touching the main branch directly.

## Hosting and Long-Term Availability

Git still needs a server to host the shared repository: a hosting service
(GitHub, GitLab, Bitbucket, or the non-profit
[Codeberg](https://codeberg.org/) — see this
[comparison](https://en.wikipedia.org/wiki/Comparison_of_source-code-hosting_facilities))
or a self-hosted server, which trades convenience for control and a real
maintenance burden.

*Cloning* (a native Git feature) gets you a local copy without changing who
owns the project. *Forking* (a hosting-service feature, not a Git one) makes
you the owner of your own copy, which you can modify freely and later
propose back to the original project via a pull request.

:::{admonition} Fun fact
:class: note
GitHub periodically archives a snapshot of every active public repository
on film, stored in the
[Arctic Code Vault](https://archiveprogram.github.com/arctic-vault/) near
the North Pole — a 500-year bet on long-term code availability.
:::

## Releases and Distribution

A Git **tag** is a named pointer to a specific commit; GitHub turns a tag
into a **release** — a changelog, a link to that commit, and a bundle of the
source code (e.g., NumPy 2.0, or Node.js's odd-numbered "experimental"
releases). What a release actually ships varies:

- **Source + install instructions** (e.g., the NVM install script)
- **Source + build instructions** (e.g., building PyTorch from source)
- **Prebuilt binaries** (e.g., VLC, or a PyPI package installed with `pip`)
- **All of the above** (e.g., Node.js: binaries, build docs, and `npm`)

Dependencies are usually kept out of the repository and declared instead
(`requirements.txt`, `package.json`) — pinning exact versions
(`package-lock.json`) is what makes an install reproducible later.

## Reproducible Environments

The same code can fail on a different OS, a different library version, or a
port already in use — "works on my machine" is a real, recurring failure
mode. Two ways to package an environment against it: a **virtual machine**
(a full OS emulation — heavy, but complete) or a **container**, most
commonly **Docker** (lightweight, Linux-kernel-based, configured in a
Dockerfile). Within a single language, Python's `venv` isolates
dependencies per project — commit `requirements.txt`, never the `.venv/`
folder — and **conda** goes further, managing Python itself alongside
non-Python dependencies (compilers, CUDA, R) via a committed
`environment.yml`.

## CI/CD

**Continuous Integration** automates checking new code on every push, on a
clean machine: if it builds and the tests pass there, it'll work for your
reviewer, your colleague, and future you. **Continuous Deployment** then
publishes something automatically once checks pass — a release, a doc site,
a Docker image. On GitHub, this is **Actions**: workflows built from
reusable blocks plus shell commands, which can also gate a pull request on
tests passing.

:::{admonition} Exercises
:class: tip
Work through [semver.org](https://semver.org)'s own questions about
Semantic Versioning 2.0.0, then compare how a well-known project (the Linux
kernel, Firefox, Chrome) actually versions its releases against that spec.
:::

## Version Control and Open Science

Version control supports reproducibility directly: it ties changes in
results to changes in code, gives publications a stable reference point,
and automates the change history that makes replication attempts possible
{cite:p}`ram2013`. Lecture 4 picks this up for data and computational
environments specifically.

## Further Resources

- **[Pro Git](https://git-scm.com/book)** — the free, canonical Git book (Chacon & Straub, cited in References)
- **[Comparison of source-code-hosting facilities](https://en.wikipedia.org/wiki/Comparison_of_source-code-hosting_facilities)**
- **[GitHub Arctic Code Vault](https://archiveprogram.github.com/arctic-vault/)**
- **[Semantic Versioning 2.0.0](https://semver.org)**
- **[Docker](https://docs.docker.com/) and [conda](https://docs.conda.io/en/latest/)** documentation
