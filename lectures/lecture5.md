---
title: Licences, Intellectual Property, and Publication
date: 2026-10-19
label: lecture5
---

:::{iframe} https://docs.google.com/presentation/d/1w-eMMQgRC8GPOd2nP1JRHZMToqjBG_TRT2yEIT0gEyg/embed?start=false&loop=false&delayms=3000
:width: 100%
:align: center
:title: Lecture 5 slides

[Open in Google Slides](https://docs.google.com/presentation/d/1w-eMMQgRC8GPOd2nP1JRHZMToqjBG_TRT2yEIT0gEyg/edit?usp=sharing)
:::

# Overview

This lecture covers the legal and publishing side of open research: what
intellectual property (IP) protects in a research project, who owns it, how
licences make a protected work open, and what publishers and funders now
expect when it comes to sharing articles, data, and code. It complements
two other Polytechnique courses: CAP7210 (IP and patents) and CAP7005
(copyright and open access).

## What We'll Cover

- The forms of IP relevant to research, and what copyright does (and doesn't) protect
- How to figure out who owns a research output
- What a licence is, and how to read one
- Creative Commons licences for text, figures, and data; open-source licences for code
- How openness and valorization can coexist
- Data availability statements, ORCID, and open access requirements

# Intellectual Property in Open Research

Four ideas are easy to mix up: **IP** (what rights protect what?),
**ownership** (who holds them?), **open dissemination** (on what terms can
others reuse the work?), and **valorization** (how is value created from
research?). The *what* determines the *how*: before choosing a licence or a
valorization path, you need to know what you hold, whether it's protected,
and who owns it.

| Right | Protects | How you get it | Term (Canada) |
|---|---|---|---|
| **Copyright** | Original *expression*: code, text, figures, videos | Automatically, on creation | Author's life + 70 years |
| **Patent** | An *invention* that is new, useful, and non-obvious | Application and examination | 20 years from filing |
| **Trademark** | A name, logo, or other distinctive sign | Use or registration | 10 years, renewable |
| **Trade secret** | Information you keep confidential | Contracts and governance | As long as it stays secret |

Open science lives almost entirely in the copyright row. Copyright protects
the **concrete expression** of a work — never the underlying idea,
algorithm, or raw fact. **Raw data** (measurements, elevations, flows) belong
to no one, but their *form* (file structure, selection, analysis scripts)
can be protected, and access can still be restricted by contract.
**Personal information** can't be owned either, but it is governed by
privacy law and ethics (see [Lecture 4](lecture4.md)). And under current
Canadian law, originality requires a human author, so purely
**AI-generated code** is generally not protected — though case law is still
evolving.

:::{admonition} Publishing before patenting
:class: warning
Disclosing an invention — in a paper, preprint, talk, or public repository —
can destroy its novelty. Canada and the US have a one-year grace period for
the inventor's own disclosure; most other countries don't. If you think you
have an invention, talk to your technology transfer office *before* you
publish.
:::

## Who Owns a Research Output?

By default, the author is the first owner of a work. Several other layers
can change that, and it's worth checking them in this order: (1) **the
law** — is there employment, or several authors? (2) **funding and
partnership contracts**; (3) **your institution's IP policies**, which often
differ for students and employees; (4) **specific agreements** with your
supervisor or collaborators; and (5) the **licences of third-party
components** you build on (libraries, datasets, pre-trained models).

:::{admonition} Case study: GéoCrue
:class: tip
After the 2017 and 2019 floods, Quebec modernized its regulation on flood
zones, and MRCs can now be tasked with producing more precise flood maps. In
this fictional (but realistic) project, a civil engineering PhD student and
his supervisor build a tool that produces high-resolution flood maps from
public LiDAR data and measured water flows, using a hydraulic library
licensed under the GPLv3. The project is funded by NSERC and an MRC.

Who owns the results? What does the GPLv3 library imply for the student's
own code? Which data can be opened? Working through the five layers above,
the student and supervisor turn out to own the code and can choose an open
licence — but the MRC's data on buildings and damage claims cannot be
opened, because it contains personal and confidential information.
:::

# Licences

A licence is written permission from the owner, with conditions. It does
**not** transfer ownership — you remain the owner of code you release
under an open licence.

:::{admonition} No licence = all rights reserved
:class: important
A public GitHub repository without a licence can be read, but not legally
copied, modified, or redistributed. Rights granted by a licence generally
can't be taken back, so choose one *before* publishing.
:::

When reading a licence, ask: **who** grants the rights, **what** is allowed
(use, modify, distribute, commercial use), **on what conditions**
(attribution, share-alike), **what warranties** (usually none, "as is"), and
**for how long**. A licence also doesn't cover trademarks: a project's name
and logo stay protected unless stated otherwise.

## Creative Commons Licences

[Creative Commons](https://creativecommons.org/) (CC) licences suit
publications, figures, videos, and datasets — not code. They combine
building blocks: **BY** (attribution), **SA** (share-alike), **NC**
(non-commercial), and **ND** (no derivatives). **CC0** waives all rights,
including attribution. Use the current version (4.0) and state the licence
clearly on the work itself. The FRQ's open access policy strongly
encourages **CC BY 4.0**, with CC0 also accepted.

:::{admonition} Example: reusing CC0 data from OpenNeuro
:class: tip
A student builds a new dataset from a CC0 dataset on
[OpenNeuro](https://openneuro.org/) (extra preprocessing, filtering, new
labels). Do they have to cite the original? **Legally, no**: CC0 waives
attribution. **Scientifically, yes**: citation is a scholarly norm, not a
legal one — it gives provenance, credits the people who shared the data,
and not citing is plagiarism even when copyright doesn't apply. Cite the
dataset's DOI and version, share the code that made the changes, document
them (README, CHANGELOG — as in [Lab 2](../labs/lab2.md)), and choose a
licence for the new dataset.
:::

## Licences for Code

Code licences fall into three families: **proprietary** (no reuse without
permission), **copyleft** (e.g., [GPLv3](https://www.gnu.org/licenses/gpl-3.0.html):
modification and redistribution allowed, but distributed derivatives must
keep the same licence), and **permissive** (e.g.,
[MIT](https://opensource.org/license/mit), BSD,
[Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0): few
restrictions). When you **reuse** code, check whether its licence
constrains yours — the GPLv3 library in the GéoCrue case does. When you
**wrote** it, you choose. For maximum reuse, MIT for code and CC BY for
everything else is a simple, widely understood combination. Also note that
some platforms automatically license what you post (e.g.,
[Stack Overflow](https://stackoverflow.com/help/licensing)).

# Openness and Valorization

Opening your work doesn't prevent creating value from it — it changes where
the value lies. "Open" is about permissions, not price: open licences
usually allow commercial use. Valorizing doesn't only mean patenting —
much of it happens through services, expertise, contracts, and trademarks.
And publishing means losing what you disclosed (e.g., patentability), not
necessarily the value.

In the GéoCrue case, the code is GPLv3, the maps are CC BY, and a company
sells what is scarce and hard to copy: local calibration expertise,
engineer-sealed reports, a hosted monitoring service, training, and a
trusted brand name. The same pattern shows up in academic labs: when a
lab's open-source MRI analysis tools become widely used, organizations
running clinical trials hire the lab's *expertise* to analyze their data or
design acquisition protocols — not the software. Openness created that
demand in the first place.

:::{admonition} Five reflexes
:class: important
1. Document who contributed what, when, and in what context.
2. Read your funding and partnership contracts before publishing.
3. Disclose inventions to your institution before making them public.
4. Inventory third-party components and their licences.
5. Before signing anything, talk to the right people: supervisor,
   technology transfer office, legal services, ethics board, library.
:::

# Publications and Reproducibility

## Data Availability Statements

Since the mid-2010s, most publishers require or strongly encourage a **data
availability statement** (DAS). At a minimum, it says where the data and
code are, and under what licence — e.g., *"Data and code associated with
this article are available at `https://doi.org/...` under CC BY 4.0 (data)
and MIT (code)."* Prefer a DOI over a Google Drive link, and avoid
"available upon request," which rarely works in practice {cite:p}`graf2020`.
Articles whose DAS links to a repository are also associated with more
citations {cite:p}`colavizza2020,colavizza2024`. More broadly,
[DORA](https://sfdora.org/) pushes to recognize data and code as research
contributions in their own right; Polytechnique signed it in January 2026.

An [ORCID iD](https://orcid.org/) — a free, persistent 16-digit identifier
— follows you across institutions and distinguishes you from researchers
with similar names. Publishers and funders increasingly ask for it: create
one early and keep it up to date.

## Open Access

Open access means peer-reviewed research is freely available online,
without a paywall. Current requirements:

- **Tri-Agency** (NSERC, CIHR, SSHRC): under the
  [2026 Open Access Policy on Publications](https://cihr-irsc.gc.ca/e/32005.html),
  articles from grants awarded on or after January 1, 2027 must be openly
  available immediately (the previous policy allowed a 12-month delay).
- **FRQ**: publications under CC BY (or equivalent), theses freely available
  immediately, for both grants and scholarships.
- **Polytechnique**: no institutional open access policy yet; one is under review.

There are two main routes. **Gold**: publish in an open access journal,
usually for a fee. **Green** (self-archiving): deposit your peer-reviewed
manuscript, usually for free, in a disciplinary archive (e.g.,
[arXiv](https://arxiv.org/)) or an institutional repository (e.g.,
[PolyPublie](https://publications.polymtl.ca/)), after any publisher
embargo. Check a journal's policies before submitting, e.g. with
[Open Policy Finder](https://openpolicyfinder.jisc.ac.uk/).

## Beyond the PDF

Publications are evolving from static PDFs into interactive, executable
objects that bundle text, code, data, and computing environment —
reproducible by design. Examples include the
[qMRLab MOOC](https://qmrlab.org/mooc/), [NeuroLibre](https://neurolibre.org/)
preprints, [Aperture Neuro](https://apertureneuro.org/), and this course book
itself. What gets reviewed, cited, and licensed is no longer just text, and
each component may carry its own licence.

:::{admonition} Discussion
:class: note
Peer review of papers is usually anonymous, while code review (GitHub pull
requests, [JOSS](https://joss.theoj.org/)) is usually public and signed.
Anonymity allows candor; open review brings accountability and credit, but
can make criticism harder. Should reviewing — papers or code — count as a
research contribution?
:::

## Further Resources

- [Choose a License](https://choosealicense.com/) — Plain-language guide to picking an open-source licence
- [Creative Commons licence chooser](https://creativecommons.org/chooser/) — Interactive tool for CC licences
- [Tri-Agency Open Access Policy on Publications](https://cihr-irsc.gc.ca/e/32005.html) — Federal open access requirements
- [Open Policy Finder](https://openpolicyfinder.jisc.ac.uk/) — Publishers' self-archiving and embargo policies
